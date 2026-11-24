#!/usr/bin/env python3
"""Check internal HTML links in a built dist tree. Usage: audit-links.py [dist]"""
import os, re, sys  # noqa: F401
from pathlib import Path

default = Path(os.environ.get("PFV1_DIST", r"C:\Users\jpowe\Desktop\projects\polsia free v1\app\dist"))
root = Path(sys.argv[1] if len(sys.argv) > 1 else default)
htmls = list(root.rglob("*.html"))
links = set()
for h in htmls:
    s = h.read_text(encoding="utf-8", errors="ignore")
    for m in re.findall(r'(?:href|src)="([^"#?]+)', s):
        if m.startswith(("http://", "https://", "mailto:", "data:", "/")):
            if not m.startswith("/"):
                continue
            m = m[1:]
        if not m or m.endswith("/"):
            continue
        links.add(m.split("#")[0])
broken = []
for link in sorted(links):
    if not (root / link).exists() and not (root / (link + ".html")).exists():
        broken.append(link)
print(f"dist html files: {len(htmls)}")
print(f"unique internal links: {len(links)}")
print("BROKEN:", len(broken))
for b in broken[:20]:
    print("  ", b)
sys.exit(1 if broken else 0)
