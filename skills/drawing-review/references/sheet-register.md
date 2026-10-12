# Sheet register and revision comparison

## 1. Default register columns

Use the project's own register if it has one. Without one, use these columns in this order.

| Column | Meaning | Source |
|---|---|---|
| sheet_no | sheet number as printed in the title block | title block |
| title | sheet title | title block |
| discipline | discipline code or name | title block or project code list |
| rev | revision code, exactly as printed (letter, number, P01) | title block |
| status | status code (for example S0, AB, for construction) | title block, from the project code list |
| date | issue or revision date as printed | title block |
| scale | scale as printed ("1:50", "as shown", "NTS") | title block |
| paper | paper size (A0, A1, A2, A3, A4) or the measured page size | page geometry |
| drawn / checked / approved | initials from the title block | title block |
| file | file name, exactly as it is on disk | file system |
| pages | pages in the file, where one file holds several sheets | file |
| note | findings: missing field, name mismatch, unreadable, scanned | review |

Rules
- One row per sheet, not per file. A multi-sheet PDF gets one row per sheet with its page number in the note.
- Keep the revision code as printed. Do not normalise "rev B" to "B" or "B" to "2": the code is what the contract and the client use.
- Never merge two registers that use different code systems without saying so; report the discrepancy instead.
- A register is an index, not a summary. Do not add opinions to it; findings go in the note column and in the report.

## 2. Reading the title block

Read these from the sheet itself. The file name is a cross-check, not a source.

1. Sheet number: usually the largest field in the title block. Check its format against the project standard before accepting it.
2. Title: the sheet title, not the drawing content. Where the title and the content disagree (a "Ground floor ventilation" sheet showing first-floor ductwork), report it.
3. Revision and status: two separate fields in most systems (revision code, purpose of issue). A sheet can be at revision C, status "for construction", issued three times. Do not confuse them.
4. Date: the date of the current revision, not the original drawing date. Both are often on the sheet; take the one that belongs to the current revision and say which you took.
5. Scale: a bar scale is more reliable than a "1:100" text field, because the PDF may be plotted to a different size. If the plot scale matters, measure the bar scale.
6. Sheet size: measure the page geometry rather than trusting the printed size. A PDF at A1 plotted to A3 is common and breaks any measurement taken from the file.

## 3. Revision comparison

Three levels, cheapest first:

1. **Register comparison.** Compare the two registers by sheet number: added, removed, revision changed, status changed, title changed. Reliable if both registers were read from the sheets. Report it as a register-level result.
2. **Sheet comparison by overlay.** Where the client asks what changed on a sheet, open both revisions and compare the drawing content: dimensions, routes, schedules, equipment tags, notes. Report the changes found, and the areas not compared.
3. **Content comparison of extracted data.** Where the previous extraction exists (a schedule, a quantity list), compare values sheet by sheet. This is the strongest evidence but needs an extraction from both revisions.

Rules
- Never claim a change from the register alone (a revision code change means something changed, not what).
- A sheet removed from a set is a finding: it often means the scope moved to another sheet.
- A sheet with the same revision code but a different title or date is a finding: report it as a possible unrecorded change rather than assuming nothing changed.
- Report the comparison basis explicitly: revision code, date, or content.
- List the sheets that could not be compared and why (scanned, corrupted, missing, unreadable).

## 4. Package completeness check

Check the package against the client's drawing list or the BEP, not against what happens to be in the folder.

| Check | Result when it fails |
|---|---|
| Every required sheet is present | list the missing sheet numbers |
| Every sheet is at the current revision | list sheets at an earlier revision, with the revision found |
| No superseded sheet in the package | list the superseded files |
| Status code is the one required for this issue | list sheets with the wrong status |
| File names follow the project standard | defer to `project-standards`, list the failures |
| The transmittal list matches the folder contents | list the differences in both directions |
| Register matches the sheets | list the rows that disagree |

Rules
- The current revision is what the client's issue list says, or the highest revision on the sheet where no list exists. Say which basis you used.
- A missing sheet is reported by number and title, not as "some sheets are missing".
- Never state that a package is complete unless the required sheet list was supplied. Without it, report the contents of the package and say that completeness could not be judged.
