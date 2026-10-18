import os
from urllib.parse import quote
from collections import defaultdict

BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"
GITHUB_REPO_URL = "https://github.com/Mr-Fu382/links-hub"

CONTACT_WECHAT = "15976948117; Yq13926922459"
CONTACT_QQ = "3628270735"
CONTACT_EMAIL = "3628270735@qq.com"

ANNOUNCEMENT_MD = """
> [!TIP]
> ### 🌟 欢迎来到公开资产下载中心 (Welcome to the Download Center)
> 
> 这里是所有插件、汉化包及其他资源的官方唯一分发渠道。为了保证极致的下载速度，所有文件均托管于 **Cloudflare R2 (全球 CDN 加速)**。
> *(This is the official distribution channel for all plugins, localizations, and other resources. All files are hosted on Cloudflare R2 for extreme download speed.)*
---
"""

ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

def generate_contact_md():
    return f"""### 💬 反馈与联系方式 (Feedback & Contact)

**遇到问题？需要帮助？ (Need help?)**
- 🐞 **提交工单 (Submit Issue)**: [点击前往 GitHub 议题 (Issues)]({GITHUB_REPO_URL}/issues) *(推荐，方便追踪 / Recommended)*
- 💡 **交流讨论 (Discussions)**: [点击前往 GitHub 讨论 (Discussions)]({GITHUB_REPO_URL}/discussions) *(分享心得 / Share ideas)*

**直接联系作者 (Contact Author)：**
- 💬 **微信 (WeChat)**: `{CONTACT_WECHAT}`
- 🐧 **QQ**: `{CONTACT_QQ}`
- 📧 **邮箱 (Email)**: `{CONTACT_EMAIL}`

> *提示 (Note)：加好友请备注来意。如遇 Bug，请尽量详细描述问题现象或附带截图。*
"""

def main():
    if not os.path.exists("all_files.txt"):
        print("未找到 all_files.txt，退出。")
        return

    with open("all_files.txt", "r", encoding="utf-8") as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        print("R2 中暂无文件，退出。")
        return

    projects = defaultdict(list)
    for file in files:
        parts = file.split("/")
        if len(parts) > 1:
            projects[parts[0]].append(file)
        else:
            projects["其他/Others"].append(file)

    # 1. 生成根目录总览
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(ANNOUNCEMENT_MD)
        f.write("# 公开资产下载中心 (Public Asset Download Center)\n\n")
        f.write(f"> 最后同步时间 (Last Sync Time): {os.popen('date').read().strip()}\n\n")
        f.write(generate_contact_md())
        f.write("\n---\n\n## 📂 分类导航 (Project Navigation)\n\n")
        for proj in projects:
            proj_encoded = quote(proj)
            f.write(f"- [{proj}](./{proj_encoded}/README.md)\n")
            
    print("✅ 根目录导航 README.md 已更新。")

    # 2. 遍历每个大类（如 DSH插件、汉化作品），生成各自的表格
    for proj_name, proj_files in projects.items():
        print(f"正在处理分类: {proj_name}")
        
        # asset_data 替代之前的 plugin_data
        asset_data = defaultdict(lambda: defaultdict(dict))

        for file_path in proj_files:
            parts = file_path.split("/")
            path_len = len(parts)
            
            # 智能解析任意层级
            if path_len >= 3:
                filename = parts[-1]
                version = parts[-2]
                
                # 中间层拼起来当资源名
                if path_len > 3:
                    asset_name = " / ".join(parts[1:-2])
                else:
                    asset_name = parts[0]
            elif path_len == 2:
                filename = parts[-1]
                version = "默认(Default)"
                asset_name = parts[0]
            else:
                continue

            # 判断是否压缩包
            if filename.lower().endswith(ARCHIVE_EXTS):
                asset_data[asset_name][version]['file'] = file_path
            else:
                try:
                    raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                    if raw_content:
                        clean_desc = raw_content.replace("\n", " ").replace("\r", "").replace("|", "/")
                        if len(clean_desc) > 500:
                            clean_desc = clean_desc[:500] + "..."
                        asset_data[asset_name][version]['desc'] = clean_desc
                except Exception:
                    pass

        # 组装当前分类的 Markdown
        md_lines = []
        md_lines.append(ANNOUNCEMENT_MD)
        md_lines.append(f"# {proj_name} 下载列表 (Download List)\n")
        md_lines.append(f"> 最后同步时间 (Last Sync Time): {os.popen('date').read().strip()}\n\n")
        
        # ⚠️ 表头大改版，彻底通用化！
        md_lines.append("| 资源名称 (Resource Name) | 版本 (Version) | 下载链接 (Download) | 说明 (Description) |")
        md_lines.append("| :--- | :--- | :--- | :--- |")

        for asset_name, versions in asset_data.items():
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
            row = f"| {asset_name} | {', '.join(version_list)} | {download_joined} | {desc_joined} |"
            md_lines.append(row)

        md_lines.append("\n---\n")
        md_lines.append(generate_contact_md())

        os.makedirs(proj_name, exist_ok=True)
        with open(f"{proj_name}/README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ {proj_name} 表格已生成。")

    print("🎉 所有资产处理完毕！")

if __name__ == "__main__":
    main()
