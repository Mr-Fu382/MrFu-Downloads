import os
from urllib.parse import quote
from collections import defaultdict

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

# 定义所有可作为“实体包”的扩展名（涵盖 7-Zip 常见格式）
ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

# 4. 遍历每个项目，生成表格
for proj_name, proj_files in projects.items():
    print(f"正在处理项目: {proj_name}")

    plugin_data = defaultdict(lambda: defaultdict(dict))

    for file_path in proj_files:
        parts = file_path.split("/")
        
        # 严格符合 4 层结构：项目 / 插件 / 版本 / 文件
        if len(parts) >= 4:
            plugin_name = parts[1]
            version = parts[2]
            filename = parts[3]

            # 判断是不是包文件（全部转为小写进行匹配）
            if filename.lower().endswith(ARCHIVE_EXTS):
                plugin_data[plugin_name][version]['file'] = file_path
            else:
                # 不是包文件，视为说明文件（建议用 .txt 或 .md）
                try:
                    raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                    if raw_content:
                        clean_desc = raw_content.replace("\n", " ").replace("\r", "").replace("|", "/")
                        if len(clean_desc) > 80:
                            clean_desc = clean_desc[:80] + "..."
                        plugin_data[plugin_name][version]['desc'] = clean_desc
                except:
                    pass

    # 生成项目内部的 Markdown 表格
    md_lines = []
    md_lines.append(f"# {proj_name} 下载列表\n")
    md_lines.append(f"> 最后同步时间: {os.popen('date').read().strip()}\n")
    md_lines.append("| 插件名称 | 版本 | 下载链接 | 说明 |")
    md_lines.append("| :--- | :--- | :--- | :--- |")

    for plugin_name, versions in plugin_data.items():
        sorted_versions = sorted(versions.keys())

        version_list = []
        download_list = []
        desc_list = []

        for v in sorted_versions:
            info = versions[v]
            
            version_list.append(v)
            
            if 'file' in info:
                encoded_zip = info['file'].replace(" ", "%20")
                download_list.append(f"[{v}]({BASE_DOWNLOAD_URL}{encoded_zip})")
            else:
                download_list.append("-")
                
            if 'desc' in info and info['desc']:
                desc_list.append(f"**{v}**: {info['desc']}")
            else:
                desc_list.append("-")

        row = f"| {plugin_name} | {', '.join(version_list)} | {', '.join(download_list)} | {' <br> '.join(desc_list)} |"
        md_lines.append(row)

    # 写入项目专属的 README.md
    proj_dir = proj_name
    os.makedirs(proj_dir, exist_ok=True)
    with open(f"{proj_dir}/README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

print("所有项目处理完毕！")
