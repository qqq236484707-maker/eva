# Eva 医学课件技能

在 Codex 中打开本仓库并开始新任务，可直接说：

> 使用 $medical-teaching，根据我提供的资料制作 AKI/CRRT 90 分钟中文实习生课件，AKI、置管、CRRT 均衡；先整理证据与逐页内容，再生成详细、可编辑的 PPT，并检查每页版式。

其他示例：
- 使用 $medical-teaching，修订已有 ECMO 课件，先核验来源，不改变已确认的课程结构。
- 使用 $medical-teaching，制作 GCP 伦理培训逐页稿，先核验适用法规版本。
- 使用 $theme-factory 为课件选择统一主题。
- 使用 $slack-gif-creator 制作供 PPT 使用的流程 GIF，调整为课堂可读尺寸，并基于我提供的已核验示意图。

若客户端未自动发现技能，请让它先读取根目录 AGENTS.md 和对应 SKILL.md。此配置属于本仓库，不会自动安装到其他项目或所有 ChatGPT 会话。

## 已安装

| 技能 | 来源 | 范围 |
|---|---|---|
| medical-teaching | 本项目原创 | 资料整理、循证核对、逐页稿、PPT/Word/表格生成和质量检查流程 |
| theme-factory | qqq236484707-maker/skills | 10 套主题、展示 PDF、Apache-2.0 许可 |
| slack-gif-creator | qqq236484707-maker/skills | GIF 工具、动画说明和依赖，Apache-2.0 许可 |

第三方固定版本：dbd4588f9e1033efb41dad4bef2f7947c8993d44。见 THIRD_PARTY.md。

原仓库的 pptx/pdf/docx/xlsx 专有技能未复制；doc-coauthoring 未确认独立授权，未复制。medical-teaching 是项目新增工作流，不宣称等同于这些技能。未安装与课件主流程无直接关系的艺术、网页开发技能。

## 运行依赖

阅读技能、大纲和写作无需额外软件包。实际生成文件优先使用 Codex 环境已有工具。若采用 Python 后端，可让 Codex 在虚拟环境中执行：

```bash
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
python -m pip install -r tools/requirements-teaching.txt
# 只有生成 GIF 时需要
python -m pip install -r .agents/skills/slack-gif-creator/requirements.txt
```

Windows PowerShell 激活命令：`.venv\Scripts\Activate.ps1`。
PDF/逐页预览另需 LibreOffice、Poppler 和可用中文字体；扫描件 OCR 还需 OCR 引擎及中文语言包。依赖没有自动安装到你的电脑或 Codex 云端环境；缺少时由执行任务的 Codex 检查并说明。

本次安装验证技能结构及 GIF 最小生成，不代表完成了医学课件、医学审校或你的云端环境端到端测试。

## 文件与隐私

建议每门课独立目录，保存 outline.md、slide-content.md、sources.md 和生成脚本。output/ 默认不提交。当前仓库公开，请勿上传真实患者资料或院内保密文件；个人课件资料需要另行确认可公开范围。
