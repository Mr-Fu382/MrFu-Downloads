import os
from urllib.parse import quote
from collections import defaultdict

# ================= ⚠️ 基础配置区 =================
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

# ================= 📜 第三方软件汉化与分发通用声明 =================
LICENSE_DISCLAIMER_MD = """
---
### 📜 第三方软件汉化与分发通用声明 (General Declaration for Third-Party Localization)

**【中文】**
1. **版权归属**：本仓库（Links-Hub）分发的部分汉化作品，是对**第三方开源或免费软件**的本地化补丁。**原软件的著作权、商标权及相关知识产权均归其原作者所有。** 本仓库及汉化作者（Mr. Fu）不主张对原软件的任何版权。
2. **汉化声明**：本仓库提供的汉化内容（包括但不限于翻译文本、修改的资源文件、重新打包的安装程序）为汉化作者的无偿劳动成果。如果原作者更新了代码或不同意此类分发，请联系我，我将立即下线相关资源。
3. **禁止商用**：无论原软件采用何种开源协议，**严禁任何人将本仓库分发的汉化包或绿色版用于商业目的**（包括但不限于出售、租赁、捆绑销售、二次倒卖）。
4. **免责条款**：所有资源均按“原样”提供，不附带任何担保。对于因下载、安装或使用本站资源而导致的任何数据丢失、系统损坏、版权纠纷或其他直接/间接损失，本仓库及作者不承担任何法律或连带责任。请在使用前确认您已合法拥有原软件的授权，并做好数据备份。

**【English】**
1. **Copyright Attribution**: Some localized works distributed in this repository (Links-Hub) are localization patches for **third-party open-source or free software**. **The copyright, trademark, and related intellectual property rights of the original software belong to their respective original authors.** This repository and the localizer (Mr. Fu) do not claim any copyright over the original software.
2. **Localization Notice**: The localization content (including but not limited to translated texts, modified resource files, and repackaged installers) provided in this repository is the unpaid work of the localizer. If the original author updates the code or does not agree with this kind of distribution, please contact me, and I will immediately take down the relevant resources.
3. **Non-Commercial**: Regardless of the original software's open-source license, **any commercial use (including but not limited to selling, renting, bundling, or reselling) of the localization packages or green versions distributed in this repository is strictly prohibited.**
4. **Disclaimer**: All resources are provided "AS IS", without warranty of any kind. The repository owner and authors are NOT liable for any data loss, system damage, copyright disputes, or other direct/indirect damages caused by downloading, installing, or using these resources. Please ensure you legally own the license of the original software before use, and back up your data.
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
        
        # 首页底部加上通用声明
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

        # 子页面：联系方式 + 通用声明
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
