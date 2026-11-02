#!/usr/bin/env python3
"""Original Eva medical-PPTX pipeline; not derived from proprietary PPTX skills."""
import argparse
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile, BadZipFile

KINDS = {"cover", "section", "bullets", "two_column", "image_right"}
BAD = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b|待补充|待核验|待审核|占位符", re.I)
PALETTE = dict(background="F8FBFD", foreground="152A3B", accent="177E89", muted="506477", font="Noto Sans CJK SC")

def load(path, release=False):
    path = Path(path).resolve(strict=True)
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("schema_version") != 1 or not d.get("title") or not d.get("course_id"):
        raise ValueError("invalid deck schema/title/course_id")
    if d.get("status") not in ("draft", "reviewed") or (release and d["status"] != "reviewed"):
        raise ValueError("course must be reviewed for release")
    sources, assets, slides = d.get("sources", {}), d.get("assets", {}), d.get("slides", [])
    if not isinstance(sources, dict) or not isinstance(assets, dict) or not isinstance(slides, list) or not slides:
        raise ValueError("invalid sources/assets/slides")
    for sid, s in sources.items():
        if not s.get("title") or not s.get("url") or (release and s.get("verified") is not True):
            raise ValueError(f"source not documented/verified: {sid}")
    for aid, a in assets.items():
        if a.get("kind") not in ("image", "chart", "animation") or any(not a.get(k) for k in ("path", "license", "source", "alt")):
            raise ValueError(f"invalid asset metadata {aid}")
        rel = Path(a["path"])
        target = (path.parent / rel).resolve()
        if rel.is_absolute() or ".." in rel.parts or not target.is_relative_to(path.parent) or not target.is_file() or target.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif"):
            raise ValueError(f"missing or unsafe asset: {aid}")
        if a["kind"] == "animation" and target.suffix.lower() != ".gif":
            raise ValueError("animation must be GIF")
        if release and a.get("approved") is not True:
            raise ValueError(f"unapproved media: {aid}")
    seen = set()
    for i, s in enumerate(slides, 1):
        if not s.get("id") or s["id"] in seen or not s.get("title") or s.get("kind") not in KINDS:
            raise ValueError(f"invalid or duplicated slide {i}")
        seen.add(s["id"])
        for key in ("bullets", "right_bullets", "source_ids", "asset_ids"):
            if not isinstance(s.get(key, []), list):
                raise ValueError(f"slide {i}: {key} must be list")
        if set(s.get("source_ids", [])) - sources.keys() or set(s.get("asset_ids", [])) - assets.keys():
            raise ValueError(f"slide {i}: unknown source/asset")
        aids = s.get("asset_ids", [])
        if len(aids) > 1 or bool(aids) != (s["kind"] == "image_right"):
            raise ValueError(f"slide {i}: image_right requires exactly one asset")
        if s["kind"] == "two_column" and not s.get("right_bullets"):
            raise ValueError(f"slide {i}: right column is empty")
        if release:
            content = " ".join([s["title"], s.get("subtitle", ""), *s.get("bullets", []), *s.get("right_bullets", [])])
            if BAD.search(content) or (s["kind"] not in ("cover", "section") and not s.get("source_ids")):
                raise ValueError(f"slide {i}: release content not reviewed/cited")
    return d

def rgb(hexval):
    from pptx.dml.color import RGBColor
    v = hexval.lstrip("#")
    if not re.fullmatch("[0-9a-fA-F]{6}", v):
        raise ValueError("invalid theme color")
    return RGBColor.from_string(v.upper())

def text(slide, content, box, theme, size=21, accent=False, bold=False):
    from pptx.util import Inches, Pt
    item = slide.shapes.add_textbox(*(Inches(v) for v in box))
    tf = item.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(.05)
    for j, line in enumerate(str(content).split("\n")):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = line
        p.space_after = Pt(10)
        for run in p.runs:
            run.font.name = theme["font"]
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = rgb(theme["accent"] if accent else theme["foreground"])
    return item

def bullets(slide, lines, box, theme, size=21):
    text(slide, "\n".join("•  " + line for line in lines), box, theme, size)

