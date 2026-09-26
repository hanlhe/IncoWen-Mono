#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

for style in Light Regular Bold; do
  "$PYTHON" "$ROOT/build.py" \
    --cjk-scale-x 0.9 --cjk-scale-y 0.9 --style "$style" \
    --output "$ROOT/dist/WenSolataMono-$style.ttf"
done
