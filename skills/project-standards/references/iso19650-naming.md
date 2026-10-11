# ISO 19650 information container naming

Use this as the default when a project has no own naming standard, or as the base for writing one.
ISO 19650-2 defines the fields. The codes below follow the **UK National Annex** (BS EN ISO 19650-2 NA), the most widely used code set.
Other countries and projects change codes and field lengths. The project BEP always wins.

## Fields

`PROJECT-ORIGINATOR-VOLUME-LEVEL-TYPE-ROLE-NUMBER`

| Field | Meaning | Typical format | Examples |
|---|---|---|---|
| Project | project code | 2–6 characters | `ZB2`, `NHS01` |
| Originator | company that produces the file | 3–6 characters | `PKS`, `ARUP` |
| Volume / system | building, zone or system | 1–2 characters | `B2`, `01`, `ZZ` (all), `XX` (none) |
| Level / location | storey or location | 2 characters | `00`, `01`, `B1`, `RF`, `ZZ`, `XX` |
| Type | information type | 2 characters | see below |
| Role | discipline | 1 character | see below |
| Number | sequence number | 4–6 digits | `0001`, `000123` |

Status and revision are metadata in the common data environment (CDE). Many projects still append them to the file name, for example `_S2_P01`. Follow the BEP.

## Type codes (UK NA)

| Code | Type | Code | Type |
|---|---|---|---|
| AF | animation | MR | model rendition |
| BQ | bill of quantities | MS | method statement |
| CA | calculations | PP | presentation |
| CM | combined model | PR | programme |
| CO | correspondence | RD | room data sheet |
| CP | cost plan | RI | request for information |
| CR | clash rendition | RP | report |
| DB | database | SA | schedule of accommodation |
| DR | drawing | SH | schedule |
| FN | file note | SN | snagging list |
| HS | health and safety | SP | specification |
| IE | information exchange file | SU | survey |
| M2 | 2D model | VS | visualisation |
| M3 | 3D model | MI | minutes, action notes |

## Role codes (UK NA)

| Code | Role | Code | Role |
|---|---|---|---|
| A | architect | L | landscape architect |
| B | building surveyor | M | mechanical engineer |
| C | civil engineer | P | public health engineer |
| D | drainage, highways engineer | Q | quantity surveyor |
| E | electrical engineer | S | structural engineer |
| F | facilities manager | T | town and country planner |
| G | geographical and land surveyor | W | contractor |
| H | heating and ventilation designer | X | subcontractor |
| I | interior designer | Y | specialist designer |
| K | client | Z | general (non-disciplinary) |

## Status codes (UK NA, common)

| Code | Meaning |
|---|---|
| S0 | work in progress |
| S1 | suitable for coordination |
| S2 | suitable for information |
| S3 | suitable for review and comment |
| S4 | suitable for stage approval |
| S6 | suitable for PIM authorisation |
| S7 | suitable for AIM authorisation |
| A1, A2… | authorised and accepted (stage) |
| B1, B2… | partially signed off, with comments |
| CR | as construction record |

## Revision codes (common)

- `P01`, `P02`…: preliminary (WIP and shared).
- `P01.1`, `P01.2`…: WIP sub-versions inside the team.
- `C01`, `C02`…: contractual (published, authorised).

## Notes for Poland and other countries

- PN-EN ISO 19650 is adopted in Poland. There is no Polish national annex with code sets. Projects define codes in the BEP or the client's standard.
- Polish projects often use Polish discipline letters, for example `S` sanitarne, `E` elektryczne, `K` konstrukcja, `A` architektura. Here `S` has a different meaning than in the UK NA. Always read the project rule set; never mix code sets.
