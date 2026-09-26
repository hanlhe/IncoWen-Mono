#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NERD_FONTS_REPO="${NERD_FONTS_REPO:-}"

if [[ -z "$NERD_FONTS_REPO" || ! -f "$NERD_FONTS_REPO/font-patcher" ]]; then
  echo "Set NERD_FONTS_REPO to a Nerd Fonts checkout containing font-patcher." >&2
  exit 2
fi

for STYLE in Regular Bold; do
  fontforge -script "$NERD_FONTS_REPO/font-patcher" \
    "$ROOT/dist/IncoWenMono-$STYLE.ttf" \
    --complete \
    --makegroups 0 \
    --name "IncoWen Mono" \
    --outputdir "$ROOT/dist/nerd" \
    --quiet
done

test -s "$ROOT/dist/nerd/IncoWenMonoNerdFont-Regular.ttf"
test -s "$ROOT/dist/nerd/IncoWenMonoNerdFont-Bold.ttf"
