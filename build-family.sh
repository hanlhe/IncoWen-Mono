#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

"$PYTHON" "$ROOT/build.py" \
  --cjk-scale-x 0.9 --cjk-scale-y 0.9 --style Regular \
  --output "$ROOT/dist/IncoWenMono-Regular.ttf"
"$PYTHON" "$ROOT/build.py" \
  --cjk-scale-x 0.9 --cjk-scale-y 0.9 --style Bold \
  --output "$ROOT/dist/IncoWenMono-Bold.ttf"
