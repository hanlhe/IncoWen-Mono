# IncoWen Mono

IncoWen Mono combines Inconsolata Latin glyphs with LXGW WenKai Mono Lite
Chinese glyphs. It provides static Regular and Bold styles with 500-unit Latin
and 1000-unit CJK advances. Inconsolata's instanced Latin outlines keep their
requested widths and are centered in the 500-unit cells without horizontal
rescaling.

## Styles

| Style | Inconsolata instance |
| --- | --- |
| Regular | `wdth=87.5`, `wght=350` |
| Bold | `wdth=90`, `wght=650` |

The Inconsolata source has no italic files or italic/slant axis, so this family
does not include Italic or Bold Italic. No synthetic slant is applied.

## Source versions

The build pins the two source repositories to these revisions:

| Source font | Font version | Source revision |
| --- | --- | --- |
| Inconsolata | 3.100 | [`fc1fc210`](https://github.com/cyrealtype/Inconsolata/commit/fc1fc21081558b39a2db43bfd9b65bf9acb50701) |
| LXGW WenKai Mono Lite | 1.522 | [`4cddacbe`](https://github.com/lxgw/LxgwWenKai-Lite/commit/4cddacbe244b0a24b10076369105f0495e5ec898) |

The combined release version is their sum (`3.100 + 1.522 = 4.622`), following
the convention used by [LXGW Bright Code](https://github.com/lxgw/LxgwBright-Code).
The first release tag is `v4.622`.

Discretionary ligatures are included as the `dlig` feature. Enable discretionary
ligatures in your editor to use them. For CSS:

```css
font-variant-ligatures: discretionary-ligatures;
```

## Chinese glyph spacing

Han, CJK radicals, and common CJK punctuation outlines are uniformly scaled to
90%, centered in their cells. This adds space around each character while
preserving its proportions. Their 1000-unit advances remain unchanged, so
terminal column alignment is preserved.

## Chinese language metadata

The merged fonts mark their design and supported scripts as Latin and
Simplified Han (`Latn,Hans`) in the OpenType `meta` table. They also set the
Simplified Chinese OS/2 code-page flag (936) and clear the Traditional Chinese
flag (950). These fields classify the CJK coverage; they do not change the
glyph outlines.
OpenType defines these code-page flags in the
[OS/2 table specification](https://learn.microsoft.com/en-us/typography/opentype/spec/os2#ulcodepagerange).
The `dlng` and `slng` tags are described in the
[OpenType `meta` table specification](https://learn.microsoft.com/en-us/typography/opentype/spec/meta).

## License

IncoWen Mono and its modified font files are distributed under the SIL Open
Font License 1.1. You may use, modify, embed, and redistribute them, including
commercially, provided you do not sell the font files by themselves, keep the
copyright and license notices, and release modified font files under OFL 1.1.
The WenKai source reserves `LXGW` and several Chinese names; this derivative
uses the distinct family name `IncoWen Mono`. The combined license and notices
are in [`OFL.txt`](OFL.txt), which includes both upstream copyright and
reserved-name notices. The build embeds the copyright notice and full OFL text
in each font's metadata.

See the [official OFL FAQ](https://openfontlicense.org/ofl-faq/) for details.

## Build

The build uses the sibling `Inconsolata` and `LxgwWenKai-Lite` checkouts.
Install the dependency and build both standard weights:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./build-family.sh
```

This writes `dist/IncoWenMono-Regular.ttf` and
`dist/IncoWenMono-Bold.ttf`. Install the TTF files with your operating system's
font manager or include them with an application. The family name is
`IncoWen Mono`; both weights are static fonts.

## Automated build and release

GitHub Actions rebuilds the Regular and Bold TTFs from the pinned sources on
pushes, pull requests, and manual runs, then uploads a ZIP artifact containing
the fonts and `OFL.txt`. Pushing a `v*` tag creates a GitHub Release with
that ZIP. The first release tag is `v4.622`.

WenKai's combining diacritics, variation sequence data, vertical metrics, and
OpenType layout tables are retained. Inconsolata's `dlig` feature is merged
into each style.
