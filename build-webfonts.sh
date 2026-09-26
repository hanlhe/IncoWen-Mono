#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

"$PYTHON" - "$ROOT" <<'PY'
import os
import shutil
import sys
from pathlib import Path

from fontTools.ttLib import woff2

root = Path(sys.argv[1])
web_source = Path(os.environ.get("WEB_SOURCE", root / "web")).resolve()
site = root / "site"
if not web_source.is_dir():
    raise SystemExit(f"Web page source directory not found: {web_source}")
shutil.rmtree(site, ignore_errors=True)
shutil.copytree(web_source, site, ignore=shutil.ignore_patterns(".DS_Store"))
shutil.copy2(root / "OFL.txt", site / "OFL.txt")
(site / "woff2").mkdir(parents=True, exist_ok=True)

for style in ("Light", "Regular", "Bold"):
    source = root / "dist" / f"WenSolataMono-{style}.ttf"
    output = site / "woff2" / f"WenSolataMono-{style}.woff2"
    woff2.compress(str(source), str(output))
    print(f"Wrote {output}")
PY
