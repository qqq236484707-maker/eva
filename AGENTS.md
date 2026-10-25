# 项目约定

这是医学教学技能与课件工作流仓库。

- 医学 PPT、资料整理、逐页稿或讲义任务，先读取 `.agents/skills/medical-teaching/SKILL.md`。
- 统一视觉时按需读取 `.agents/skills/theme-factory/SKILL.md`。
- GIF 动画任务按需读取 `.agents/skills/slack-gif-creator/SKILL.md`。
- 原有资料和用户最新要求优先；不自动重做课件。
- 输出使用中文，来源可追溯，模拟病例明确标注；不编造医学证据。
- 仓库当前公开：仅提交通用技能、代码和可公开内容，不提交患者信息、密钥或院内资料。
- 外部技能的许可、资源与来源说明必须保留。

## 新增科研技能调用

- 文献检索：读取 `.agents/skills/paper-lookup/SKILL.md`。
- DOI/PMID、引用核验与 BibTeX：读取 `.agents/skills/citation-management/SKILL.md`。
- 多文献证据整理与综述：读取 `.agents/skills/literature-review/SKILL.md`。
- 数据图表、配色与导出检查：读取 `.agents/skills/scientific-visualization/SKILL.md`。
- PDF 提取、生成和逐页渲染：读取 `.agents/skills/pdf/SKILL.md`。
- 医学课件仍由 medical-teaching 组织，按需组合上述技能，不必每次全部运行。
- 上游的 Read/Write/Bash/WebSearch 等名称映射到当前环境等效工具；先检查实际能力。
- 引用的外部辅助技能、服务和推广内容不是本仓库任务的先决条件；不得声称未安装的工具可用。付费 API 调用须有明确授权，核心检索和整理不强制使用 OpenRouter 或 Parallel。
- DOI 存在不等于支持医学结论；页级结论需要核对原文。GCP 法规另核验官方原文与适用地区/版本。

## 成品课件与新增视觉技能（2026-10-25）

- 三套医学课件独立生成：AKI、深静脉穿刺置管、CRRT；继续由 medical-teaching 组织内容与证据。
- 详细型课件以教学信息完整、中文可读、图示准确为先；不套用艺术技能的极简文字要求来删减教学内容。
- canvas-design 仅用于封面、章节视觉或原创静态插图；不得把艺术化构图当作解剖、设备或定量证据。相对字体路径从技能目录解析，中文字体另行检查。
- algorithmic-art 按需用于明确请求的生成艺术或网页演示。医学过程必须依据核验内容另行建模；随机粒子效果不代表真实清除率、血流或剂量。HTML 不是 PPT 内嵌动画，需另行录制/逐帧导出并检查播放。其 CDN/字体需联网，离线教学先打包有许可的资源。
- brand-guidelines 仅在用户明确要求 Anthropic 品牌外观时使用；普通医学课件继续采用用户选定主题/theme-factory，不自动套用该品牌。上游算法演示模板的品牌样式不传播到课件。
- 新增技能完整保留上游说明；上述项目适用范围优先。所有“已预装”声明均需实测，禁止自动覆盖依赖或升级全局环境。
- 源仓库 pptx/docx 的专有 LICENSE 不支持本次直接复制；未安装。继续用现有 requirements-teaching.txt 中 python-pptx/python-docx，或当前宿主已经授权的文档工具。不得声称新技能已补齐原生 PPT 动画或完成成品渲染。
- 使用新增视觉技能前参阅 docs/skill-install-audit-2026-10-25.md。
