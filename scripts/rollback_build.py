#!/usr/bin/env python3
"""Restore the last known good build after a failed deployment.

`npm run build` snapshots dist/ into dist.previous/ before Vite runs. This
script swaps them back, locally and without credentials.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

WORKSPACE = Path(os.environ.get("PFV1_WORKSPACE", r"C:\Users\jpowe\Desktop\projects\polsia free v1"))
DIST = WORKSPACE / "app" / "dist"
PREVIOUS = WORKSPACE / "app" / "dist.previous"


def main() -> None:
    if not PREVIOUS.exists():
        raise SystemExit("No previous build to restore. Run npm run build once first.")
    if DIST.exists():
        backup = DIST.with_name("dist.failed")
        if backup.exists():
            shutil.rmtree(backup)
        DIST.rename(backup)
    PREVIOUS.rename(DIST)
    print(f"Restored {DIST.relative_to(WORKSPACE)} from {PREVIOUS.name}")


if __name__ == "__main__":
    main()
