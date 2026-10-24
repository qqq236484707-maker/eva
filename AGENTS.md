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
