#!/usr/bin/env python3
"""Build a static Inconsolata + WenKai Mono Lite TTF."""

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parent
INCONSOLATA = (
    ROOT.parent
    / "Inconsolata/fonts/variable/Inconsolata[wdth,wght].ttf"
)
WENKAI = (
    ROOT.parent
    / "LxgwWenKai-Lite/fonts/TTF/LXGWWenKaiMonoLite-Regular.ttf"
)
FAMILY = "IncoWen Mono"
PREFIX = "IWInco_"
LIGATURE_PREFIX = "IWLig_"
LATIN_ADVANCE = 500
COMBINING_MARKS = range(0x0300, 0x0370)


def is_chinese_outline(cp):
    """Return True for Han, CJK radicals, and common CJK punctuation."""
    return (
        0x2E80 <= cp <= 0x2EFF
        or 0x2F00 <= cp <= 0x2FDF
        or 0x2FF0 <= cp <= 0x2FFF
        or 0x3000 <= cp <= 0x303F
        or 0x3200 <= cp <= 0x33FF
        or 0x3400 <= cp <= 0x4DBF
        or 0x4E00 <= cp <= 0x9FFF
        or 0xF900 <= cp <= 0xFAFF
        or 0x20000 <= cp <= 0x323AF
    )


def set_english_name(font, name_id, value):
    """Set the English Windows Unicode name record, replacing old one."""
    name_table = font["name"]
    name_table.names = [
        record for record in name_table.names if record.nameID != name_id
    ]
    name_table.setName(value, name_id, 3, 1, 0x0409)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cjk-scale-x", type=float, default=1.0)
    parser.add_argument(
        "--style", choices=("Regular", "Bold"), default="Regular"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 0 < args.cjk_scale_x <= 1:
        parser.error("--cjk-scale-x must be greater than 0 and at most 1")

    latin_axes = (
        {"wdth": 87.5, "wght": 350}
        if args.style == "Regular"
        else {"wdth": 90, "wght": 650}
    )
    if args.output is None:
        args.output = ROOT / "dist" / f"IncoWenMono-{args.style}.ttf"

    base = TTFont(WENKAI)
    latin = instantiateVariableFont(
        TTFont(INCONSOLATA),
        latin_axes,
        inplace=True,
    )

    # This optional optical-spacing variant narrows Han and CJK punctuation
    # outlines around the center of their full-width cells. Their 1000-unit
    # advances stay unchanged, keeping terminal columns aligned.
    cjk_glyph_names = {
        glyph_name
        for cp, glyph_name in base.getBestCmap().items()
        if is_chinese_outline(cp)
        and base["hmtx"].metrics[glyph_name][0] >= 800
    }
    cjk_scaled = 0
    if args.cjk_scale_x != 1.0:
        original_glyph_set = base.getGlyphSet()
        glyf = base["glyf"]
        hmtx = base["hmtx"].metrics
        em = base["head"].unitsPerEm
        x_offset = (1 - args.cjk_scale_x) * em / 2
        replacements = {}
        for glyph_name in cjk_glyph_names:
            recording_pen = DecomposingRecordingPen(original_glyph_set)
            original_glyph_set[glyph_name].draw(recording_pen)
            pen = TTGlyphPen(None)
            recording_pen.replay(TransformPen(
                pen,
                (args.cjk_scale_x, 0, 0, 1, x_offset, 0),
            ))
            replacements[glyph_name] = pen.glyph()
        for glyph_name, glyph in replacements.items():
            glyph.recalcBounds(glyf)
            glyf.glyphs[glyph_name] = glyph
            advance, _ = hmtx[glyph_name]
            hmtx[glyph_name] = (advance, glyph.xMin or 0)
        cjk_scaled = len(replacements)

    base_cmap = base.getBestCmap()
    latin_cmap = latin.getBestCmap()
    imported_cps = {
        cp: glyph_name
        for cp, glyph_name in latin_cmap.items()
        if cp != 0 and cp not in COMBINING_MARKS
    }
    source_glyph_names = sorted(set(imported_cps.values()))

    # Inconsolata's mapped glyphs have a 438-unit advance. Expand their
    # outlines to the 500-unit half-width cell used by the CJK mono font.
    source_glyph_set = latin.getGlyphSet()
    source_hmtx = latin["hmtx"].metrics
    source_cell = Counter(
        source_hmtx[name][0]
        for name in source_glyph_names
        if source_hmtx[name][0] > 0
    ).most_common(1)[0][0]
    scale_x = LATIN_ADVANCE / source_cell
    glyf = base["glyf"]
    hmtx = base["hmtx"].metrics
    converted_glyphs = {}

    def converted_glyph(source_name):
        if source_name not in converted_glyphs:
            recording_pen = DecomposingRecordingPen(source_glyph_set)
            source_glyph_set[source_name].draw(recording_pen)
            pen = TTGlyphPen(None)
            recording_pen.replay(
                TransformPen(pen, (scale_x, 0, 0, 1, 0, 0))
            )
            converted_glyphs[source_name] = pen.glyph()
        return converted_glyphs[source_name]

    # Reuse WenKai's glyph slots where their Unicode aliases are all being
    # replaced by the same Inconsolata glyph. This keeps the existing layout
    # rules attached to common glyph names such as A, eacute, and space.
    target_codepoints = {}
    target_aliases = {}
    for cp, target_name in base_cmap.items():
        target_aliases.setdefault(target_name, set()).add(cp)
    for cp, source_name in imported_cps.items():
        target_name = base_cmap.get(cp)
        if target_name is not None:
            target_codepoints.setdefault(target_name, []).append((cp, source_name))

    appended_source_names = set()
    appended_cmaps = {}
    for target_name, items in target_codepoints.items():
        source_names = {source_name for _, source_name in items}
        aliases = target_aliases[target_name]
        can_replace = (
            len(source_names) == 1
            and aliases.issubset(imported_cps)
            and all(imported_cps[cp] in source_names for cp in aliases)
        )
        if can_replace:
            source_name = next(iter(source_names))
            glyf.glyphs[target_name] = converted_glyph(source_name)
            source_advance, source_lsb = source_hmtx[source_name]
            hmtx[target_name] = (
                LATIN_ADVANCE if source_advance else 0,
                round(source_lsb * scale_x),
            )
        else:
            for cp, source_name in items:
                appended_source_names.add(source_name)
                appended_cmaps[cp] = PREFIX + source_name

    # Inconsolata also supplies a small number of codepoints absent from the
    # WenKai cmap; add those glyphs and point only those mappings at them.
    for cp, source_name in imported_cps.items():
        if cp not in base_cmap:
            appended_source_names.add(source_name)
            appended_cmaps[cp] = PREFIX + source_name

    # Bring over Inconsolata's discretionary ligature substitution and its
    # unencoded result glyphs. Inputs are resolved through Unicode so the
    # lookup follows any renamed glyph slots used by the merged cmap.
    source_gsub = latin["GSUB"].table
    dlig_record = next(
        record for record in source_gsub.FeatureList.FeatureRecord
        if record.FeatureTag == "dlig"
    )
    source_ligature_lookup = source_gsub.LookupList.Lookup[
        dlig_record.Feature.LookupListIndex[0]
    ]
    output_cmap = base.getBestCmap()
    reverse_source_cmap = {}
    for cp, glyph_name in latin_cmap.items():
        reverse_source_cmap.setdefault(glyph_name, []).append(cp)

    def merged_input_name(source_name):
        for cp in sorted(reverse_source_cmap.get(source_name, [])):
            output_name = output_cmap.get(cp)
            if output_name is not None:
                return output_name
        return source_name

    ligature_glyph_names = set()
    for subtable in source_ligature_lookup.SubTable:
        for source_ligature_name_list in subtable.ligatures.values():
            for ligature in source_ligature_name_list:
                ligature_glyph_names.add(ligature.LigGlyph)
    ligature_order = [
        LIGATURE_PREFIX + name for name in sorted(ligature_glyph_names)
    ]
    for source_name in sorted(ligature_glyph_names):
        target_name = LIGATURE_PREFIX + source_name
        glyf.glyphs[target_name] = converted_glyph(source_name)
        source_advance, source_lsb = source_hmtx[source_name]
        hmtx[target_name] = (
            round(source_advance / source_cell) * LATIN_ADVANCE,
            round(source_lsb * scale_x),
        )

    dlig_lookup = deepcopy(source_ligature_lookup)
    for subtable in dlig_lookup.SubTable:
        remapped = {}
        for first_source_name, ligature_list in subtable.ligatures.items():
            first_name = merged_input_name(first_source_name)
            remapped_ligatures = []
            for ligature in ligature_list:
                ligature.Component = [
                    merged_input_name(name) for name in ligature.Component
                ]
                ligature.LigGlyph = LIGATURE_PREFIX + ligature.LigGlyph
                remapped_ligatures.append(ligature)
            remapped.setdefault(first_name, []).extend(remapped_ligatures)
        subtable.ligatures = remapped

    gsub = base["GSUB"].table
    lookup_index = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(dlig_lookup)
    feature = deepcopy(dlig_record.Feature)
    feature.LookupListIndex = [lookup_index]
    new_feature_record = deepcopy(dlig_record)
    new_feature_record.Feature = feature
    feature_records = gsub.FeatureList.FeatureRecord
    insert_at = next(
        (i for i, record in enumerate(feature_records)
         if record.FeatureTag > "dlig"),
        len(feature_records),
    )
    feature_records.insert(insert_at, new_feature_record)

    # Feature indices in every LangSys shift after inserting dlig. Expose the
    # discretionary feature in the default DFLT and Latin language systems.
    for script_record in gsub.ScriptList.ScriptRecord:
        script = script_record.Script
        lang_systems = ([script.DefaultLangSys] if script.DefaultLangSys else [])
        lang_systems += [record.LangSys for record in script.LangSysRecord]
        for lang_sys in lang_systems:
            lang_sys.FeatureIndex = [
                index + (index >= insert_at) for index in lang_sys.FeatureIndex
            ]
            if lang_sys.ReqFeatureIndex != 0xFFFF and lang_sys.ReqFeatureIndex >= insert_at:
                lang_sys.ReqFeatureIndex += 1
        if script_record.ScriptTag in ("DFLT", "latn") and script.DefaultLangSys:
            script.DefaultLangSys.FeatureIndex.append(insert_at)
            script.DefaultLangSys.FeatureIndex.sort()

    for source_name in sorted(appended_source_names):
        target_name = PREFIX + source_name
        glyf.glyphs[target_name] = converted_glyph(source_name)
        source_advance, source_lsb = source_hmtx[source_name]
        hmtx[target_name] = (
            LATIN_ADVANCE if source_advance else 0,
            round(source_lsb * scale_x),
        )

    # Update cmap tables only for glyphs that needed separate slots. The
    # combining marks and any non-Latin aliases keep their original mappings.
    for subtable in base["cmap"].tables:
        if subtable.format == 14:
            continue
        for cp, target_name in appended_cmaps.items():
            if subtable.format == 4 and cp > 0xFFFF:
                continue
            subtable.cmap[cp] = target_name

    old_order = base.getGlyphOrder()
    appended_order = [PREFIX + name for name in sorted(appended_source_names)]
    new_order = list(dict.fromkeys(old_order + appended_order + ligature_order))
    base.setGlyphOrder(new_order)
    for glyph_name in new_order:
        if glyph_name not in base["hmtx"].metrics:
            source_name = glyph_name.removeprefix(PREFIX)
            source_advance, source_lsb = source_hmtx[source_name]
            base["hmtx"].metrics[glyph_name] = (
                LATIN_ADVANCE if source_advance else 0,
                round(source_lsb * scale_x),
            )
        if "vmtx" in base and glyph_name not in base["vmtx"].metrics:
            glyph = glyf[glyph_name]
            glyph.recalcBounds(glyf)
            vertical_origin = round(base["head"].unitsPerEm * 0.88)
            base["vmtx"].metrics[glyph_name] = (
                base["head"].unitsPerEm,
                vertical_origin - (glyph.yMax or 0),
            )
    base["maxp"].numGlyphs = len(new_order)
    base["hhea"].numberOfHMetrics = len(new_order)

    # Include the imported outlines in the global head bounds.
    boxes = [(base["head"].xMin, base["head"].yMin,
              base["head"].xMax, base["head"].yMax)]
    for glyph_name in list(target_codepoints) + appended_order + ligature_order:
        glyph = glyf[glyph_name]
        glyph.recalcBounds(glyf)
        if glyph.xMin is not None:
            boxes.append((glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax))
    if boxes:
        head = base["head"]
        head.xMin = min(box[0] for box in boxes)
        head.yMin = min(box[1] for box in boxes)
        head.xMax = max(box[2] for box in boxes)
        head.yMax = max(box[3] for box in boxes)

    # The base font's layout tables refer to its original glyphs and remain
    # valid. Remove any stale signature before saving modified font data.
    if "DSIG" in base:
        del base["DSIG"]

    names = {
        1: FAMILY,
        2: args.style,
        3: f"{FAMILY} {args.style} 1.0",
        4: f"{FAMILY} {args.style}",
        5: "Version 1.0",
        6: FAMILY.replace(" ", "") + f"-{args.style}",
        16: FAMILY,
        17: args.style,
    }
    for name_id, value in names.items():
        set_english_name(base, name_id, value)
    base["head"].fontRevision = 1.0
    if args.style == "Bold":
        base["head"].macStyle |= 1
    else:
        base["head"].macStyle &= ~1
    base["OS/2"].achVendID = "IWKM"
    base["OS/2"].usWeightClass = 700 if args.style == "Bold" else 400
    base["OS/2"].fsSelection &= ~((1 << 5) | (1 << 6))
    base["OS/2"].fsSelection |= 1 << (5 if args.style == "Bold" else 6)
    # WenKai marks both legacy Chinese code pages as functional. This family
    # uses its Simplified Chinese glyph forms, so advertise Simplified only.
    base["OS/2"].ulCodePageRange1 |= 1 << 18
    base["OS/2"].ulCodePageRange1 &= ~(1 << 20)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    base.save(args.output)
    print(f"Wrote {args.output}")
    print(
        f"Replaced Latin and symbol glyphs for {len(imported_cps)} "
        f"codepoints; added {len(appended_source_names)} Latin and "
        f"{len(ligature_order)} ligature glyphs; added the dlig feature. "
        f"Inconsolata axes are {latin_axes}; style is {args.style}. "
        f"Latin advances are {LATIN_ADVANCE}/{base['head'].unitsPerEm} em "
        f"(scaled {scale_x:.3f}x horizontally). "
        f"Scaled {cjk_scaled} Chinese glyph outlines "
        f"({args.cjk_scale_x:.3f}x horizontally); their advances are unchanged."
    )


if __name__ == "__main__":
    main()
