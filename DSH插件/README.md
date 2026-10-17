# dsh-av-continuous

A [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) host-side tool plugin that **samples a video continuously** and **transcribes its speech locally**, then puts both on **one timeline**.

Two model-callable tools:

| Tool | What it does |
| --- | --- |
| `read_video_continuous` | Samples a video with ffmpeg at a fixed interval and returns the frames **as native image content blocks**, each labelled with its timestamp. |
| `transcribe_audio_vad` | Runs a voice-activity pass first, then transcribes only the surviving speech with a **local whisper.cpp** engine, returning timestamped text. |

Everything runs on the machine. No frame or audio sample is uploaded, and no vision or ASR API key is used.

English · [中文](README.zh.md)

## Why another video plugin

- **Fixed-interval sampling, not keyframes or scene cuts.** Most video plugins hand the model keyframes or frames chosen by a scene detector, which by construction skips whatever happens *between* cuts. This one uses ffmpeg's `fps` filter to emit one frame per interval for the whole duration, and uses `ffprobe`'s duration and frame rate to decide the density.
- **Loudness is not speech.** Engine noise, low-frequency rumble and a whistle can all be louder than a person talking, and they defeat any level meter. A Silero VAD pass decides what is speech *before* the recogniser sees it.
- **One clock.** Frames and speech land in a single ascending timeline, so "what was on screen" and "what was said" line up instead of being two lists you correlate by hand.

## Requirements

