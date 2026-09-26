# WenSolata Mono

WenSolata Mono combines Inconsolata Latin glyphs with LXGW WenKai Mono Lite
Chinese glyphs. It provides static Light, Regular, and Bold styles with
500-unit Latin and 1000-unit CJK advances. Inconsolata's instanced Latin outlines keep their
requested widths and are centered in the 500-unit cells without horizontal
rescaling.

Its Simplified Chinese localized family name is **慰文楷**.

## Styles

| Style | Inconsolata instance | WenKai Mono Lite source |
| --- | --- | --- |
| Light | `wdth=87.5`, `wght=300` | Light |
| Regular | `wdth=87.5`, `wght=350` | Regular |
| Bold | `wdth=90`, `wght=650` | Medium |

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

Discretionary ligatures are included as the `dlig` feature. Enable them in the
application that renders the font. For CSS:

```css
font-variant-ligatures: discretionary-ligatures;
```

## Chinese glyph spacing

Han, CJK radicals, and common CJK punctuation outlines are uniformly scaled to
90%. They are centered horizontally in their cells, while vertical scaling is
anchored at the baseline to keep their position aligned with Latin text. Light
and Regular use the corresponding WenKai outlines; Bold uses WenKai Medium
outlines. Their 1000-unit advances remain unchanged, so terminal column
alignment is preserved.

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

WenSolata Mono and its modified font files are distributed under the SIL Open
Font License 1.1. You may use, modify, embed, and redistribute them, including
commercially, provided you do not sell the font files by themselves, keep the
copyright and license notices, and release modified font files under OFL 1.1.
The WenKai source reserves `LXGW` and several Chinese names; this derivative
uses the distinct family names `WenSolata Mono` and `慰文楷`. The combined
license and notices are in [`OFL.txt`](OFL.txt), which includes both upstream
copyright and reserved-name notices. The build embeds the copyright notice and
full OFL text in each font's metadata.

See the [official OFL FAQ](https://openfontlicense.org/ofl-faq/) for details.

## Build

The build uses the sibling `Inconsolata` and `LxgwWenKai-Lite` checkouts.
Install the dependency and build all three weights:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./build-family.sh
```

This writes `dist/WenSolataMono-Light.ttf`, `dist/WenSolataMono-Regular.ttf`,
and `dist/WenSolataMono-Bold.ttf`. Install the TTF files with your operating
system's font manager or include them with an application. The family name is
`WenSolata Mono`; all three styles are static fonts.

The page templates live on the `pages-source` branch, separate from the font
sources on `main`. For a local web build, check out that branch and pass its
directory to the script:

```sh
git worktree add ../WenSolata-Pages pages-source
WEB_SOURCE="../WenSolata-Pages" ./build-webfonts.sh
```

This writes the generated site to `site/` and requires the WOFF2 extra in
`requirements.txt`.

## Web fonts

The Light, Regular, and Bold web fonts are WOFF2 files. Include the hosted stylesheet:

```html
<link rel="stylesheet" href="https://hanlhe.github.io/WenSolata-Mono/WenSolataMono.css">
```

Then use `WenSolata Mono` as the CSS font family. The stylesheet defines weights
300, 400, and 700. The web font files and `OFL.txt` are available in the
[GitHub Pages site](https://hanlhe.github.io/WenSolata-Mono/).

## Automated build and release

GitHub Actions rebuilds the Light, Regular, and Bold fonts from the pinned sources on
pushes, pull requests, and manual runs. The site templates are kept on
`pages-source`, and the workflow combines them with the generated WOFF2 files.
It publishes the WOFF2 files and CSS
to [GitHub Pages](https://hanlhe.github.io/WenSolata-Mono/) on pushes to `main`,
and creates a GitHub Release with the TTFs, web fonts, CSS, and `OFL.txt` when
a `v*` tag is pushed. The first release tag is `v4.622`.

WenKai's combining diacritics, variation sequence data, vertical metrics, and
OpenType layout tables are retained. Inconsolata's `dlig` feature is merged
into each style.
