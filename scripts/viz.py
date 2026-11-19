#!/usr/bin/env python3
"""
viz.py - charts and diagrams from plain data, with no third-party packages.

Produces SVG (real vector images, openable in a browser, Word, PowerPoint,
LibreOffice, Inkscape and Google Slides), standalone HTML reports, and Mermaid
diagram source (rendered by GitHub, GitLab, Obsidian, VS Code and the OpenCode
Review pane).

Usage
-----
  viz.py --from data.json --chart bar  --x name --y price -o ram.svg --title "RAM options"
  viz.py --from data.json --chart line --x month --y revenue -o trend.svg
  viz.py --from data.json --chart pie  --x name --y share -o split.svg
  viz.py --from data.csv  --chart bar  --x name --y price -o ram.svg --html
  viz.py --mermaid flowchart --from flow.json -o flow.md
  viz.py --mermaid mindmap  --from map.json  -o map.md

Data shapes
-----------
  [{"name": "Timetec", "price": 51.99}, ...]
  {"columns": ["name","price"], "rows": [["Timetec", 51.99], ...]}
  .csv with a header row

Mermaid JSON shapes
-------------------
  flowchart: {"direction":"LR","nodes":[{"id":"a","label":"Start"}],"edges":[{"from":"a","to":"b","label":"yes"}]}
  mindmap:   {"root":"Laptop","children":[{"label":"Memory","children":[{"label":"12 GB max"}]}]}
"""

import argparse
import csv
import html
import json
import os
import sys

PALETTE = ["#2563eb", "#16a34a", "#dc2626", "#d97706", "#7c3aed",
           "#0891b2", "#db2777", "#65a30d", "#475569", "#c2410c"]


# ------------------------------------------------------------------ data

def load_rows(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, newline="", encoding="utf-8-sig") as f:
            r = list(csv.DictReader(f))
        return r
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "columns" in data:
        return [dict(zip(data["columns"], row)) for row in data["rows"]]
    return data


def series(rows, xkey, ykey):
    out = []
    for r in rows:
        try:
            v = float(str(r[ykey]).replace(",", "").replace("£", "").replace("$", "").strip())
        except (ValueError, KeyError):
            continue
        out.append((str(r.get(xkey, "")), v))
    return out


# ------------------------------------------------------------------ svg

def esc(s):
    return html.escape(str(s), quote=True)


def svg_bar(data, title="", width=900, height=520):
    pad_l, pad_b, pad_t, pad_r = 90, 110, 70, 30
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    vmax = max(v for _, v in data) or 1
    step = 10 ** (len(str(int(vmax))) - 1) / 2 or 1
    top = (int(vmax / step) + 1) * step
    n = len(data)
    slot = plot_w / n
    bw = min(110, slot * 0.6)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="20" font-weight="600" fill="#0f172a">{esc(title)}</text>'
    ]
    # gridlines + y labels
    ticks = 5
    for i in range(ticks + 1):
        val = top * i / ticks
        y = pad_t + plot_h - (plot_h * i / ticks)
        parts.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{pad_l-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="#64748b">{val:,.0f}</text>')
    parts.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#94a3b8"/>')

    for i, (label, v) in enumerate(data):
        h = plot_h * (v / top) if top else 0
        x = pad_l + slot * i + (slot - bw) / 2
        y = pad_t + plot_h - h
        colour = PALETTE[i % len(PALETTE)]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{colour}" rx="3"/>')
        parts.append(f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#0f172a">{v:,.2f}</text>')
        short = label if len(label) <= 16 else label[:15] + "…"
        ty = pad_t + plot_h + 20
        parts.append(f'<text x="{x+bw/2:.1f}" y="{ty}" text-anchor="end" font-size="12" fill="#334155" '
                     f'transform="rotate(-35 {x+bw/2:.1f} {ty})">{esc(short)}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def svg_line(data, title="", width=900, height=520):
    pad_l, pad_b, pad_t, pad_r = 90, 90, 70, 30
    plot_w, plot_h = width - pad_l - pad_r, height - pad_t - pad_b
    vmax = max(v for _, v in data) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="20" font-weight="600" fill="#0f172a">{esc(title)}</text>'
    ]
    for i in range(6):
        y = pad_t + plot_h - plot_h * i / 5
        parts.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l+plot_w}" y2="{y:.1f}" stroke="#e2e8f0"/>')
        parts.append(f'<text x="{pad_l-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="#64748b">{vmax*i/5:,.0f}</text>')
    n = len(data)
    pts = []
    for i, (_, v) in enumerate(data):
        x = pad_l + (plot_w * i / max(1, n - 1))
        y = pad_t + plot_h - plot_h * (v / vmax)
        pts.append((x, y))
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    parts.append(f'<polyline points="{d}" fill="none" stroke="#2563eb" stroke-width="3"/>')
    for (label, v), (x, y) in zip(data, pts):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#2563eb"/>')
        parts.append(f'<text x="{x:.1f}" y="{y-12:.1f}" text-anchor="middle" font-size="11" fill="#0f172a">{v:,.1f}</text>')
        parts.append(f'<text x="{x:.1f}" y="{pad_t+plot_h+22:.1f}" text-anchor="middle" font-size="11" fill="#334155">{esc(label[:14])}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def svg_pie(data, title="", width=900, height=520):
    import math
    total = sum(v for _, v in data) or 1
    cx, cy, r = width * 0.36, height * 0.55, min(width, height) * 0.32
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width/2}" y="34" text-anchor="middle" font-size="20" font-weight="600" fill="#0f172a">{esc(title)}</text>'
    ]
    start = -math.pi / 2
    for i, (label, v) in enumerate(data):
        frac = v / total
        end = start + frac * 2 * math.pi
        x1, y1 = cx + r * math.cos(start), cy + r * math.sin(start)
        x2, y2 = cx + r * math.cos(end), cy + r * math.sin(end)
        large = 1 if frac > 0.5 else 0
        parts.append(
            f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} Z" '
            f'fill="{PALETTE[i % len(PALETTE)]}" stroke="#ffffff" stroke-width="2"/>'
        )
        mid = (start + end) / 2
        lx, ly = cx + r * 0.66 * math.cos(mid), cy + r * 0.66 * math.sin(mid)
        if frac > 0.06:
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="13" '
                         f'font-weight="600" fill="#ffffff">{frac*100:.0f}%</text>')
        # legend
        ly2 = 120 + i * 26
        parts.append(f'<rect x="{width*0.72:.0f}" y="{ly2-12}" width="14" height="14" fill="{PALETTE[i % len(PALETTE)]}"/>')
        parts.append(f'<text x="{width*0.72+22:.0f}" y="{ly2}" font-size="13" fill="#0f172a">{esc(label[:24])} — {v:,.2f}</text>')
        start = end
    parts.append("</svg>")
    return "\n".join(parts)


