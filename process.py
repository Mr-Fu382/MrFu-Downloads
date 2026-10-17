import os
import json
import requests
from urllib.parse import quote
from collections import defaultdict

# 从 GitHub Secrets 获取 Key
api_key = os.environ.get("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com/chat/completions"
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"

# 1. 读取 rclone 抓取的文件列表
with open("all_files.txt", "r", encoding="utf-8") as f:
    files = [line.strip() for line in f if line.strip()]

if not files:
    print("R2 里没有文件，退出。")
    exit(0)

# 2. 按第一层项目分组
projects = defaultdict(list)
for file in files:
    parts = file.split("/")
    if len(parts) > 1:
        projects[parts[0]].append(file)
    else:
        projects["其他"].append(file)

# 3. 生成根目录的总导航 README
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# 公开资产下载中心\n\n")
    f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
    f.write("## 📂 项目分类导航\n\n")
    for proj in projects:
        proj_encoded = quote(proj)
        f.write(f"- [{proj}](./{proj_encoded}/README.md)\n")

print("根目录 README.md 已更新。")

# 4. 按项目循环，调用 DeepSeek 生成每个项目的合并表格
for proj_name, proj_files in projects.items():
    print(f"正在处理项目: {proj_name}")
    
    # 针对你的结构优化后的提示词
    prompt = f"""
    你是一个软件仓库管理助手。现在有项目【{proj_name}】下的以下文件列表（包含不同插件的不同版本）：
    {json.dumps(proj_files, ensure_ascii=False, indent=2)}
    
    文件路径结构为：项目名/插件名/版本文件夹/文件.zip或说明。
    请你按以下规则生成 Markdown 表格：
    1. 识别属于同一个插件（比如“插件1”）的所有不同版本（比如“插件文件1.0.0”、“插件文件2.0.0”）。
    2. 将同一个插件的不同版本合并展示在同一行。
    3. 表格列必须为：`插件名称`、`版本`、`下载链接`、`说明文档`。
    4. “版本”列列出该插件的所有版本号（用逗号隔开）。
    5. “下载链接”列请为每个版本生成带链接的 Markdown，格式为：`[版本号]({BASE_DOWNLOAD_URL} + 原始的.zip文件完整路径)`。
    6. “说明文档”列也请为每个版本生成链接，指向对应的“说明”文件。
    7. 只输出纯 Markdown 表格，不要有任何解释文字。
    
    示例输出：
    | 插件名称 | 版本 | 下载链接 | 说明文档 |
    | :--- | :--- | :--- | :--- |
    | 插件1 | 1.0.0, 2.0.0 | [1.0.0]({BASE_DOWNLOAD_URL}1项目/插件1/插件文件1.0.0/插件文件.zip), [2.0.0]({BASE_DOWNLOAD_URL}1项目/插件1/插件文件2.0.0/插件文件.zip) | [1.0.0说明]({BASE_DOWNLOAD_URL}1项目/插件1/插件文件1.0.0/说明), [2.0.0说明]({BASE_DOWNLOAD_URL}1项目/插件1/插件文件2.0.0/说明) |
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # 依然是轻量便宜版，放心用
        "messages": [
            {"role": "system", "content": "你是一个无情的表格生成机器，只输出纯 Markdown 表格，禁止包含解释性文字。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    response = requests.post(base_url, headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"请求失败: {response.text}")
        continue
        
    result = response.json()["choices"][0]["message"]["content"]
    
    # 创建对应的项目文件夹，并写入 README.md
    proj_dir = proj_name
    os.makedirs(proj_dir, exist_ok=True)
    with open(f"{proj_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(f"# {proj_name} 下载列表\n\n")
        f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
        f.write(result)

print("所有项目处理完毕！")