def build(course, output, release=False):
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.util import Inches
    from PIL import Image
    course, output = Path(course).resolve(), Path(output)
    d = load(course, release)
    theme = PALETTE | d.get("theme", {})
    for key in ("background", "foreground", "accent", "muted"):
        rgb(theme[key])
    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(13.333), Inches(7.5)
    media = []
    output.parent.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(d["slides"], 1):
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = rgb(theme["background"])
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(.46), Inches(.48), Inches(.10), Inches(.68))
        band.fill.solid()
        band.fill.fore_color.rgb = rgb(theme["accent"])
        band.line.fill.background()
        kind = s["kind"]
        text(slide, s["title"], (.79, 1.2 if kind == "cover" else .48, 11.8, 1.1), theme, 37 if kind == "cover" else 31, bold=True)
        if kind in ("cover", "section"):
            text(slide, s.get("subtitle", ""), (.80, 3.0, 11.5, 1.4), theme, 23)
        elif kind == "bullets":
            bullets(slide, s.get("bullets", []), (.84, 1.6, 11.6, 4.8), theme)
        elif kind == "two_column":
            text(slide, s.get("left_heading", "重点"), (.84, 1.5, 5.4, .5), theme, 20, accent=True)
            text(slide, s.get("right_heading", "补充"), (6.81, 1.5, 5.4, .5), theme, 20, accent=True)
            bullets(slide, s.get("bullets", []), (.84, 2.1, 5.4, 4.2), theme, 19)
            bullets(slide, s.get("right_bullets", []), (6.81, 2.1, 5.4, 4.2), theme, 19)
        elif kind == "image_right":
            bullets(slide, s.get("bullets", []), (.84, 1.6, 5.3, 4.7), theme, 19)
            aid = s["asset_ids"][0]
            a = d["assets"][aid]
            original = (course.parent / a["path"]).resolve()
            image = original
            if a["kind"] == "animation":
                image = output.parent / "assets" / f"{d['course_id']}-{aid}-poster.png"
                image.parent.mkdir(parents=True, exist_ok=True)
                with Image.open(original) as im:
                    im.seek(0)
                    im.convert("RGB").save(image)
            with Image.open(image) as im:
                ratio = min(5.8 / im.width, 4.6 / im.height)
                w, h = im.width * ratio, im.height * ratio
            slide.shapes.add_picture(str(image), Inches(6.64 + (5.8 - w)/2), Inches(1.7 + (4.6 - h)/2), width=Inches(w), height=Inches(h))
            media.append({"asset_id": aid, "source": str(original), "sha256": hashlib.sha256(original.read_bytes()).hexdigest(), "license": a["license"], "alt": a["alt"], "gif_is_static_poster": a["kind"] == "animation"})
        text(slide, " | ".join("[" + sid + "]" for sid in s.get("source_ids", [])), (.81, 6.86, 10.8, .35), theme, 10)
        text(slide, f"{i}/{len(d['slides'])}", (12.0, 6.86, .6, .35), theme, 10)
    deck.save(output)
    manifest = {"course": d["course_id"], "slides": len(d["slides"]), "assets": media, "release_requested": release}
    output.with_suffix(".build.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"pptx": str(output), "slides": len(d["slides"]), "manifest": str(output.with_suffix(".build.json"))}

def check(pptx, course=None, release=False):
    from pptx import Presentation
    pptx = Path(pptx)
    errors, warnings = [], []
    with ZipFile(pptx) as z:
        names = set(z.namelist())
        if z.testzip():
            errors.append("corrupt ZIP member")
        if not {"[Content_Types].xml", "ppt/presentation.xml"} <= names:
            errors.append("missing required OOXML files")
        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            root = ET.fromstring(z.read(name))
            if name.endswith(".rels"):
                base = "" if name == "_rels/.rels" else posixpath.dirname(posixpath.dirname(name))
                for rel in root:
                    target = rel.get("Target", "")
                    if target and rel.get("TargetMode") != "External":
                        dest = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
                        if dest not in names:
                            errors.append(f"broken OOXML relationship {name}: {target}")
    prs = Presentation(pptx)
    if abs(prs.slide_width/prs.slide_height - 16/9) > .025:
        warnings.append("not 16:9")
    for i, slide in enumerate(prs.slides, 1):
        content = " ".join(sh.text for sh in slide.shapes if sh.has_text_frame)
        if not content.strip():
            warnings.append(f"page {i}: no editable text")
        if BAD.search(content):
            (errors if release else warnings).append(f"page {i}: placeholder")
        for sh in slide.shapes:
            if sh.left < 0 or sh.top < 0 or sh.left+sh.width > prs.slide_width+11000 or sh.top+sh.height > prs.slide_height+11000:
                errors.append(f"page {i}: out of bounds: {sh.name}")
    if course:
        d = load(course, release)
        if len(prs.slides) != len(d["slides"]):
            errors.append("page count mismatch")
        else:
            for i, s in enumerate(d["slides"]):
                content = " ".join(sh.text for sh in prs.slides[i].shapes if sh.has_text_frame)
                if s["title"] not in content or any(f"[{sid}]" not in content for sid in s.get("source_ids", [])):
                    errors.append(f"page {i+1}: missing title/reference")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "slides": len(prs.slides), "visual_review_required": True}