def html_wrap(svg, title):
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{esc(title)}</title>"
        "<style>body{margin:0;font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;"
        "display:flex;justify-content:center;padding:24px}"
        ".card{background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(15,23,42,.08);padding:8px}"
        "</style></head><body><div class='card'>" + svg + "</div></body></html>"
    )


# ------------------------------------------------------------------ mermaid

def mermaid_flowchart(spec):
    d = spec.get("direction", "LR")
    lines = [f"flowchart {d}"]
    for n in spec.get("nodes", []):
        lines.append(f'    {n["id"]}["{n.get("label", n["id"])}"]')
    for e in spec.get("edges", []):
        if e.get("label"):
            lines.append(f'    {e["from"]} -->|{e["label"]}| {e["to"]}')
        else:
            lines.append(f'    {e["from"]} --> {e["to"]}')
    return "\n".join(lines)


def mermaid_mindmap(spec):
    lines = ["mindmap", f'  root(({spec.get("root", "Root")}))']

    def walk(node, depth):
        pad = "  " * depth
        lines.append(f"{pad}{node.get('label', '?')}")
        for c in node.get("children", []):
            walk(c, depth + 1)

    for c in spec.get("children", []):
        walk(c, 2)
    return "\n".join(lines)


# ------------------------------------------------------------------ main

def main():
    p = argparse.ArgumentParser(description="Charts and diagrams from data, no dependencies.")
    p.add_argument("--from", dest="src", required=True, help="input .json or .csv")
    p.add_argument("--chart", choices=["bar", "line", "pie"], help="chart type")
    p.add_argument("--mermaid", choices=["flowchart", "mindmap"], help="diagram type")
    p.add_argument("--x", default="name", help="label column (default: name)")
    p.add_argument("--y", default="value", help="value column (default: value)")
    p.add_argument("--title", default="", help="chart title")
    p.add_argument("--width", type=int, default=900)
    p.add_argument("--height", type=int, default=520)
    p.add_argument("--html", action="store_true", help="also write a .html wrapper")
    p.add_argument("-o", "--out", required=True, help="output file")
    args = p.parse_args()

    if args.mermaid:
        with open(args.src, encoding="utf-8") as f:
            spec = json.load(f)
        body = mermaid_flowchart(spec) if args.mermaid == "flowchart" else mermaid_mindmap(spec)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("```mermaid\n" + body + "\n```\n")
        print(f"wrote {args.out}  ({args.mermaid})")
        return 0

    if not args.chart:
        raise SystemExit("Pick --chart bar|line|pie or --mermaid flowchart|mindmap")

    rows = load_rows(args.src)
    data = series(rows, args.x, args.y)
    if not data:
        raise SystemExit(f"No numeric values found in column '{args.y}'")

    fn = {"bar": svg_bar, "line": svg_line, "pie": svg_pie}[args.chart]
    svg = fn(data, args.title or os.path.basename(args.src), args.width, args.height)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {args.out}  ({args.chart}, {len(data)} points)")

    if args.html:
        hp = os.path.splitext(args.out)[0] + ".html"
        with open(hp, "w", encoding="utf-8") as f:
            f.write(html_wrap(svg, args.title or "Chart"))
        print(f"wrote {hp}")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main())
