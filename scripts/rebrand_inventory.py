#!/usr/bin/env python3
"""Read-only rebrand inventory for Polsia Free v1.

Nothing is modified. Run it before a rename or theme change to see every
touchpoint, then again afterwards to confirm the old name is gone.

Usage:
    python scripts/rebrand_inventory.py "C:/Users/jpowe/Desktop/projects/polsia free v1/app"
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

SKIP = {"node_modules", ".git", "__pycache__", "capture", "checks", ".smoke"}


def skipped(path: Path) -> bool:
    """True for build output and tool folders that mirror src/."""
    return any(
        part in SKIP or part.startswith("dist") or part.startswith(".")
        for part in path.parts
    )
NAME = re.compile(r"polsia", re.I)
LOCAL_KEY = re.compile(r"localStorage\.(?:get|set|remove)Item\(\s*['\"]([^'\"]+)['\"]")
ENV_VAR = re.compile(r"\b(?:PFV1|POLSIA)_[A-Z0-9_]+\b")
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def walk(root: Path, suffixes: tuple[str, ...]):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if skipped(path):
            continue
        yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}")
        return 2

    web = list(walk(root, (".js", ".html", ".css", ".json", ".py", ".md")))
    hits: Counter[str] = Counter()
    for path in web:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        count = len(NAME.findall(text))
        if count:
            hits[str(path.relative_to(root))] = count

    titles = []
    for path in walk(root, (".html",)):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "<title>" in line:
                titles.append((str(path.relative_to(root)), line.strip()))

    keys: set[str] = set()
    envs: set[str] = set()
    colours: Counter[str] = Counter()
    for path in walk(root, (".js", ".py")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        keys.update(LOCAL_KEY.findall(text))
        envs.update(ENV_VAR.findall(text))
    for path in walk(root, (".css",)):
        colours.update(HEX.findall(path.read_text(encoding="utf-8", errors="ignore")))

    tests_with_name = [p for p in walk(root, (".js", ".py")) if "test" in str(p).lower() and NAME.search(p.read_text(encoding="utf-8", errors="ignore"))]
    assets = sorted(p.name for p in (root / "public").glob("*") if p.is_file()) if (root / "public").is_dir() else []
    pkg = root / "package.json"
    package_name = json.loads(pkg.read_text(encoding="utf-8")).get("name", "?") if pkg.is_file() else "?"

    print("REBRAND INVENTORY (read-only)")
    print(f"root: {root}")
    print(f"package name: {package_name}")
    print(f"files mentioning the current name: {len(hits)} ({sum(hits.values())} occurrences)")
    for path, count in hits.most_common(15):
        print(f"  {count:>4}  {path}")
    print(f"\nHTML titles: {len(titles)}")
    for path, line in titles[:6]:
        print(f"  {path}: {line}")
    print(f"\nlocalStorage keys ({len(keys)}): {', '.join(sorted(keys)) or 'none'}")
    print(f"env prefixes ({len(envs)}): {', '.join(sorted(envs)) or 'none'}")
    print(f"brand assets in public/: {', '.join(assets) or 'none'}")
    print(f"unique hex colours in CSS: {len(colours)}")
    if colours:
        print("  top: " + ", ".join(f"{c}({n})" for c, n in colours.most_common(8)))
    print(f"test files asserting the current name: {len(tests_with_name)}")
    for path in tests_with_name[:8]:
        print(f"  {path.relative_to(root)}")

    print("\nPOST-RENAME CHECKLIST")
    for item in (
        "Replace the display name in HTML titles, headers, footers and docs",
        "Rename package.json name and any vite base/asset paths",
        "Migrate pfv1_* localStorage keys (read old key, write new, keep data)",
        "Rename PFV1_* bridge env vars in .env.example and bridge code",
        "Replace public/brand.svg and any favicon references",
        "Retokenise CSS colours into variables before restyling",
        "Regenerate visual-regression baselines; the current 99.9% is clone-specific",
        "Re-run tests, build, both link audits and the requirement audit",
        "Trademark/domain/legal check before publishing under the new name",
        "Keep dependency licences and attribution unchanged",
    ):
        print(f"  [ ] {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