| Dependency | Required for | Notes |
| --- | --- | --- |
| `ffmpeg` + `ffprobe` **6.0+** | Frame sampling; audio normalisation | `winget install --id Gyan.FFmpeg -e`, `brew install ffmpeg`, or `apt install ffmpeg` |
| `whisper.cpp` — `whisper-cli` / `whisper` / `main` **or** `whisper-server`, plus a `ggml-*.bin` model | Transcription | Both transports supported; see [Whisper transports](#whisper-transports) |
| `onnxruntime-node` + `silero_vad.onnx` | *Optional*, strongly recommended | Silero VAD. Without it the plugin falls back to a built-in energy VAD and says so |

Missing engines **degrade**, they do not crash: the tool returns install guidance, and for audio it still reports which regions the VAD kept.

## Install

```sh
# from npm
dsh plugin --profile desktop add dsh-av-continuous

# or from a clone (the built dist/ is committed, so no build step is needed)
git clone <repo> && cd dsh-av-continuous && pnpm install && pnpm build
dsh plugin --profile desktop add link:<absolute path to the clone>
```

Restart DSH after installing.

## Tools

### `read_video_continuous`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `videoPath` | string | — (required) | Video file. Relative paths resolve against the session working directory. Any container ffmpeg can open. |
| `every` | number | `1` | Seconds between sampled frames. Minimum `0.04`. |
| `maxFrames` | integer | `60` | Frame budget. Hard limit `200`. |

When the interval would exceed the budget the tool keeps the **earliest** frames and reports the `every` that *would* have covered the whole video, rather than silently handing back a truncated view.

```
sampled 6 frame(s) every 2s of 12s at 10.000 fps, 640x360 px
[00:00.0] frame #0  <image>
[00:02.0] frame #1  <image>
…
```

Frames are planned against the **last video frame** (`duration - 1/fps`), not the container duration, so the read never promises a tail frame that ffmpeg's `fps` filter will not emit.

### `transcribe_audio_vad`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `audioPath` | string | — (required) | Audio file, or a video file whose audio track is used. |
| `vadThreshold` | number | `0.30` | Speech probability a window must reach to count as voice. |
| `language` | string | auto | ISO-639-1 (`zh`, `en`, …). A non-two-letter value falls back to auto-detection and is reported in `warnings`. |
| `alignToVideo` | string | — | Path to the source video. When given, the result merges sampled frame labels with the speech spans into one ascending timeline. |
| `alignEvery` | number | `1` | Seconds between the frame labels on that merged timeline. **Pass the same value you gave `read_video_continuous`**, or the two sides will not share a grid. |

```
engine ready: yes
vad engine: silero (threshold 0.3)
speech: 7.49s over 4 segment(s) of 11s (68.1%)

--- merged timeline ---
[00:00.0] frame #0
[00:00.3]-[00:02.2] speech: And so my fellow Americans.
[00:02.0] frame #1
[00:03.3]-[00:04.3] speech: ASK NOT!
[00:04.0] frame #2
[00:05.4]-[00:07.4] speech: What your country can do for you?
[00:06.0] frame #3
[00:08.0] frame #4
[00:08.2]-[00:10.4] speech: Ask what you can do for your country.
[00:10.0] frame #5
```

## Configuration

Nothing machine-specific is hard-coded. Override the bundle row from your profile's `cordis.patch.yml`:

```yaml
- id: dsh-av-continuous
  config:
    ffmpegPath: 'D:\tools\ffmpeg\bin\ffmpeg.exe'
    ffprobePath: 'D:\tools\ffmpeg\bin\ffprobe.exe'
    whisperPath: 'D:\tools\whisper\whisper-server.exe'
    whisperModelPath: 'D:\models\ggml-base.bin'
    vadModelPath: 'D:\models\silero_vad.onnx'
    vadEngine: auto          # auto | silero | heuristic
    frameFormat: jpeg        # jpeg | png
    maxFrameWidth: 1280
    whisperThreads: 4
    commandTimeoutMs: 120000
```

Engine discovery order: config → environment (`DSH_AV_FFMPEG`, `DSH_AV_FFPROBE`, `DSH_AV_WHISPER`, `DSH_AV_WHISPER_MODEL`, `DSH_AV_VAD_MODEL`) → `PATH` → common install locations. `ffprobe` is also looked for next to `ffmpegPath`.

## Whisper transports

Upstream stopped publishing prebuilt CLI binaries, while the Vulkan/GPU builds people download ship `whisper-server` only. Both work; the plugin picks the transport from the resolved executable's name.

- **`whisper-cli` / `whisper` / `main`** — one-shot CLI per speech region; `-oj` writes a JSON sidecar the plugin reads.
- **`whisper-server`** — the model loads once, each speech region is POSTed to `/inference` as `verbose_json` (the only response shape carrying segment boundaries), and the server is stopped afterwards.

> **whisper.cpp cannot open paths containing non-ASCII characters.** It parses its command line in the ANSI code page, prints the path mangled, and then **crashes while loading the model** (Windows exit code `3221226505` = `0xC0000409`). Keep `whisperModelPath` on a pure-ASCII path. Audio is uploaded as bytes rather than by path, so a non-ASCII workspace is fine in server mode; in CLI mode the `-f` WAV path hits the same bug.

## Verify the VAD

Against the Silero model that whisper.cpp's own ecosystem pins (`silero_vad.onnx`), at threshold `0.30`:

| Signal | Max probability | Verdict |
| --- | --- | --- |
| Digital silence | 0.043 | rejected |
| Engine noise (broadband + 55 Hz rumble) | 0.102 | rejected |
| Low rumble (pure 50 Hz) | 0.001 | rejected |
| Whistle (pure 3 kHz) | 0.001 | rejected |
| Real speech | mean 0.677, 69% of windows ≥ 0.30 | detected |

Reproduce it with `node scripts/silero-check.mjs <silero_vad.onnx> <speech.wav>`.

## Limitations

1. **The fallback VAD is not Silero.** Without ONNX Runtime and a model, the built-in band-limited energy VAD runs instead; the result reports `vadEngine: heuristic` and warns. It removes silence and low rumble, but **keeps broadband noise and tonal whistles** — on the same noisy recording it kept a 3 kHz whistle as speech where Silero rejected it. Install the optional dependency for the numbers above.
2. **whisper.cpp is not bundled.** The plugin calls it; you install it. The engine-missing path is a degradation with guidance, not a failure.
3. **Scratch space lives in the session workspace** (`<session cwd>/.dsh-av-continuous/`), not the system temp directory: DSH's file sandbox only grants the workspace write access, and ffmpeg is a child process. Frames become attachments and the directory is removed immediately.
4. **Frames cost context.** Every frame is a real image block. The attachment service caps the bytes one message may carry; when the budget is reached the plugin stops early and reports how many frames it dropped.
5. **Code changes need a remount.** `shim.js` is a byte-stable entry that content-hashes `dist/bundle.js`, so a rebuild is picked up on the next remount. Changing `shim.js` itself or the `inject` list needs a DSH restart.

## Development

```sh
pnpm install
pnpm build       # tsc -> dist/*.js (types + tests) and esbuild -> dist/bundle.js (runtime)
pnpm test        # 99 unit tests; no ffmpeg / whisper / ONNX required
pnpm verify      # build + test
```

End-to-end checks need the real engines:

```sh
node scripts/e2e.mjs <out-dir>                                  # frame sampling + audio + shipped entry
node scripts/silero-check.mjs <silero_vad.onnx> <speech.wav>     # per-class VAD table
node scripts/tool-smoke.mjs <silero_vad.onnx|none> <audio> [silero|heuristic]
```

`tool-smoke.mjs` deliberately runs one tool call per process.

## Layout

```
shim.js            byte-stable entry; loads dist/bundle.js through ?v=<sha256>
cordis.patch.yml   bundle patch: inserts one row into the profile
src/impl.ts        pure logic: frame planning, parsers, argv builders, VAD, timeline
src/wav.ts         pure logic: dependency-free RIFF/WAVE decode + resampling
src/define-tool.ts the defineTool contract, reimplemented locally (see below)
src/runtime.ts     processes, engine discovery, ffmpeg/whisper/ONNX calls, scratch
src/tools.ts       the two tool definitions, canonical values and renderers
src/index.ts       plugin entry: name / inject / apply / ctx.effect
dist/bundle.js     single-file runtime build (esbuild)
```

### Why `main` is `shim.js` and not the built entry

DSH pins a plugin's module URL for the lifetime of the process, so a rebuilt entry loaded from the same path keeps executing the **cached old module** — a real problem this plugin was bitten by. `shim.js` is byte-stable and imports `dist/bundle.js?v=<sha256>`, so changed content yields a new URL and therefore fresh code. Making `main` point straight at the build output would reintroduce that bug, which is why it does not.

### Why no `@deepseek-ai/*` imports

The Harness bundles `@deepseek-ai/dsh-tools@0.2.0-rc.2`, while npm's copy of that name is `0.0.1-rc.1` — older and different. A third-party plugin resolves those names from the **profile's** `node_modules`, so a static import would resolve to the stale copy or to nothing, and the plugin would fail to mount for reasons unrelated to its own code. This plugin therefore declares **zero `@deepseek-ai/*` dependencies** and reimplements the `defineTool` contract locally, calling `ctx.tools.register(...)` exactly as a first-party tool plugin does.

## Privacy

ffmpeg only reads and writes local files, whisper.cpp is a local binary, Silero is local ONNX inference. There are no network requests, no telemetry, and no API keys.

## License

MIT — see [LICENSE](LICENSE).
