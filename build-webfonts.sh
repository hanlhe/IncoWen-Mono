#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

"$PYTHON" - "$ROOT" <<'PY'
import shutil
import sys
from pathlib import Path

from fontTools.ttLib import woff2

root = Path(sys.argv[1])
site = root / "site"
shutil.rmtree(site, ignore_errors=True)
shutil.copytree(root / "web", site, ignore=shutil.ignore_patterns(".DS_Store"))
shutil.copy2(root / "OFL.txt", site / "OFL.txt")
(site / "woff2").mkdir(parents=True, exist_ok=True)

for style in ("Regular", "Bold"):
    source = root / "dist" / f"IncoWenMono-{style}.ttf"
    output = site / "woff2" / f"IncoWenMono-{style}.woff2"
    woff2.compress(str(source), str(output))
    print(f"Wrote {output}")
PY
