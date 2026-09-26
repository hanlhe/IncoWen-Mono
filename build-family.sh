#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

"$PYTHON" "$ROOT/build.py" --style Regular \
  --output "$ROOT/dist/IncoWenMono-Regular.ttf"
"$PYTHON" "$ROOT/build.py" --style Bold \
  --output "$ROOT/dist/IncoWenMono-Bold.ttf"
