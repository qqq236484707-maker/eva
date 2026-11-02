# Eva 医学课件 PPTX 生成与 QA（独立原创实现）

本方案只使用公开 Python 库及独立编写的脚本，不复制或安装带专有许可证的上游 pptx skill，不覆盖既有 .agents/skills。

## 依赖

Python 3.11+、tools/requirements-teaching.txt 内的 python-pptx、Pillow、pypdf 已覆盖生成与校验；可选 python-docx、openpyxl 用于讲义及证据表。科研 CSV 图表依赖 tools/requirements-research.txt 的 matplotlib。PDF 导出需要 LibreOffice (soffice)，逐页 PNG 需要 Poppler (pdftoppm)，中文需要 Noto Sans CJK SC 等可用字体。

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/requirements-teaching.txt -r tools/requirements-research.txt
python tools/medical_ppt.py doctor --require-render
```

## 逐页生成、检查与 PDF 可视化

```bash
for c in aki cvc crrt; do
  python tools/medical_ppt.py build --course courses/$c/deck.json --output output/$c/$c.pptx
  python tools/medical_ppt.py check --pptx output/$c/$c.pptx --course courses/$c/deck.json --report output/$c/check.json
  python tools/medical_ppt.py render --pptx output/$c/$c.pptx --out-dir output/$c/render
done
python -m unittest discover -s tests -v
```

三门课分别配置在 courses/aki、courses/cvc、courses/crrt；各自只有五页未审校的流程验证稿，不是完整医学教学课件。JSON 每页可设 id、title、kind、bullets、right_bullets、source_ids、asset_ids。source 需要标题、URL、验证标志。asset 需要 path、kind、source、license、alt、approved；图片保留 SHA256 溯源，GIF 仅使用第一帧静态海报，不支持播放。CSV 原始数据可通过 tools/chart_from_csv.py 生成 PNG 和 provenance.json，缺失点不得臆造或补全。

`check` 包含压缩包校验、OOXML 解析与内部关系、可编辑文本、比例、形状边界、页数、标题与文献引用；`render` 转换 PDF 后生成逐页 PNG 和联系表。必须人工核对中文字体、裁剪/遮挡、图表单位、图像与设备准确性、医学证据、许可及 PowerPoint 放映。自动通过不等于医学与视觉验收。

`--release` 需要 reviewed 状态、实际来源验证标记、素材批准及正文无待审核文字；这些是数据登记门禁，不是真实医学证据核验。

不支持原生动画时间线、触发器、原生视频自动嵌入或播放测试，无法保证 Microsoft PowerPoint 与 LibreOffice 逐像素一致，也无法独立医学审校。公开仓库不得放患者资料、院内秘密或未经授权的图像。
