#!/usr/bin/env python3
"""
office.py - turn research output into real Office documents.

Takes structured data (JSON) or Markdown and writes .xlsx, .docx, .pptx or .csv.
These are genuine Office Open XML files, so they open in Microsoft Word, Excel
and PowerPoint, in LibreOffice, and in Google Docs/Sheets/Slides. Microsoft
Office does not need to be installed to produce them.

Requires (install once):
    python -m pip install openpyxl python-docx python-pptx

Usage
-----
  office.py --from data.json  --to xlsx out.xlsx
  office.py --from data.json  --to csv  out.csv
  office.py --from notes.md   --to docx report.docx
  office.py --from notes.md   --to pptx deck.pptx
  office.py --from data.json  --to docx report.docx --title "RAM options"

Input shapes accepted from JSON
-------------------------------
  [ {..}, {..} ]                       list of records -> table
  {"columns": [...], "rows": [[...]]}  explicit table
  {"title": "...", "sections": [{"heading": "...", "body": "...", "table": {...}}]}

Markdown rules
--------------
  # / ## / ###   headings
  - / * / 1.     bullets and numbered items
  | a | b |      tables (pipe format)
  ```            fenced code (kept as monospace paragraphs)
"""

import argparse
import csv
import json
import os
import re
import sys


# ------------------------------------------------------------------ loading

