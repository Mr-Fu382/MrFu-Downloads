import os
from urllib.parse import quote
from collections import defaultdict

# ================= ⚠️ 基础配置区 =================
BASE_DOWNLOAD_URL = "https://github-download.1253510.com/"
# 如果你改了仓库名字，记得把这里的 links-hub 替换掉
GITHUB_REPO_URL = "https://github.com/Mr-Fu382/links-hub"

CONTACT_WECHAT = "15976948117; Yq13926922459"
CONTACT_QQ = "3628270735"
CONTACT_EMAIL = "3628270735@qq.com"

# ================= 📢 置顶专属公告 =================
ANNOUNCEMENT_MD = """
> [!TIP]
> ### 👋 欢迎来到 Mr. Fu 的专属宝库 (Welcome to Mr. Fu's Asset Hub)
> 
> 这里是由 **初中生开发者 Mr. Fu** 独立维护的项目分发中心。为了保证极致的下载速度，所有大文件均托管于 **Cloudflare R2 (全球 CDN 加速)**。
> *(This is the official distribution center independently maintained by **Mr. Fu, a junior high school developer**. All large files are hosted on Cloudflare R2 for extreme download speed.)*
> 
> 👇 下方包含我的**原创插件**、**合作项目**以及**第三方软件的汉化作品**，请自由选择下载。
---
"""

# ================= 📜 分发授权与版权协议 =================
LICENSE_DISCLAIMER_MD = """
---
### 📜 分发授权与版权协议 (Distribution Authorization & Copyright)

**【中文】**
本仓库（Mr. Fu's Asset Hub）及其关联的所有项目库内分发的资源，均由作者（Mr. Fu）进行整理、制作与授权分发。**凡从本渠道获取的资源，均需遵守以下协议：**

1. **原创作品版权**：由 Mr. Fu 完全原创的代码、插件及工具，其完整著作权归 Mr. Fu 所有。
2. **汉化及衍生作品版权**：对于基于第三方软件制作的汉化版、修改版或绿色版，**原软件的底层代码版权归原作者所有，但本汉化包内的翻译文本、排版优化、重打包程序及相关分发权利，均归 Mr. Fu 所有。**
3. **严格的非商业限制**：**无论资源属于原创还是汉化，严禁任何人将本仓库分发的任何资源用于商业目的**（包括但不限于倒卖、租赁、捆绑销售、设置付费下载门槛）。
4. **署名权保护**：任何个人或组织在转载、分享或二次分发上述资源时，**必须完整保留 Mr. Fu 及原作者的署名信息与出处链接**，严禁恶意篡改或抹除。
5. **免责与下线机制**：本仓库提供的资源仅限个人学习交流。若任何第三方原作者认为本仓库的汉化分发行为侵犯其权益，请立即联系 Mr. Fu，我们将第一时间无条件下线相关底层代码。

**【English】**
Resources distributed in this repository (Mr. Fu's Asset Hub) and its associated project repositories are organized, created, and distributed by Mr. Fu. **All resources obtained from this channel must comply with the following terms:**

1. **Original Works**: The complete copyright of codes, plugins, and tools entirely created by Mr. Fu belongs to Mr. Fu.
2. **Localizations & Derivative Works**: For localized or modified versions based on third-party software, **the underlying code copyright belongs to the original authors, BUT the translated texts, formatting optimizations, repackaged installers, and distribution rights within this localization package belong to Mr. Fu.**
3. **Strict Non-Commercial Restriction**: **Regardless of whether the resource is original or localized, any commercial use of any resources distributed in this repository is strictly prohibited.**
4. **Attribution Protection**: When redistributing or sharing, you **MUST retain the credits and source links of Mr. Fu and the original authors**. Malicious tampering is prohibited.
5. **Disclaimer & Takedown**: Resources are for personal study only. If any original author believes the distribution infringes their rights, please contact Mr. Fu, and the underlying code will be taken down unconditionally.
"""
# ==================================================================

# 支持的可执行包后缀（全覆盖）
ARCHIVE_EXTS = (
    '.zip', '.7z', '.rar', '.tar', '.gz', '.tgz', '.bz2', '.tbz2', '.xz', '.txz',
    '.zst', '.lz', '.lzma', '.cab', '.iso', '.img', '.wim', '.esd', '.swm', 
    '.dmg', '.msi', '.exe', '.gtz', '.pak', '.arc', '.arj', '.lzh', '.cpio'
)

# 忽略的系统垃圾文件
IGNORE_FILES = ['.DS_Store', 'Thumbs.db', 'desktop.ini']

def generate_contact_md():
    """生成联系方式模块"""
    return f"""### 💬 反馈与联系方式 (Feedback & Contact)

**遇到问题？需要帮助？ (Need help?)**
- 🐞 **提交工单 (Submit Issue)**: [点击前往 GitHub 议题 (Issues)]({GITHUB_REPO_URL}/issues) *(推荐，方便追踪 / Recommended)*
- 💡 **交流讨论 (Discussions)**: [点击前往 GitHub 讨论 (Discussions)]({GITHUB_REPO_URL}/discussions) *(分享心得 / Share ideas)*

**直接联系作者 (Contact Author)：**
- 💬 **微信 (WeChat)**: `{CONTACT_WECHAT}`
- 🐧 **QQ**: `{CONTACT_QQ}`
- 📧 **邮箱 (Email)**: `{CONTACT_EMAIL}`

> *提示 (Note)：初中生课业繁忙，加好友请备注来意。如遇 Bug，请尽量详细描述问题现象或附带截图。*
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

    # 按第一层目录（大类）分组
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
        
        # 数据结构：{ '资源名': { '版本号': { 'files': [ (文件名, 路径), ... ], 'desc': '说明' } } }
        asset_data = defaultdict(lambda: defaultdict(lambda: {'files': [], 'desc': ''}))

        for file_path in proj_files:
            filename = file_path.split("/")[-1]
            
            if filename in IGNORE_FILES or filename.startswith('.'):
                continue
                
            parts = file_path.split("/")
            path_len = len(parts)
            
            # ----- 🧠 智能层级解析引擎 -----
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

            # ----- 📦 文件类型识别与读取说明 -----
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

        # ----- 📝 组装 Markdown 表格 -----
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
                        
                        # 如果同版本有多个文件，用文件名区分并换行；单文件直接显示版本号
                        if len(info['files']) > 1:
                            short_name = fname if len(fname) <= 25 else fname[:22] + "..."
                            v_links.append(f"[{short_name}]({full_url})")
                        else:
                            v_links.append(f"[{v}]({full_url})")
                    
                    if len(sorted_versions) > 1:
                        download_list.append(f"**{v}**:<br>" + "<br>".join(v_links))
                    else:
                        download_list.append("<br>".join(v_links))
                else:
                    download_list.append("-")
                    
                if info['desc']:
                    desc_list.append(f"**{v}**: {info['desc']}")
                else:
                    desc_list.append("-")

            download_joined = " <br><br> ".join(download_list)
            desc_joined = " <br> ".join(desc_list)
            
            row = f"| {asset_name} | {', '.join(version_list)} | {download_joined} | {desc_joined} |"
            md_lines.append(row)

        # 底部信息 + 协议
        md_lines.append("\n---\n")
        md_lines.append(generate_contact_md())
        md_lines.append(LICENSE_DISCLAIMER_MD)

        # 写入文件
        os.makedirs(proj_name, exist_ok=True)
        with open(f"{proj_name}/README.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"✅ {proj_name} 表格已生成。")

    print("🎉 所有资产处理完毕！")

if __name__ == "__main__":
    main()
