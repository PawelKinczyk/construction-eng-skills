---
name: dxf-dwg-analysis
description: Read CAD files without opening CAD - DXF and DWG layers (names, states, entity counts per layer), blocks and their insert counts, block attributes, entity type counts, drawing extents and units, text and notes on layers, and a revision comparison between two files. Use when the user asks to analyse a DXF or DWG, count blocks or symbols (sockets, sprinklers, diffusers, doors), list layers or check layer standards, extract attributes (room numbers, equipment tags), check drawing units or extents, compare two CAD issues for changes, or find out what is in a CAD file without a CAD seat.
---

# DXF and DWG analysis

Goal: counts, layer and block data taken from the file itself, with the file, the units and the comparison basis stated. The output is data another engineer can check, not a drawing.

Python with `ezdxf` is required for every analysis here. DWG files must first be converted to DXF (ODA File Converter); only DXF is read directly.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, disciplines, deliverable language, section "Project standards" (layer naming rules, block naming rules, units convention).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for the deliverable language and the layer or block standard in use.
- Load `references/shared/disciplines/<discipline>.md` for what the blocks and layers mean in that discipline.
- Load `references/dxf-reading.md` (this skill) for units, model space versus paper space, blocks, attributes, xrefs and what the file cannot tell you.
- Layer and block naming rules are `project-standards`. This skill reports what is in the file; it does not decide whether a name is compliant.

## 2. Collect inputs

1. **The file or files.** One file for a report, two for a revision comparison. Ask for the issue date and revision of each.
2. **What is wanted**: layer list, block counts, attributes, text extraction, units and extents, or a comparison. Ask, do not guess - a full dump of a large file is unreadable.
3. **Conversion.** For DWG: is the ODA File Converter installed, and where? Without it, ask the user to convert, or to supply DXF.
4. **Filters.** Which layers, block names or attribute tags matter. For a big file, filter instead of dumping everything.
5. **Cross-check.** The sheet register (`drawing-review`) or the schedule the counts will be compared with.

## 3. Work

1. **Check the file.** Run the summary first, and read the units and the extents before any count. A file with a wrong unit or a stray entity a kilometre away corrupts every other number.
   ```
   python scripts/dxf_report.py summary --file A-101.dxf
   python scripts/dxf_report.py layers --file A-101.dxf --csv layers.csv
   python scripts/dxf_report.py blocks --file A-101.dxf --attributes
   python scripts/dxf_report.py text --file A-101.dxf --pattern "SAP|DSO|wentylacja"
   python scripts/dxf_report.py diff --old revB.dxf --new revC.dxf
   ```
2. **Layers.** List the layers with their state (on, off, frozen, locked) and the entity count on each. Compare with the project layer standard and report the differences as findings: layers not in the standard, standard layers missing, entities on the wrong layer where the file shows it (for example dimensions on a construction layer).
3. **Blocks.** Count block references by name, and read the attributes of each insert (room number, tag, type). Give the counts per layer and per block name. State whether the file uses anonymous blocks (dimensions, hatches) which must be excluded from the count.
4. **Text.** Extract text and mtext with the layer and position, filtered by the user's pattern. Text in a CAD file is often duplicated or on a layer that is off: report what is in the file, not what was plotted.
5. **Revision comparison.** Compare the two files: layers added or removed, entity count change per layer, block count change per block name, and attribute changes where the block insert count is the same. Report a change to a layer count as a change, and say that the file cannot show what a line means - that reading needs the drawing.
6. **DWG.** Convert first, then run the same commands:
   ```
   # example, adjust the paths to the installed converter
   "C:\Program Files\ODA\ODAFileConverter\ODAFileConverter.exe" <in_folder> <out_folder> ACAD2018 DXF 0 1
   ```
   Record the converter version and the output format in the report.

## 4. Verify

- Units: read `$INSUNITS` and state it. If it is unset or wrong, say so; do not assume millimetres.
- Extents: check for entities far outside the drawing area before trusting any area or length. Report them; they usually mean a stray object or an inserted drawing at the wrong scale.
- Counts: state the entity types counted, and whether paperspace is included (default: no).
- Xrefs: list unresolved xrefs. A count without them is a count of part of the drawing.
- Proxies and missing custom objects: report their count, because their content is not readable and the counts may be low.
- Attribute values: read from the file, no cleaning. Empty or duplicated tags are findings.
- Revision comparison: state the two files with their dates or revisions, and that the comparison is of file content, not of the drawing's meaning.
- Typical drawings: never take a quantity for an order, a price or a selection straight from the counts. Route it to `cost-estimate` or `equipment-selection`, and say the count needs a check against the drawing.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default Markdown; on request `.csv` or `.xlsx`.

1. **Summary**: file(s) analysed, units, drawing extents, entity and block totals, the three findings that matter.
2. **Layers**: table with layer name, state, entity count, standard status, note.
3. **Blocks**: table with block name, insert count, layers used, attribute tags, note; a separate attribute table when the user needs the values.
4. **Text extracted**: table with text, layer, position, sheet or layout.
5. **Revision comparison**: layers and counts added, removed, changed; attribute changes; what could not be compared.
6. **Findings**: units, stray entities, unresolved xrefs, proxy objects, layer standard differences.
7. **To verify**: items needing a visual check in CAD, counts to confirm against the drawing, converted-from-DWG notes.

## Rules

- Read only. Never modify, purge, explode, save or convert-in-place a user's file. Write output to new files only.
- Do not invent layer names, block names, counts or attribute values. If a value is absent, say it is absent.
- A count from a CAD file is evidence, not a measurement: it counts what is drawn, including mistakes and duplicates.
- DWG conversion is a copy, not a repair. A file that fails to convert perfectly is reported as such, with the converter version used.
- State the file name, size, date and the tool version in every report.
