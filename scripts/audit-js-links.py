#!/usr/bin/env python3
"""Check absolute path literals in source JS against the built dist tree.

Usage: audit-js-links.py [app_dir]
  app_dir defaults to PFV1_APP or the local Windows workspace path.
"""
import glob
import os
import re
import sys

base = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "PFV1_APP", r"C:\Users\jpowe\Desktop\projects\polsia free v1\app")
root = os.path.join(base, "dist")
src = os.path.join(base, "src")
links = {}
for f in glob.glob(os.path.join(src, "*.js")):
    txt = open(f, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r"[\"'](/[A-Za-z0-9_\-/\.]*)[\"']", txt):
        p = m.group(1)
        if len(p) < 2 or "\\" in p or p.startswith("//"):
            continue
        links.setdefault(p, set()).add(os.path.basename(f))

missing = []
for href, sources in links.items():
    path = href.split("#")[0].split("?")[0]
    if not path:
        continue
    rel = path.lstrip("/").replace("/", os.sep)
    candidates = [
        os.path.join(root, rel),
        os.path.join(root, rel, "index.html"),
        os.path.join(root, rel + ".html"),
    ]
    if not any(os.path.exists(c) for c in candidates):
        missing.append((href, sorted(sources)))

print("JS path literals:", len(links))
print("BROKEN:", len(missing))
for href, srcs in sorted(missing):
    print(" ", href, "<-", ", ".join(srcs[:4]))
sys.exit(1 if missing else 0)