def load(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    if ext == ".json":
        return json.loads(raw)
    return {"markdown": raw}


def as_table(data):
    """Normalise supported JSON shapes into (columns, rows)."""
    if isinstance(data, list) and data and isinstance(data[0], dict):
        cols = []
        for rec in data:
            for k in rec:
                if k not in cols:
                    cols.append(k)
        return cols, [[rec.get(c, "") for c in cols] for rec in data]
    if isinstance(data, dict):
        if "columns" in data and "rows" in data:
            return list(data["columns"]), [list(r) for r in data["rows"]]
        if "rows" in data:
            rows = data["rows"]
            return None, [list(r) for r in rows]
    raise SystemExit("Input is not tabular. Use --to docx/pptx for prose, or pass a list of records.")


def as_sections(data):
    """Normalise JSON or Markdown into [{heading, body, table}]."""
    if "markdown" in data:
        return parse_markdown(data["markdown"]),
    if isinstance(data, dict) and "sections" in data:
        out = []
        for s in data["sections"]:
            out.append({
                "heading": s.get("heading", ""),
                "body": s.get("body", ""),
                "table": s.get("table"),
                "bullets": s.get("bullets", []),
            })
        return out
    if isinstance(data, list):
        cols, rows = as_table(data)
        return [{"heading": "Data", "body": "", "table": {"columns": cols, "rows": rows}, "bullets": []}]
    return [{"heading": str(data.get("title", "")), "body": json.dumps(data, indent=2), "table": None, "bullets": []}]


def parse_markdown(md):
    sections, cur = [], {"heading": "", "body": "", "bullets": [], "table": None, "code": False}
    lines = md.splitlines()
    i = 0
    pending_table = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            cur["code"] = not cur["code"]
            i += 1
            continue
        if cur["code"]:
            cur["body"] += line + "\n"
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if cur["heading"] or cur["body"] or cur["bullets"] or cur["table"]:
                sections.append(cur)
            cur = {"heading": m.group(2).strip(), "body": "", "bullets": [], "table": None, "code": False, "level": len(m.group(1))}
            i += 1
            continue
        if line.strip().startswith("|") and line.count("|") >= 2:
            pending_table.append([c.strip() for c in line.strip().strip("|").split("|")])
            i += 1
            # consume the whole table block
            while i < len(lines) and lines[i].strip().startswith("|"):
                pending_table.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            rows = [r for r in pending_table if not all(re.fullmatch(r":?-{2,}:?", c or "") for c in r)]
            if rows:
                cur["table"] = {"columns": rows[0], "rows": rows[1:]}
            pending_table = []
            continue
        m = re.match(r"^\s*(?:[-*+]|\d+\.)\s+(.*)$", line)
        if m:
            cur["bullets"].append(m.group(1).strip())
            i += 1
            continue
        if line.strip():
            cur["body"] += line.strip() + "\n"
        i += 1
    if cur["heading"] or cur["body"] or cur["bullets"] or cur["table"]:
        sections.append(cur)
    return sections


# ------------------------------------------------------------------ writers

def write_csv(data, path):
    cols, rows = as_table(data)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if cols:
            w.writerow(cols)
        w.writerows(rows)
    print(f"wrote {path}  ({len(rows)} rows)")


def write_xlsx(data, path, title=None):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
    except ImportError:
        raise SystemExit("openpyxl missing: python -m pip install openpyxl")

    cols, rows = as_table(data)
    wb = Workbook()
    ws = wb.active
    ws.title = (title or "Data")[:31]

    if cols:
        ws.append(cols)
        for c in range(1, len(cols) + 1):
            cell = ws.cell(row=1, column=c)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E78")
            cell.alignment = Alignment(vertical="center")
        ws.freeze_panes = "A2"
    for r in rows:
        ws.append(["" if v is None else v for v in r])

    all_rows = ([cols] if cols else []) + rows
    for c in range(1, (len(cols) or max((len(r) for r in rows), default=1)) + 1):
        width = max(len(str(r[c - 1])) if c - 1 < len(r) else 0 for r in all_rows) if all_rows else 10
        ws.column_dimensions[get_column_letter(c)].width = min(60, max(10, width + 2))
    ws.auto_filter.ref = ws.dimensions

    wb.save(path)
    print(f"wrote {path}  ({len(rows)} data rows, {len(cols or [])} columns)")


def write_docx(data, path, title=None):
    try:
        from docx import Document
        from docx.shared import Pt
    except ImportError:
        raise SystemExit("python-docx missing: python -m pip install python-docx")

    sections = as_sections(data)
    doc = Document()
    if title:
        doc.add_heading(title, level=0)

    for s in sections:
        if s.get("heading"):
            doc.add_heading(s["heading"], level=min(s.get("level", 1), 4))
        for line in (s.get("body") or "").splitlines():
            if line.strip():
                doc.add_paragraph(line.strip())
        for b in s.get("bullets") or []:
            doc.add_paragraph(b, style="List Bullet")
        if s.get("table"):
            cols = s["table"]["columns"]
            rows = s["table"]["rows"]
            t = doc.add_table(rows=1, cols=len(cols))
            t.style = "Light Grid Accent 1"
            for i, c in enumerate(cols):
                cell = t.rows[0].cells[i]
                cell.text = str(c)
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.bold = True
            for r in rows:
                cells = t.add_row().cells
                for i, v in enumerate(r[: len(cols)]):
                    cells[i].text = "" if v is None else str(v)
            doc.add_paragraph("")
    doc.save(path)
    print(f"wrote {path}  ({len(sections)} sections)")


def write_pptx(data, path, title=None):
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
    except ImportError:
        raise SystemExit("python-pptx missing: python -m pip install python-pptx")

    sections = as_sections(data)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    cover = prs.slides.add_slide(prs.slide_layouts[0])
    cover.shapes.title.text = title or (sections[0]["heading"] if sections else "Report")
    if len(cover.placeholders) > 1:
        cover.placeholders[1].text = "Generated by research.py + office.py"

    for s in sections:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = s.get("heading") or "Slide"
        body = slide.placeholders[1].text_frame
        body.clear()
        first = True
        for line in (s.get("body") or "").splitlines():
            if line.strip():
                p = body.paragraphs[0] if first else body.add_paragraph()
                p.text = line.strip()
                p.font.size = Pt(18)
                first = False
        for b in s.get("bullets") or []:
            p = body.paragraphs[0] if first else body.add_paragraph()
            p.text = b
            p.level = 0
            p.font.size = Pt(18)
            first = False
        if s.get("table"):
            cols, rows = s["table"]["columns"], s["table"]["rows"]
            top = Inches(5.0) if first is False else Inches(2.0)
            shape = slide.shapes.add_table(
                min(len(rows) + 1, 6), len(cols), Inches(0.8), top, Inches(11.7), Inches(0.4 * min(len(rows) + 1, 6))
            )
            tbl = shape.table
            for i, c in enumerate(cols[: len(tbl.columns)]):
                tbl.cell(0, i).text = str(c)
            for ri, r in enumerate(rows[: len(tbl.rows) - 1], start=1):
                for ci, v in enumerate(r[: len(tbl.columns)]):
                    tbl.cell(ri, ci).text = "" if v is None else str(v)
    prs.save(path)
    print(f"wrote {path}  ({len(prs.slides)} slides)")


# ------------------------------------------------------------------ main

def main():
    p = argparse.ArgumentParser(
        description="Convert JSON or Markdown into xlsx / docx / pptx / csv.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--from", dest="src", required=True, help="input .json or .md")
    p.add_argument("--to", dest="fmt", required=True, choices=["xlsx", "docx", "pptx", "csv"])
    p.add_argument("out", help="output file path")
    p.add_argument("--title", help="document / workbook title")
    args = p.parse_args()

    data = load(args.src)

    if args.fmt == "csv":
        write_csv(data, args.out)
    elif args.fmt == "xlsx":
        write_xlsx(data, args.out, args.title)
    elif args.fmt == "docx":
        write_docx(data, args.out, args.title)
    elif args.fmt == "pptx":
        write_pptx(data, args.out, args.title)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    sys.exit(main())
