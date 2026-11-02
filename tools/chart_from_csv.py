#!/usr/bin/env python3
"""Generate a traceable chart only from real, independently reviewed CSV values."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    for k in ("csv","x","y","title","x-label","y-label","source","output"):
        ap.add_argument("--"+k,required=True)
    a=ap.parse_args()
    rows=list(csv.DictReader(open(a.csv,encoding="utf-8-sig",newline="")))
    if not rows or any(a.x not in r or a.y not in r for r in rows):
        ap.error("missing data columns")
    xs,ys=[],[]
    for r in rows:
        xs.append(float(r[a.x]))
        ys.append(float(r[a.y]) if r[a.y].strip() else float("nan"))
    if any(b<=a for a,b in zip(xs,xs[1:])):
        ap.error("x must be strictly increasing")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import rc_context
    out=Path(a.output)
    if out.suffix.lower()!=".png": ap.error("output must be PNG")
    out.parent.mkdir(parents=True,exist_ok=True)
    with rc_context({"font.family":"sans-serif"}):
        fig,ax=plt.subplots(figsize=(10,5.5),layout="constrained")
        ax.plot(xs,ys,marker="o",linewidth=2)
        ax.set(xlabel=a.x_label,ylabel=a.y_label,title=a.title)
        ax.grid(alpha=.2)
        fig.savefig(out,dpi=170)
        plt.close(fig)
    provenance={"csv_sha256":hashlib.sha256(Path(a.csv).read_bytes()).hexdigest(),"source":a.source,"rows":len(rows),"missing_y":sum(v!=v for v in ys),"processing":"no interpolation/smoothing"}
    out.with_suffix(".provenance.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
    main()
