import os
from urllib.parse import quote
from collections import defaultdict

# 你的下载域名前缀
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"

# 支持的所有压缩包/镜像格式（7-Zip 常见格式）
ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

def main():
    # 1. 读取抓取的文件列表
    if not os.path.exists("all_files.txt"):
        print("未找到 all_files.txt，退出。")
        return

    with open("all_files.txt", "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        print("R2 中暂无文件，退出。")
        return

    # 2. 按第一层项目分组
    projects = defaultdict(list)
    for file in files:
        parts = file.split("/")
        if len(parts) > 1:
            projects[parts[0]].append(file)
        else:
            projects["其他"].append(file)

    # 3. 生成根目录导航 README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 公开资产下载中心\n\n")
        f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
        f.write("## 📂 项目分类导航\n\n")
        for proj in projects:
            proj_encoded = quote(proj)
            f.write(f"- [{proj}](./{proj_encoded}/README.md)\n")
    print("✅ 根目录导航 README.md 已更新。")

    # 4. 遍历每个项目，生成对应的表格
    for proj_name, proj_files in projects.items():
        print(f"正在处理项目: {proj_name}")
        
        # 数据结构：{ 插件名: { 版本号: { 'file': 压缩包路径, 'desc': 说明文本 } } }
        plugin_data = defaultdict(lambda: defaultdict(dict))

        for file_path in proj_files:
            parts = file_path.split("/")
            
            # 严格解析 4 层结构：项目 / 插件 / 版本 / 文件
            if len(parts) >= 4:
                plugin_name = parts[1]
                version = parts[2]
                filename = parts[3]

                # 判断是否为压缩包
                if filename.lower().endswith(ARCHIVE_EXTS):
                    plugin_data[plugin_name][version]['file'] = file_path
                else:
                    # 识别为说明文件，读取内容
                    try:
                        raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                        if raw_content:
                            # 替换换行符和竖线，防止 Markdown 表格崩塌
                            clean_desc = raw_content.replace("\n", " ").replace("\r", "").replace("|", "/")
                            # 放宽到 500 字符
                            if len(clean_desc) > 500:
                                clean_desc = clean_desc[:500] + "..."
                            plugin_data[plugin_name][version]['desc'] = clean_desc
                    except Exception as e:
                        print(f"  [警告] 读取说明失败: {file_path}")

        # 5. 组装 Markdown 表格
        md_lines = []
        md_lines.append(f"# {proj_name} 下载列表\n")
        md_lines.append(f"> 最后同步时间: {os.popen('date').read().strip()}\n")
        md_lines.append("| 插件名称 | 版本 | 下载链接 | 说明 |")
        md_lines.append("| :--- | :--- | :--- | :--- |")

        for plugin_name, versions in plugin_data.items():
            # 按版本号排序
            sorted_versions = sorted(versions.keys())
            
            version_list = []
            download_list = []
            desc_list = []

            for v in sorted_versions:
                info = versions[v]
                
                # 版本号
                version_list.append(v)
                
                # 下载链接
                if 'file' in info:
                    encoded_zip = info['file'].replace(" ", "%20")
                    download_list.append(f"[{v}]({BASE_DOWNLOAD_URL}{encoded_zip})")
                else:
                    download_list.append("-")
                    
                # 说明（带版本号标注，用 <br> 换行，保证对应关系）
                if 'desc' in info and info['desc']:
                    desc_list.append(f"**{v}**: {info['desc']}")
                else:
                    desc_list.append("-")

            # 组装成一行
            row = f"| {plugin_name} | {', '.join(version_list)} | {', '.join(download_list)} | {' <br> '.join(desc_list)} |"
            md_lines.append(row)

        # 6. 写入项目目录
        os.makedirs(proj_name, exist_ok=True)
        with open(f"{proj_name}/README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ {proj_name} 表格已生成。")

    print("🎉 所有项目处理完毕！")

if __name__ == "__main__":
    main()
