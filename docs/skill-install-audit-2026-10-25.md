# 医学教学课件技能安装核对

核对日期：2026-10-25（北京时间）。目标 eva/main 基线 d6ad5e60b549c4307c9664a544af2fca2d64419c；来源 qqq236484707-maker/skills 固定提交 dbd4588f9e1033efb41dad4bef2f7947c8993d44。

已读取现有八项与五个候选的 SKILL.md、项目 AGENTS.md、两份依赖列表及候选许可证。五个候选均无同名目录。以下按对三套独立课件的价值排序，不代表五个均应启用。

|优先级|候选与路径（均在 .agents/skills/ 下）|用途与依赖|决定|
|---|---|---|---|
|1|pptx/（未创建）|可编辑 PPTX、模板编辑、校验。上游采用 Node.js/pptxgenjs；Python markitdown[pptx]、Pillow、defusedxml、lxml；LibreOffice、Poppler；图标另需 react/react-dom/react-icons/sharp|功能最有价值，但源 LICENSE 限制复制、保留及再分发；本次不安装。继续现有 python-pptx 后端|
|2|docx/（未创建）|讲义、讲稿、操作清单。上游采用 Node.js/docx；Pandoc、LibreOffice、Poppler；OOXML 脚本还需按实际 imports 检查依赖|同上，未安装。继续现有 python-docx 后端|
|3|canvas-design/|封面、静态插图。没有固定软件包依赖清单；可用现有 Pillow/reportlab，需字体及 PDF 检查工具|完整安装，包括 canvas-fonts 与许可；不是科学图表或解剖工具|
|4|algorithmic-art/|p5.js 生成艺术/网页动态演示；浏览器、p5.js，模板使用 CDN；离线需本地化资源|完整安装；按需使用；GIF/MP4 导出工具不包含在内|
|5|brand-guidelines/|Anthropic 专属色彩/字体规范；没有独立执行程序，示例指向 python-pptx；Poppins/Lora 或回退字体|完整安装作为可选参考；医学课件默认不启用，不能当作医院品牌规范|

## 重叠与适配

- medical-teaching 是课程工作流，pptx/docx 是文件生成后端，职责互补。当前 Python 依赖不能满足上游 Node.js 后端，但两者不构成已确认的版本冲突。
- paper-lookup 承担检索，literature-review 承担筛选与证据综合，citation-management 承担元数据与引用核验。功能部分重叠但均保留，不重复安装。
- scientific-visualization 负责真实数据图表；canvas-design 是艺术设计，其少文字要求与用户“详细型课件”冲突，仅用于局部素材。
- theme-factory 与 brand-guidelines 都管视觉规范；前者继续负责课件主题。后者仅按用户明确品牌要求使用。
- slack-gif-creator 生成 GIF；algorithmic-art 生成网页艺术，两者不是同一工具。CRRT 动画必须有医学逻辑、清晰标注、适合课堂的尺寸和播放验证，不能使用 Slack 表情尺寸直接交付。
- 上游默认字体不保证中文覆盖；使用前检查中文字符、嵌入/回退和最终 PowerPoint 渲染。动画与网页交互均不可由静态 PDF 验证。
- 现有科研技能的付费 API、Parallel、OpenRouter 仍是可选，不因新增技能自动获得调用授权。
- 未执行依赖求解或三套课件的实际生成。本次是文件级安装和静态兼容性审查，不能声称所有运行环境已验证。

## 组合方式

medical-teaching → paper-lookup / literature-review → citation-management → scientific-visualization → 已选 theme-factory → python-pptx 成品生成 → pdf 逐页渲染检查。

canvas-design 按需提供封面素材；slack-gif-creator 按需提供 GIF；algorithmic-art 为独立网页演示或另行导出的动画素材；python-docx 生成配套讲义。三套课件分别保存内容、来源和生成脚本，不能仅拆分同一文件后假称独立设计。

## 在 Codex 中同步和准备环境

在现有 eva 仓库中，先查看工作区，有未提交内容时不要自动覆盖或 stash：

```bash
git status --short
git pull --ff-only origin main
```

仅在需要生成课件时，使用项目隔离环境。下面是执行方案，本次没有代为安装依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/requirements-teaching.txt -r tools/requirements-research.txt
.venv/bin/python -m pip check
.venv/bin/python -c 'import pptx, docx, PIL, reportlab; print("document backends available")'
command -v soffice
command -v pdftoppm
fc-list :lang=zh family
```

Ubuntu/Debian 环境缺少渲染器时，由具备系统安装权限的环境执行 `apt-get install libreoffice poppler-utils fonts-noto-cjk`。无权限则明确渲染未完成，不把库导入成功当作视觉检查通过。GIF 后端还需要 `.agents/skills/slack-gif-creator/requirements.txt` 中的依赖，安装后再次执行 pip check。复现实际课件时保存成功环境的锁定版本。

## 保留与许可

原样保留 medical-teaching、literature-review、citation-management、paper-lookup、scientific-visualization、pdf、theme-factory、slack-gif-creator 全部八个目录。

新增三个目录完整保留 Apache-2.0 LICENSE、字体许可及模板；根目录 UPSTREAM_THIRD_PARTY_NOTICES.md 已与源提交逐字节核对一致。pptx/docx 的 LICENSE 是明确限制本次复制的依据，不是缺少 GitHub 写权限。无需为了凑齐五个技能重复安装或删除现有目录。

原始依据：
- https://github.com/qqq236484707-maker/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills
- https://github.com/qqq236484707-maker/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/pptx/LICENSE.txt
- https://github.com/qqq236484707-maker/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/docx/LICENSE.txt
