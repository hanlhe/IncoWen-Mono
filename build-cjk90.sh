#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

"$PYTHON" "$ROOT/build.py" \
  --cjk-scale-x 0.9 \
  --output "$ROOT/dist/cjk90/IncoWenMono-Regular.ttf"

"$PYTHON" "$ROOT/build.py" \
  --style Bold \
  --cjk-scale-x 0.9 \
  --output "$ROOT/dist/cjk90/IncoWenMono-Bold.ttf"
