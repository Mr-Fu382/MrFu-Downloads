<div align="center">

<img src="OpenBurningSuite/icon.png" width="128px">

# Open Burning Suite (简体中文版)

[![.NET 8.0](https://img.shields.io/badge/.NET-8.0-512BD4?logo=dotnet)](https://dotnet.microsoft.com/)
[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)]()
[![Localization](https://img.shields.io/badge/Localization-Simplified_Chinese-green)]()

**基于官方原版最新源码编译制作 (Based on the latest official source code)**

👉 **[点击这里访问原作者官方仓库 (Original Repository)](https://github.com/marcelofrau/OpenBurningSuite)**

<img src="/Screenshots/Home.png" width="75%">

</div>

---

## 📥 极速下载 (Download Now)

**本汉化版由初中生开发者 Mr. Fu 独立编译制作，托管于 Cloudflare R2 全球极速 CDN。**

> [!IMPORTANT]  
> **如果下方的直链点击没反应、或者下载速度极慢，请立刻点击备用通道！**
> 👉 **[前往本作者的专属下载中心获取备用链接 (Backup Download Center)](https://github.com/Mr-Fu382/links-hub)**

为了方便不同需求的用户，提供了以下两种环境的四个版本，请根据需要选择：

| 类型 | 推荐人群 | 下载链接 |
| :--- | :--- | :--- |
| 🚀 **免安装绿色版 (独立版)**<br>*(自带 .NET 8，解压即用)* | **强烈推荐小白下载**，无需配置任何环境。 | [📦 下载 ZIP](https://github-download.1253510.com/OpenBurningSuite中文版/1.0.0/OpenBurningSuite-Chinese-独立版-自带%20.NET%208.zip) |
| 💿 **安装程序版 (独立版)**<br>*(自带 .NET 8)* | 喜欢“下一步”安装到系统的用户。 | [⬇️ 下载 EXE](https://github-download.1253510.com/OpenBurningSuite中文版/1.0.0/OpenBurningSuite-汉化版-独立版-自带%20.NET%208.exe) |
| 🍃 **免安装绿色版 (依赖版)**<br>*(需自备 .NET 8)* | 追求小体积，且电脑已装运行库的用户。 | [📦 下载 ZIP](https://github-download.1253510.com/OpenBurningSuite中文版/1.0.0/OpenBurningSuite-Chinese-需要%20.NET%208%20Desktop%20Runtime.zip) |
| ⚙️ **安装程序版 (依赖版)**<br>*(需自备 .NET 8)* | 体积最小，但未装运行库会报错。 | [⬇️ 下载 EXE](https://github-download.1253510.com/OpenBurningSuite中文版/1.0.0/OpenBurningSuite-汉化版-需要%20.NET%208%20Desktop%20Runtime.exe) |

> **⚠️ 运行提示：** 如果你下载的版本提示缺少 `.NET`，请前往微软官网下载安装 [.NET 8 Desktop Runtime](https://dotnet.microsoft.com/zh-cn/download/dotnet/8.0)。如遇问题，欢迎前往 **[本作者的专属宝库 (Mr. Fu's Asset Hub)](https://github.com/Mr-Fu382/links-hub)** 提交反馈。

---

## 🔗 开源关联与致谢 (Credits & Relation)

- **原始仓库 (Original Repo)**: [marcelofrau/OpenBurningSuite](https://github.com/marcelofrau/OpenBurningSuite) *(Active Fork)*
- **最初作者 (Original Creator)**: [SvenGDK/OpenBurningSuite](https://github.com/SvenGDK/OpenBurningSuite)
- **汉化与维护 (Localization)**: Mr. Fu

**本项目是基于上述官方开源代码的衍生汉化分支 (Derivative Fork)。** 我们严格遵循原项目的开源精神，仅对用户界面（UI）进行了简体中文本地化，并进行了深度测试。若您想查阅最新功能开发或提交底层代码 Issue，请前往上述**原作者的官方仓库**。

---

## 📖 关于原软件 (About)

**Open Burning Suite** 是一款适用于 **Windows**、**Linux** 和 **macOS** 的免费开源光盘刻录应用程序。你可以通过一个应用完成 CD、DVD、HD DVD 和蓝光光盘的刻录、复制、创建与校验。针对音频、视频、数据和游戏光盘，它提供了分步向导，方便新手快速上手；同时，高级选项也为经验丰富的用户提供了全面的控制权。

在底层，Open Burning Suite 使用原生 **SCSI/MMC 命令**直接与你的光驱通信，因此无需安装任何外部工具。它基于 **.NET 8** 和 **Avalonia UI** 构建，在每个平台上都能提供现代感十足的观感。

---

## ✨ 功能 (Features)

| | 功能 | 亮点 |
|:--:|:--------|:-----------|
| 🔥 | **刻录 (Burn)** | CD-R/RW, DVD±R/RW, DVD-RAM, HD DVD, BD-R/RE, BDXL, M-DISC · TAO/SAO/DAO/RAW 写入模式 · 动态构建 · 多份刻录 · 模拟刻录 · 超刻 · CUE 索引表 |
| 💿 | **读取 (Read)** | 输出 ISO, BIN/CUE, CCD/IMG/SUB, TOC/BIN, NRG, MDF/MDS, IMG, CDI · 原生 2352 字节扇区 · 子通道提取 · 精确音频抓取 · 游戏预设 |
| 🏗 | **构建 (Build)** | ISO 9660, Joliet, UDF, Rock Ridge, HFS+ 文件系统 · El Torito 引导光盘 · VCD/SVCD/XSVCD |
| 🎵 | **音频 (Audio)** | 制作带 CD-TEXT 的音频 CD · 将音频 CD 抓取为 WAV 或 BIN/CUE · 将音乐文件刻录到光盘 · 导入 M3U, PLS, WPL, ASX 播放列表 |
| 🎬 | **视频 (Video)** | DVD-Video 创作 (VIDEO_TS) · 蓝光 BDMV · BDAV 刻录格式 · 蓝光 3D (MVC/SBS/TAB) · 基于 FFmpeg 的转码 |
| ✅ | **校验 (Verify)** | 逐扇区完整性校验 · 光盘与镜像比对 · CRC32, MD5, SHA-1, SHA-256, SHA-512 校验和 |
| 🎮 | **游戏 (Gaming)** | PlayStation 1–5, PSP · GameCube, Wii, Wii U · Dreamcast, Saturn, Mega CD · Xbox, Xbox 360, Xbox One/Series · Neo Geo CD, 3DO, CD-i, PC Engine, Amiga CD32/CDTV, Atari Jaguar CD · LibCrypt, 全区及引导扇区补丁 |
| ⚙️ | **高级 (Advanced)** | 光盘擦除与格式化 (快速/完整) · 弹出/加载托盘 · 封盘 · M-DISC 归档 · 实时光盘可视化 |
| 🔒 | **加密 (Encryption)** | 采用 AES-256-CBC 光盘镜像加密，带密码保护 (.obse 格式) · PS3 光盘解密 (IRD/dkey/hex) |
| 🧙 | **向导 (Wizards)** | 针对音频、视频、数据、游戏、复制和空白/擦除光盘的分步快速入门向导 |

---

## 💽 支持的介质 (Supported Media)

- **CD：** CD-R/RW (74, 80, 90, 99 分钟)
- **DVD：** DVD±R/RW, DVD-R DL, DVD+R DL, DVD-RAM
- **HD DVD：** HD DVD-R/RW/RAM (单层/双层)
- **蓝光：** BD-R/RE (25–128 GB, BDXL)
- **UHD 蓝光：** UHD BD-66, UHD BD-100
- **M-DISC：** DVD, BD-R (单层/双层/三层)

---

## 📄 许可证与汉化声明 (License & Localization)

- **原软件**：基于 **BSD 2-Clause License** 分发。请参阅原始 [`LICENSE`](LICENSE) 获取更多信息。
- **汉化说明**：本仓库提供的汉化文本、排版优化及重打包程序，其相关权利归 **Mr. Fu** 所有。**严禁将本汉化包用于任何商业倒卖。** 若原作者认为本仓库的内容侵犯了其权益，请联系我，我将立即无条件下线。
