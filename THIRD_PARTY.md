# 第三方技能来源

以下目录完整取自 https://github.com/qqq236484707-maker/skills ，固定提交 dbd4588f9e1033efb41dad4bef2f7947c8993d44：

- `.agents/skills/theme-factory/` ← `skills/theme-factory/`
- `.agents/skills/slack-gif-creator/` ← `skills/slack-gif-creator/`

保留各目录 LICENSE.txt（Apache License 2.0）。上游目录内容未修改，仅更换安装位置。上游仓库的 THIRD_PARTY_NOTICES.md 随本文件所在目录保存为 UPSTREAM_THIRD_PARTY_NOTICES.md。

`medical-teaching`、AGENTS.md、README.md、依赖列表为本项目新增，不是上游专有文档技能的复制品。

## 新增科研技能

- 上游：https://github.com/K-Dense-AI/scientific-agent-skills
- 固定提交：593377bb048752abb0152deab9fbb1083a6087df
- `skills/paper-lookup/`、`skills/citation-management/`、`skills/literature-review/`、`skills/scientific-visualization/` 分别复制到 `.agents/skills/` 下同名目录。
- 保留上游文件，另在各目录附上根目录 LICENSE.md（MIT，Copyright (c) 2025 K-Dense Inc.）。

- 上游：https://github.com/openai/skills
- 固定提交：49f948faa9258a0c61caceaf225e179651397431
- `skills/.curated/pdf/` 完整复制到 `.agents/skills/pdf/`。
- 保留该目录 LICENSE.txt（Apache-2.0）。

集成说明位于 AGENTS.md 和 README.md；未将上游服务或 API 凭据包含在仓库中。

## 2026-10-25 新增视觉技能

源仓库与固定提交同首节。完整复制 canvas-design、algorithmic-art、brand-guidelines 到 .agents/skills/ 同名目录，保留 LICENSE.txt、模板、字体与字体许可；上游文件未修改。额外项目调用限制见 AGENTS.md。现有 UPSTREAM_THIRD_PARTY_NOTICES.md 与本次源提交一致。未复制专有 pptx/docx。
