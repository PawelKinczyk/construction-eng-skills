# What can be extracted from a PDF, and how

## 1. Two kinds of PDF

| Kind | How to tell | What works |
|---|---|---|
| Vector (plotted from CAD or BIM) | text is selectable, file is small, lines are crisp at any zoom | text extraction gives the title block and most notes and schedules |
| Scanned or image-based | text is not selectable, file is large, lines are raster | only the agent reading the image; text extraction returns nothing |

Check first, then choose the method. A mixed set (vector sheets plus scanned as-builts) is common: report which sheets are which rather than treating the whole set the same way.

## 2. Working without Python

The agent reads PDFs directly, which is the right method for:
- one drawing, a few sheets, or a question about a specific sheet;
- title block fields and schedules read from a vector PDF;
- scanned drawings, where reading the image is the only option;
- checking a package list against folder contents.

Limits to state in the output: a value read from a low-resolution scan is a visual reading, not an extraction. Say so, and ask the user to confirm critical numbers (dimensions, quantities, ratings).

## 3. Working with Python

`scripts/pdf_register.py` is for bulk work over a folder. It reads text with the first available of:
1. `pypdf` (pure Python, `pip install pypdf`);
2. `pdftotext` from Poppler, if it is on the PATH;
3. nothing - then the script stops and says which dependency to install.

The script never interprets: it extracts text and page geometry, and applies the patterns you give it.

```
python scripts/pdf_register.py scan --dir drawings --recursive --rules rules.json --csv register.csv
python scripts/pdf_register.py titles --file drawings/A-101.pdf [--pages 1]
python scripts/pdf_register.py compare --a register-revB.csv --b register-revC.csv
```

## 4. Rules file for the scan

Field detection is project-specific, so the script takes a JSON of regular expressions instead of guessing. Write one per project and keep it next to the register.

```json
{
  "sheet_no": "\\b([A-Z]{1,3}-[0-9]{3,4})\\b",
  "title": "\\bTITLE[:.]?\\s*([^\\n]{3,60})",
  "rev": "\\bRev[:.]?\\s*([A-Z0-9]{1,3})\\b",
  "status": "\\bStatus[:.]?\\s*([A-Z0-9]{2,8})\\b",
  "date": "\\b([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})\\b",
  "scale": "\\b1:[0-9]{1,4}\\b"
}
```

Rules
- Allowed keys: `sheet_no`, `title`, `rev`, `status`, `date`, `scale`; any other key is rejected (exit 2). Limit the status length to the codes the project uses (IFC, S2, TENDER).
- Write each backslash twice in JSON (`\\b` in the file is the regex `\b`). Copied text with four backslashes matches nothing.
- The first capture group is the value.
- Patterns match on the whole first-page text (or the page text, with `--pages`). Nothing else is inferred.
- A field with no match stays empty in the register and is marked `missing` in the note column. Never fill it from the file name or from another sheet. A rule that matches 0 of N sheets also prints a `WARNING` on stderr: treat it as a rules problem first (escaping, wording of the title block), not as a drawing problem.
- Test the rules on a few sheets before scanning a whole set, and record which sheets they were tested on.

## 5. What extraction cannot do

- It cannot tell whether a value is correct, current, or consistent with another sheet. That is a review, not an extraction.
- It cannot measure geometry reliably. Plotted scale, paper size and line weights all change the result. For quantities, use `dxf-dwg-analysis` or `ifc-analysis`.
- It cannot read text converted to curves or outlines (common in older sets). Those sheets need the agent's visual reading.
- It cannot see the drawing content: a changed dimension inside a drawing is not text, so revision comparison of content is a visual or overlay job, and its result must say which areas were compared.
- It cannot detect a hidden layer: a PDF contains what was plotted, so a switched-off layer is simply absent. If a sheet looks incomplete, ask for the CAD or the model.

## 6. Reporting extracted data

Every extracted value goes out with: sheet number, revision, page, and where on the sheet it sits (title block field, schedule row, note number). A table of values without that chain cannot be checked, and will be rejected by a reviewer.

Where the extraction is used for a decision (a quantity for an order, a rating for a selection), say so and route the decision to the skill that owns it: `cost-estimate` for quantities and prices, `equipment-selection` for equipment, `code-compliance` for requirements.
