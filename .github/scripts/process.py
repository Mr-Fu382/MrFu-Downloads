import os
from urllib.parse import quote
from collections import defaultdict

# ================= ⚠️ 基础配置区 =================
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"
GITHUB_REPO_URL = "https://github.com/Mr-Fu382/links-hub"

CONTACT_WECHAT = "15976948117; Yq13926922459"
CONTACT_QQ = "3628270735"
CONTACT_EMAIL = "3628270735@qq.com"

# ================= 📢 置顶欢迎公告 =================
ANNOUNCEMENT_MD = """
> [!TIP]
> ### 🌟 欢迎来到公开资产下载中心 (Welcome to the Download Center)
> 
> 这里是本项目的**官方展示与核心分发中心**。为了保证极致的下载速度，所有大文件均托管于 **Cloudflare R2 (全球 CDN 加速)**。此外，部分插件也会同步发布至 npm、GitHub Releases 等其他平台，请根据您的网络环境自由选择。
> *(This is the **official showcase and core distribution center** for this project. For extreme download speeds, all large files are hosted on **Cloudflare R2 (Global CDN)**. Additionally, some plugins are also distributed via platforms like npm and GitHub Releases. Please choose based on your network environment.)*
---
"""

# ================= 📜 版权与免责声明 =================
LICENSE_DISCLAIMER_MD = """
---
### 📜 版权与免责声明 (Copyright & Disclaimer)

**【中文】**
本仓库（Links-Hub）包含两类完全不同的资源，请仔细区分：

1. **由 Mr. Fu 原创的插件/工具**：版权归 Mr. Fu 所有。**严禁任何形式的商业倒卖、租赁或售卖**。转载或分享时必须保留原作者署名。
2. **由 Mr. Fu 汉化的第三方软件**：**原软件的版权完全归其原作者所有**。本仓库仅提供汉化补丁与修改版，使用条件与版权限制**完全以原始项目的 `LICENSE` 为准**。若原作者要求停止分发，我会立即无条件下线。
3. **免责条款**：所有资源均按“原样”提供。对于下载、安装或使用本仓库资源导致的任何数据丢失、系统损坏或法律纠纷，作者（Mr. Fu）不承担任何责任。请自行做好备份。

**【English】**
This repository (Links-Hub) contains two distinct types of resources:

1. **Original plugins/tools by Mr. Fu**: Copyright belongs to Mr. Fu. **Any commercial reselling or renting is strictly prohibited.** Credits must be retained when redistributed.
2. **Third-party localizations by Mr. Fu**: **Copyright of the original software belongs entirely to its original authors.** Usage terms are strictly governed by the **original project's `LICENSE`**. If the original author requests takedown, it will be removed immediately.
3. **Disclaimer**: All resources are provided "AS IS". The author (Mr. Fu) is NOT liable for any data loss, system damage, or legal disputes caused by using these resources. Please back up your data.
"""
# ==================================================================

ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

IGNORE_FILES = ['.DS_Store', 'Thumbs.db', 'desktop.ini']

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

    # 1. 生成根目录总览 README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(ANNOUNCEMENT_MD)
        f.write("# 公开资产下载中心 (Public Asset Download Center)\n\n")
        f.write(f"> 最后同步时间 (Last Sync Time): {os.popen('date').read().strip()}\n\n")
        f.write(generate_contact_md())
        f.write("\n---\n\n## 📂 分类导航 (Project Navigation)\n\n")
        for proj in projects:
            proj_encoded = quote(proj)
            f.write(f"- [{proj}](./{proj_encoded}/README.md)\n")
        
        f.write(LICENSE_DISCLAIMER_MD)
            
    print("✅ 根目录导航 README.md 已更新。")

    # 2. 遍历每个大类，生成具体的表格
    for proj_name, proj_files in projects.items():
        print(f"正在处理分类: {proj_name}")
        
        asset_data = defaultdict(lambda: defaultdict(lambda: {'files': [], 'desc': ''}))

        for file_path in proj_files:
            filename = file_path.split("/")[-1]
            
            if filename in IGNORE_FILES or filename.startswith('.'):
                continue
                
            parts = file_path.split("/")
            path_len = len(parts)
            
            if path_len >= 3:
                version = parts[-2]
                if path_len > 3:
                    asset_name = " / ".join(parts[1:-2])
                else:
                    asset_name = parts[0]
            elif path_len == 2:
                version = "默认(Default)"
                asset_name = parts[0]
            else:
                continue

            if filename.lower().endswith(ARCHIVE_EXTS):
                asset_data[asset_name][version]['files'].append((filename, file_path))
            else:
                try:
                    raw_content = os.popen(f'rclone cat "r2:public-assets/{file_path}" 2>/dev/null').read().strip()
                    if raw_content:
                        clean_desc = raw_content.replace("\n", " ").replace("\r", "").replace("|", "/")
                        if len(clean_desc) > 300:
                            clean_desc = clean_desc[:300] + "..."
                        if asset_data[asset_name][version]['desc']:
                            asset_data[asset_name][version]['desc'] += f" | {clean_desc}"
                        else:
                            asset_data[asset_name][version]['desc'] = clean_desc
                except Exception:
                    pass

        md_lines = []
        md_lines.append(ANNOUNCEMENT_MD)
        md_lines.append(f"# {proj_name} 下载列表 (Download List)\n")
        md_lines.append(f"> 最后同步时间 (Last Sync Time): {os.popen('date').read().strip()}\n\n")
        
        md_lines.append("| 资源名称 (Resource) | 版本 (Version) | 下载链接 (Download) | 说明 (Description) |")
        md_lines.append("| :--- | :--- | :--- | :--- |")

        for asset_name, versions in asset_data.items():
            sorted_versions = sorted(versions.keys())
            version_list = []
            download_list = []
            desc_list = []

            for v in sorted_versions:
                info = versions[v]
                version_list.append(v)
                
                if info['files']:
                    v_links = []
                    for fname, fpath in info['files']:
                        encoded_path = quote(fpath)
                        full_url = f"{BASE_DOWNLOAD_URL}{encoded_path}"
                        
                        if len(info['files']) > 1:
                            v_links.append(f"[{fname}]({full_url})")
                        else:
                            v_links.append(f"[{v}]({full_url})")
                    
                    if len(sorted_versions) > 1:
                        download_list.append(f"**{v}**: " + " , ".join(v_links))
                    else:
                        download_list.append(" , ".join(v_links))
                else:
                    download_list.append("-")
                    
                if info['desc']:
                    desc_list.append(f"**{v}**: {info['desc']}")
                else:
                    desc_list.append("-")

            download_joined = " <br> ".join(download_list)
            desc_joined = " <br> ".join(desc_list)
            
            row = f"| {asset_name} | {', '.join(version_list)} | {download_joined} | {desc_joined} |"
            md_lines.append(row)

        md_lines.append("\n---\n")
        md_lines.append(generate_contact_md())
        md_lines.append(LICENSE_DISCLAIMER_MD)

        os.makedirs(proj_name, exist_ok=True)
        with open(f"{proj_name}/README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ {proj_name} 表格已生成。")

    print("🎉 所有资产处理完毕！")

if __name__ == "__main__":
    main()
