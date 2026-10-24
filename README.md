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

各来源固定版本见 THIRD_PARTY.md。

原仓库的 pptx/pdf/docx/xlsx 专有技能未复制；doc-coauthoring 未确认独立授权，未复制。medical-teaching 是项目新增工作流，不宣称等同于这些技能。未安装与课件主流程无直接关系的艺术、网页开发技能。

## 新增五个科研技能

均位于 `.agents/skills/`，已保留脚本、参考资料、资产和许可。

| 技能 | 适用场景 | 额外依赖 |
|---|---|---|
| paper-lookup | AKI/CRRT、ECMO 的 PubMed 等文献检索，记录检索来源 | Python 3.11+、curl、联网；部分服务的密钥按需配置 |
| citation-management | 核对 DOI/PMID、作者和年份，整理参考文献与 BibTeX | Python、requests；Google Scholar 路径另需 scholarly |
| literature-review | 证据表、文献筛选、主题综述和研究局限 | Python、requests；自带 PDF 导出另需 Pandoc/XeLaTeX；可选 AI 图需 OpenRouter |
| scientific-visualization | 原始数据图、误差与缺失值表达、课堂配色和导出检查 | Python 3.11+；按任务安装 Matplotlib/Seaborn/Plotly；Kaleido 静态导出需 Chrome |
| pdf | 指南 PDF 提取、讲义输出、页面渲染与版式检查 | reportlab、pdfplumber、pypdf、Poppler；中文字体 |

这五个来自 K-Dense 和 OpenAI，不是原始 skills 仓库中的同名专有技能。

### 建议组合

1. medical-teaching 明确受众、课时、教学目标；pdf 提取用户资料。
2. paper-lookup 检索并保存检索式、日期、数据库和文献标识。
3. citation-management 核验元数据；literature-review 整理证据表、分歧和局限。
4. medical-teaching 编写逐页标题、正文、讲稿与来源；GCP 同时核验官方法规。
5. scientific-visualization 根据真实数据制图，theme-factory 统一风格；需要时生成 GIF。
6. 使用环境已有 PPT 工具或 python-pptx 生成可编辑 PPT，导出 PDF 后用 pdf 逐页检查。

可直接发送：

> 使用本仓库技能制作 AKI/CRRT 教学课件。先用 paper-lookup、citation-management 和 literature-review 整理证据，再用 medical-teaching 编写逐页稿，scientific-visualization 制图，生成可编辑 PPT 并导出 PDF 检查。缺少依赖时先说明；不调用付费 API。

新增技能提供工作流和脚本；不自动完成医学审校，也不保证系统综述穷尽性。它们不会替代 PPT 生成后端。

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

科研绘图与 PDF 的常用 Python 依赖可按需安装：

```bash
python -m pip install -r tools/requirements-research.txt
```

该列表不包含可选的 scholarly、Plotly/Kaleido、Parallel、OpenRouter，亦不安装系统级 Poppler、Pandoc、XeLaTeX、Chrome 或中文字体。新增 Python 脚本通过语法检查，检索解析、BibTeX 格式化和图表导出规划的命令入口检查通过。综述引用检查入口因本次环境缺少 requests 未通过，需先安装上述依赖。未进行在线数据库、付费服务或完整课件端到端测试。
