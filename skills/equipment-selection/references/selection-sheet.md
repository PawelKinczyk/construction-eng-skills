# Selection sheet format

Write section headings in the deliverable language. Keep the order.

```markdown
# Selection sheet: <equipment tag> <equipment type>

Project: <project_name> (<project_number>)   Date: <YYYY-MM-DD>   Prepared by: agent, for review by <engineer>
Status: draft for engineer review

## 1. Summary
One to three sentences: what was selected, for which duty, and the main open point.

## 2. Design duty
| Parameter | Value | Unit | Source |
|---|---|---|---|
| e.g. Heat load | 120 | kW | heat load calc rev B |
| Flow | 5.25 | m³/h | hvac_calc water-flow |
| Head incl. margin | 6.6 | m | 6.0 m calculated + 10 % |

## 3. Calculation
Script commands and key results, or a table of the index circuit:
| Segment / component | Flow | Size | Δp | Source |
|---|---|---|---|---|
Total and margin applied, with reason.

## 4. Requirements
| Requirement | Value | Source |
|---|---|---|
| e.g. Ecodesign | EEI ≤ 0.23 (circulators) | Reg. (EC) 641/2009, EUR-Lex |
| Electrical supply | 1~230 V | PROJECT.md |
| Noise | ≤ 35 dB(A) in plant room door | client brief |

## 5. Selected unit
| Item | Value |
|---|---|
| Manufacturer / model | <or "to select"> |
| Duty point on curve | flow, head, efficiency at duty |
| Power input | |
| Dimensions / weight | |
| Connections | |
| Controls | |
| Data source | data sheet name, revision/date, URL |

## 6. Alternatives
| Option | Model | Key difference | Trade-off |
|---|---|---|---|

## 7. Assumptions
- Every assumed value, with reason.

## 8. Sources
- Laws (official government sources only), standards (number, edition, clause), data sheets, project documents.

## 9. To verify
- [ ] Items the engineer must confirm before the selection is final.
```