def render(pptx, directory, dpi=110):
    from PIL import Image, ImageDraw
    from pypdf import PdfReader
    pptx, directory = Path(pptx).resolve(), Path(directory).resolve()
    if not (60 <= dpi <= 220) or not shutil.which("soffice") or not shutil.which("pdftoppm"):
        raise ValueError("render requires LibreOffice, Poppler and DPI 60..220")
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        subprocess.run(["soffice", f"-env:UserInstallation={Path(temp).as_uri()}", "--headless", "--convert-to", "pdf", "--outdir", str(directory), str(pptx)], check=True, timeout=120)
    pdf = directory / (pptx.stem+".pdf")
    n = len(PdfReader(pdf).pages)
    if n != check(pptx)["slides"]:
        raise ValueError("PDF/PPTX page mismatch")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(directory/"slide")], check=True, timeout=120)
    frames = sorted(directory.glob("slide-*.png"))
    if len(frames) != n:
        raise ValueError("PNG page count mismatch")
    cols, rows = min(n,3), (n+2)//3
    sheet = Image.new("RGB", (cols*660, rows*390), "#eeeeee")
    for i,p in enumerate(frames):
        with Image.open(p) as im:
            im = im.convert("RGB")
            im.thumbnail((640,360))
            sheet.paste(im, ((i%cols)*660+10, (i//cols)*390+10))
        ImageDraw.Draw(sheet).text(((i%cols)*660+15, (i//cols)*390+366), f"Slide {i+1}", fill="black")
    sheet.save(directory/"contact-sheet.png")
    result = {"pdf": str(pdf), "pages": n, "contact_sheet": str(directory/"contact-sheet.png"), "visual_review_required": True, "animation_tested": False}
    (directory/"render-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("doctor")
    p.add_argument("--require-render", action="store_true")
    p = sub.add_parser("build")
    p.add_argument("--course", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--release", action="store_true")
    p = sub.add_parser("check")
    p.add_argument("--pptx", required=True)
    p.add_argument("--course")
    p.add_argument("--report")
    p.add_argument("--release", action="store_true")
    p = sub.add_parser("render")
    p.add_argument("--pptx", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args()
    try:
        if a.command == "doctor":
            import importlib.metadata
            packages = {}
            for pkg in ("python-pptx","Pillow","pypdf","python-docx","openpyxl","matplotlib"):
                try: packages[pkg] = importlib.metadata.version(pkg)
                except importlib.metadata.PackageNotFoundError: packages[pkg] = None
            binaries = {name: shutil.which(name) for name in ("soffice","pdftoppm","fc-match")}
            ok = all(packages[k] for k in ("python-pptx","Pillow","pypdf"))
            if a.require_render: ok = ok and binaries["soffice"] and binaries["pdftoppm"]
            result = {"ok":bool(ok),"packages":packages,"binaries":binaries,"render_available":bool(binaries["soffice"] and binaries["pdftoppm"])}
        elif a.command == "build": result = build(a.course, a.output, a.release)
        elif a.command == "check":
            result = check(a.pptx, a.course, a.release)
            if a.report:
                Path(a.report).parent.mkdir(parents=True, exist_ok=True)
                Path(a.report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        else: result = render(a.pptx, a.out_dir, a.dpi)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok",True) else 1
    except (ValueError, OSError, BadZipFile, ET.ParseError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as ex:
        print(f"ERROR: {ex}",file=sys.stderr)
        return 2
if __name__ == "__main__":
    sys.exit(main())
