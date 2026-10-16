import os
import json
import requests

# 从 GitHub Secrets 获取 DeepSeek Key
api_key = os.environ.get("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com/v1/chat/completions"
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"

# 1. 读取刚才 rclone 抓取的文件列表
with open("all_files.txt", "r", encoding="utf-8") as f:
    files = [line.strip() for line in f if line.strip()]

if not files:
    print("R2 里没有文件，退出。")
    exit(0)

# 2. 提取所有的第一层项目文件夹
projects = set()
for file in files:
    parts = file.split("/")
    if len(parts) > 1:
        projects.add(parts[0])
    else:
        projects.add("其他")

# 3. 为了节省 AI token 且避免超时，我们只把文件名发送给 AI 整合
prompt = f"""
你是一个软件仓库管理助手。现在我有以下文件列表：
{json.dumps(files, ensure_ascii=False, indent=2)}

请你：
1. 识别出属于同一个插件/软件的不同版本。
2. 将它们合并，按“项目分类”输出为 Markdown 表格。
3. 表格必须包含四列：`插件名称`、`文件大小(估算)`、`版本/变体(需带下载链接)`、`备注`。
4. 下载链接的格式必须严格遵守：{BASE_DOWNLOAD_URL} + 原始文件路径。
5. 只输出纯 Markdown 内容，不要包含任何解释性文字。

输出示例：
| 插件名称 | 版本 | 下载链接 | 备注 |
| :--- | :--- | :--- | :--- |
| 某某某插件 | 1.0.0, 1.0.1 | [1.0.0]({BASE_DOWNLOAD_URL}DSH插件/xxx/1.0.0.zip), [1.0.1]({BASE_DOWNLOAD_URL}DSH插件/xxx/1.0.1.zip) | 历史版本 |
"""
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "你是一个专业的仓库索引生成器，请严格按用户要求输出 Markdown 表格。"},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.1
}

print("正在请求 DeepSeek 智能整合...")
response = requests.post(base_url, headers=headers, json=data)
if response.status_code != 200:
    print(f"DeepSeek API 请求失败: {response.text}")
    exit(1)

# 4. 拿到 AI 整合好的内容
ai_output = response.json()["choices"][0]["message"]["content"]

# 5. 将 AI 内容写入各个项目的文件夹里
# 因为 AI 可能混合了所有项目，为了安全，我们统一输出到一个总表，或者让 AI 分项目输出
# 为了简单且完美展示，直接生成到根目录的一个汇总表里（AI 会帮我们排版好）
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# 公开资产下载中心 (AI 智能整合版)\n\n")
    f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
    f.write(ai_output)

# 同时生成各个项目的独立文件（简单版本，确保 AI 幻觉不至于弄丢链接）
for proj in projects:
    proj_files = [f for f in files if f.startswith(proj + "/")]
    if not proj_files: continue
    
    os.makedirs(proj, exist_ok=True)
    with open(f"{proj}/下载列表.md", "w", encoding="utf-8") as f:
        f.write(f"# {proj} 下载列表\n\n")
        f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
        f.write("| 文件路径 | 下载链接 |\n| :--- | :--- |\n")
        for pf in proj_files:
            encoded_file = pf.replace(" ", "%20")
            f.write(f"| {pf} | [点击下载]({BASE_DOWNLOAD_URL}{encoded_file}) |\n")

print("生成完毕！")
