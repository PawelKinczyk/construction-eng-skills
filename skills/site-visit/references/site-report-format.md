# Site visit report: structure and photo rules

## 1. Report structure (short form and full form)

Use the short form for a routine visit, the full form for an inspection, a handover or an incident.

| Section | Short form | Full form |
|---|---|---|
| Identification | yes | yes |
| Summary (3-5 lines) | yes | yes |
| Present on site | yes | yes |
| Weather and site conditions | yes | yes |
| Progress | yes | yes, per activity |
| Observations by area or level | yes | yes, per area, numbered |
| Safety | yes | yes, per area |
| Quality and defects | list | list with severity and owner |
| Materials, deliveries, plant | optional | yes |
| Instructions and agreements | yes | yes, with the person and whether written |
| Items to follow up | yes | yes, with owner and date |
| Photos | list | list, numbered, one line each |
| Not visited / not recorded | yes | yes |
| Next visit | yes | yes |

## 2. Identification block

```
Report: <project prefix>-SV-<number>          Date: <YYYY-MM-DD>
Project: <name and number>                    Time on site: <from> - <to>
Visitor: <name - company - role>
Purpose: routine visit / inspection / handover / incident / authority visit
Weather: <dry, rain, temperature if it matters>   Site conditions: <mud, frost, dust, wind>
Distribution: <who this goes to>
```

Rules
- The number comes from the project register. If it is not known in the field, write `SV-<date>` provisionally and say it must be renumbered in the office.
- Weather is recorded when it affects the work: concreting, earthworks, coatings, scaffolding, crane operations, temporary works.

## 3. Observations

One numbered item per observation. Each item carries:

```
O-<n>  Area / level: <grid, storey, room>   Time: <HH:MM>   Photos: <7, 8>
What was seen: <fact>
Measured or estimated: <if a number is given>
Conclusion: <only if it follows directly, and marked as a conclusion>
Action: <who was told, what was agreed, or "reported to the office">
```

Rules
- One observation per item. Two observations in one item get one follow-up and the other is forgotten.
- Photo numbers let a reader find the evidence. A photo with no date or no location is flagged.
- An impression is recorded as an impression: "the void looks too shallow for the duct" is a concern, not a measurement, and it is listed under items to verify.
- A measurement states the method and the accuracy: "measured with a tape, ±5 mm".
- Do not record a conclusion as an observation. "Insulation missing at the valve" is a conclusion from "the insulation ends 300 mm before the valve" - keep the fact and, if useful, the conclusion separately.

## 4. Safety section

Record what was seen, per area and time:

| Item | What to look at |
|---|---|
| Access and edges | edge protection, openings, covers, ladders |
| Work at height | scaffolds with valid tags, harnesses, mobile towers |
| Personal protective equipment | helmets, footwear, eye and hearing protection in use |
| Housekeeping | debris, trailing cables, blocked routes, waste separation |
| Temporary works | formwork, props, excavations with supports and access |
| Plant and lifting | lifting plans, banksman, exclusion zones, certificates on the machine |
| Hot works and permits | permits issued, fire watch, extinguisher at the work place |
| Temporary electrics | distribution boards, RCDs, cable protection, overloads |
| Welfare | toilets, water, shelter, first aid, site tidiness |
| Signage | barriers, warnings, emergency routes, contact numbers |

Rules
- A safety observation states place, time and what was seen. No blame, no adjectives, no speculation about consequences.
- A serious or imminent danger is reported to the person responsible on site at the time, and the report says who was told and when. If the danger is still present, the agent's first sentence tells the user to inform the person responsible on site (the site manager) now, before any drafting; the report is not the notification. Record who and when once known, otherwise "not recorded".
- Never soften a safety observation because the report goes to the contractor.

## 5. Quality and defects

Items here are the input to `punch-list`. Per item: location, element, trade, description, severity, photo number, who was told.

| Severity | Meaning |
|---|---|
| A | safety-critical or structurally significant; stop and report immediately |
| B | functional, will not work as designed or will not be accepted |
| C | cosmetic or minor; fix before handover |
| D | observation, no action agreed |

Rules
- A defect is described by the requirement it fails where that is known (document, clause, tolerance), and by what was seen. If the requirement is not at hand, describe the fact.
- Never record a defect you did not see. "Reported by the site manager" is attributed, not adopted.
- An item that is a design question rather than a defect goes to the designer, not to the defect list.

## 6. Instructions and agreements

```
Who instructed: <name, company>
To whom: <name, company>
What: <one line>
Written or verbal: <written, with the document number and date, or verbal - needs confirming in writing>
Effect noted: <time, cost, design, safety - if stated at the time; otherwise "not stated">
```

Rules
- A verbal instruction is recorded as verbal and flagged for written confirmation. Send it the same day: documents produced later in the day are still contemporaneous evidence, documents produced next month are not.
- Do not record your own instruction as agreed unless the other side agreed. "We asked for X" and "they agreed to X" are different lines.
- An instruction that changes scope, cost or time is routed to `project-correspondence` as a change request or a notice.

## 7. Photo rules

- Number the photos in the report (`Photo 1`, `Photo 2`) and refer to the numbers in the observations.
- One line per photo in the photo list: number, area, subject, time if known.
- Do not edit photo content, and never delete one that shows a problem. Keep the originals in the project record.
- A photo taken without a scale (a tape, a person, a known object) is a poor record for a defect claim: say so.
- A close-up without a wider view is hard to place later: ask for both, or note which is missing.
- Screenshots, chat photos forwarded from site, and photos from another date are labelled as such. They are not evidence of what was seen during this visit.

## 8. Items to follow up

| # | Item | Owner | Due | Route to |
|---|---|---|---|---|
| 1 | | | | correspondence / punch-list / meeting-minutes / design |

Rules
- Every observation that needs action produces one row.
- The route matters: an RFI goes to `project-correspondence`, a defect to `punch-list`, a decision to `meeting-minutes`, a design question to the designer with a written record.
- An item with no owner is a note, not a follow-up. Write "owner not assigned" explicitly.

## 9. What a site report is not

It is not a notice, not an instruction, not an acceptance, not a certificate of payment, not a design decision, and not proof of the cause of a defect. Where the visit concerns one of those, say so in the summary and route it to the document that does the job.
