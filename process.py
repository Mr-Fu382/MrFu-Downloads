import os
import re
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

# 4. 遍历每个项目，用纯 Python 逻辑生成表格
for proj_name, proj_files in projects.items():
    print(f"正在处理项目: {proj_name}")
    
    # 数据结构：{ '插件名': { '1.0.0': { 'zip': '路径', 'desc': '说明内容' } } }
    plugin_data = defaultdict(lambda: defaultdict(dict))
    
    for file_path in proj_files:
        # 按 / 分割，预计格式：项目/插件/版本/文件
        parts = file_path.split("/")
        if len(parts) >= 4:
            plugin_name = parts[1]
            version = parts[2]
            filename = parts[3]
            
            # 判断是否为压缩包
            if filename.lower().endswith(('.zip', '.7z', '.rar', '.tar.gz', '.tar')):
                plugin_data[plugin_name][version]['zip'] = file_path
            else:
                # 不是压缩包，就当做说明文件，读取其内容
                try:
                    # rclone cat 读取内容
                    raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                    if raw_content:
                        # 清除换行符，防止表格崩塌
                        clean_desc = raw_content.replace("\n", " ").replace("\r", "").strip()
                        # 转义表格分隔符竖线，防止排版错位
                        clean_desc = clean_desc.replace("|", "/")
                        # 截断过长的说明（最多80个字符，保持表格美观）
                        if len(clean_desc) > 80:
                            clean_desc = clean_desc[:80] + "..."
                        plugin_data[plugin_name][version]['desc'] = clean_desc
                except Exception as e:
                    print(f"读取说明失败: {file_path}, 错误: {e}")
        else:
            # 不符合层级的文件，放到“其他”分类
            pass

    # 开始生成项目 README 内容
    md_lines = []
    md_lines.append(f"# {proj_name} 下载列表\n")
    md_lines.append(f"> 最后同步时间: {os.popen('date').read().strip()}\n")
    md_lines.append("| 插件名称 | 版本 | 下载链接 | 说明 |")
    md_lines.append("| :--- | :--- | :--- | :--- |")
    
    for plugin_name, versions in plugin_data.items():
        # 按版本号排序（尝试按字典序，如果需要严格版本排序可另写逻辑）
        sorted_versions = sorted(versions.keys())
        
        version_list = []
        download_list = []
        desc_list = []
        
        for v in sorted_versions:
            info = versions[v]
            # 1. 版本号拼接
            version_list.append(v)
            
            # 2. 下载链接拼接
            if 'zip' in info:
                encoded_zip = info['zip'].replace(" ", "%20")
                download_list.append(f"[{v}]({BASE_DOWNLOAD_URL}{encoded_zip})")
            else:
                download_list.append("-")
                
            # 3. 说明拼接（不同版本的说明按顺序对应）
            if 'desc' in info and info['desc']:
                desc_list.append(f"`{v}` {info['desc']}")
            else:
                desc_list.append("-")
        
        # 组装成一行表格
        row = f"| {plugin_name} | {', '.join(version_list)} | {', '.join(download_list)} | {'<br>'.join(desc_list)} |"
        md_lines.append(row)
    
    # 写入项目文件夹的 README.md
    proj_dir = proj_name
    os.makedirs(proj_dir, exist_ok=True)
    with open(f"{proj_dir}/README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

print("所有项目处理完毕！")
