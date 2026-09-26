# IncoWen Mono

IncoWen Mono combines Inconsolata Latin glyphs with LXGW WenKai Mono Lite
Chinese glyphs. It provides static Regular and Bold styles. Both styles keep
the same 500-unit Latin and 1000-unit CJK terminal advances.

## Styles

| Style | Inconsolata instance |
| --- | --- |
| Regular | `wdth=87.5`, `wght=350` |
| Bold | `wdth=90`, `wght=650` |

The Inconsolata source has no italic files or italic/slant axis, so this family
does not include Italic or Bold Italic. No synthetic slant is applied.

Discretionary ligatures are included as the `dlig` feature. Enable discretionary
ligatures in your editor to use them. For CSS:

```css
font-variant-ligatures: discretionary-ligatures;
```

## Chinese glyph spacing

The standard build keeps LXGW WenKai Mono Lite's original CJK outlines. The
optional `dist/cjk90/` build narrows Han, CJK radicals, and common CJK
punctuation outlines to 90%, centered in their cells. Vertical size and the
1000-unit advances remain unchanged. This gives the Chinese glyphs more visible
side space without changing terminal column alignment. The CJK90 variant is a
creator choice: its internal family name is still `IncoWen Mono`, and its font
file names do not include a CJK90 suffix.

## Chinese language metadata

LXGW WenKai Mono Lite's localized font name is Simplified Chinese (`zh-CN`),
but its OS/2 code-page flags advertise both Simplified Chinese (936) and
Traditional Chinese (950). The merged fonts preserve the Simplified flag and
clear the Traditional flag, so font viewers should classify the CJK coverage as
Simplified Han. This changes classification metadata, not the CJK glyphs.
OpenType defines these code-page flags in the
[OS/2 table specification](https://learn.microsoft.com/en-us/typography/opentype/spec/os2#ulcodepagerange).

## Build

The build uses the sibling `Inconsolata` and `LxgwWenKai-Lite` checkouts.
Install the dependency and build both standard weights:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./build-family.sh
```

This writes `dist/IncoWenMono-Regular.ttf` and `dist/IncoWenMono-Bold.ttf`.
Build both CJK90 weights with:

```sh
./build-cjk90.sh
```

This writes same-named Regular and Bold files under `dist/cjk90/`.

The font family name stays `IncoWen Mono` for both spacing choices. In Ghostty,
the standard fonts can be selected with:

```ini
font-family = "IncoWen Mono"
```

The separate Nerd Font patch uses the family name `IncoWenMono Nerd Font`.
These static fonts do not need Ghostty `font-variation` settings.

WenKai's combining diacritics, variation sequence data, vertical metrics, and
OpenType layout tables are retained. Inconsolata's `dlig` feature is merged
into each style.

## Nerd Font variants

The Nerd Font outputs are separate from the standard fonts. They include the
complete Nerd Fonts glyph set, including Braille. To build them, install
FontForge and clone the tested Nerd Fonts revision:

```sh
git clone https://github.com/ryanoasis/nerd-fonts.git /tmp/nerd-fonts
git -C /tmp/nerd-fonts checkout 33db50390a1b173e6f19ecc2119248d2ec166a11
NERD_FONTS_REPO=/tmp/nerd-fonts ./build-nerd-font.sh
NERD_FONTS_REPO=/tmp/nerd-fonts ./build-cjk90-nerd-font.sh
```

Each script builds Regular and Bold. Standard outputs are in `dist/nerd/`; the
spacing variant is in `dist/cjk90/nerd/`.

Third-party license texts are in `NerdFonts-Glyph-Licenses/`. The Nerd Fonts
license and license audit are in `LICENSE-Nerd-Fonts.txt` and
`NerdFonts-license-audit.md`. The audit notes that Font Logos has no declared
license; review its terms before redistributing the complete Nerd Font files.
The source font licenses are `LICENSE-Inconsolata.txt` and
`LICENSE-WenKai-Lite.txt`.
