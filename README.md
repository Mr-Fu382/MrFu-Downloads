import os
from urllib.parse import quote
from collections import defaultdict

# 你的下载域名
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"
# 你的 GitHub 仓库地址（用于反馈链接）
GITHUB_REPO_URL = "https://github.com/Mr-Fu382/public-assets"

ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

def main():
    if not os.path.exists("all_files.txt"):
        print("未找到 all_files.txt，退出。")
        return

    with open("all_files.txt", "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        print("R2 中暂无文件，退出。")
        return

    # 按第一层项目分组
    projects = defaultdict(list)
    for file in files:
        parts = file.split("/")
        if len(parts) > 1:
            projects[parts[0]].append(file)
        else:
            projects["其他"].append(file)

    # 1. 生成根目录导航 README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 公开资产下载中心\n\n")
        f.write(f"> 最后同步时间: {os.popen('date').read().strip()}\n\n")
        f.write("## 📂 项目分类导航\n\n")
        for proj in projects:
            proj_encoded = quote(proj)
            f.write(f"- [{proj}](./{proj_encoded}/README.md)\n")
        
        # 根目录的反馈入口
        f.write("\n---\n")
        f.write("### 💬 反馈与支持\n")
        f.write(f"- 遇到 Bug 或想提建议？请前往 [**GitHub Issues**]({GITHUB_REPO_URL}/issues) 提交反馈。\n")
        f.write(f"- 想和大家交流心得？请前往 [**GitHub Discussions**]({GITHUB_REPO_URL}/discussions) 参与讨论。\n")
    print("✅ 根目录导航 README.md 已更新。")

    # 2. 遍历每个项目，生成对应的表格
    for proj_name, proj_files in projects.items():
        print(f"正在处理项目: {proj_name}")
        
        plugin_data = defaultdict(lambda: defaultdict(dict))

        for file_path in proj_files:
            parts = file_path.split("/")
            
            if len(parts) >= 4:
                plugin_name = parts[1]
                version = parts[2]
                filename = parts[3]

                if filename.lower().endswith(ARCHIVE_EXTS):
                    plugin_data[plugin_name][version]['file'] = file_path
                else:
                    try:
                        # 读取说明文件内容
                        raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                        if raw_content:
                            clean_desc = raw_content.replace("\n", " ").replace("\r", "").replace("|", "/")
                            if len(clean_desc) > 500:
                                clean_desc = clean_desc[:500] + "..."
                            plugin_data[plugin_name][version]['desc'] = clean_desc
                    except Exception:
                        pass

        # 组装 Markdown 表格
        md_lines = []
        md_lines.append(f"# {proj_name} 下载列表\n")
        md_lines.append(f"> 最后同步时间: {os.popen('date').read().strip()}\n")
        md_lines.append("| 插件名称 | 版本 | 下载链接 (明文) | 说明 |")
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
                    full_url = f"{BASE_DOWNLOAD_URL}{encoded_zip}"
                    if len(sorted_versions) > 1:
                        download_list.append(f"**{v}**: {full_url}")
                    else:
                        download_list.append(full_url)
                else:
                    download_list.append("-")
                    
                if 'desc' in info and info['desc']:
                    desc_list.append(f"**{v}**: {info['desc']}")
                else:
                    desc_list.append("-")

            download_joined = " <br> ".join(download_list)
            desc_joined = " <br> ".join(desc_list)
            row = f"| {plugin_name} | {', '.join(version_list)} | {download_joined} | {desc_joined} |"
            md_lines.append(row)

        # 子目录的反馈入口
        md_lines.append("\n---")
        md_lines.append("### 🐞 问题反馈")
        md_lines.append(f"如果你在使用 **{proj_name}** 中的任何插件时遇到问题，请点击下方链接提交反馈：")
        md_lines.append(f"👉 [**前往 GitHub Issues 提交问题**]({GITHUB_REPO_URL}/issues)")

        # 写入项目目录
        os.makedirs(proj_name, exist_ok=True)
        with open(f"{proj_name}/README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ {proj_name} 表格已生成。")

    print("🎉 所有项目处理完毕！")

if __name__ == "__main__":
    main()
