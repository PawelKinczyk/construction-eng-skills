---
name: site-visit
description: Record a site visit or an inspection from photos, dictation and notes, on a phone or on a computer - progress against the programme, works done and resources, weather and conditions, materials and deliveries, safety and quality observations, deviations from the design, instructions given or received, defects and the next steps. Produces a site visit report ready to send, and a list of items to follow up. Use when the user asks to write up a site visit or an inspection, describe what they saw on site, turn site photos and a voice note into a report, record an inspection for an authority or an insurer, or prepare a site diary entry.
---

# Site visit

Goal: a report of what was actually there, from the photos and the visitor's own words, in a form that can be sent the same day and quoted later. Facts and observations; no conclusions that the evidence does not support.

This skill is built for a phone: no scripts, no files to process. The agent reads the photos, takes the dictation or the notes, and writes the report. The desktop is used afterwards for `.docx` and for adding documents.

## 1. Load context

- Read `PROJECT.md` if it is available: project, jurisdiction, role of the visitor, deliverable language, the report template and the numbering of site visit reports.
- On a phone in the field, `PROJECT.md` is often not at hand: ask for the project name or number, the visitor's name and company, and the visit date. Say that the report will need the project's numbering checked afterwards.
- Load `references/shared/disciplines/<discipline>.md` for what is worth looking at and recording in that discipline (what is inspected at which stage, which observations matter).
- Load `references/site-report-format.md` (this skill) for the report structure and the photo rules.
- Load `references/mobile-workflow.md` (this skill) for working from a phone: dictation, photo batches, no signal, long visits, and what to defer to the desktop.

## 2. Collect inputs

Draft first, then ask. Ask at most 3 questions per message (a phone user will not answer a long list), the minimum needed for the report; everything else becomes "not recorded" ("nie zarejestrowano"). The items below are what a complete report needs, not a questionnaire:

1. **Visit facts**: date, time on site, weather (dry or rain, temperature if relevant), who was present, purpose (routine visit, inspection, handover, incident).
2. **Photos**: in batches, with the area or the level they show. Photos carry date and time in most phone cameras; do not retype what the photo shows, describe what it means.
3. **The visitor's words**: dictation, notes, a voice memo transcript. This is the primary content; the photos are evidence.
4. **Progress reference**: the programme activity or the milestone the visit relates to, if progress is being reported.
5. **What was agreed or instructed on site**: by whom, to whom, and whether it was written down.
6. **Whether the report goes to someone**: the client, the authority, the insurer, or the office file. That decides the tone and the amount of background.

Missing inputs are named in the report as "not recorded", never filled in. When there is almost no data (for example a voice note not yet supplied), show the short-form skeleton with every field "not recorded" together with the questions, and state that the site report is not an instruction, a notice or an acceptance.

## 3. Work

1. **Structure the report** per `references/site-report-format.md`: identification, visit facts, progress, observations by area, safety, quality and defects, materials and deliveries, instructions and agreements, items to follow up, photos, next visit.
2. **Take the visitor's words as the source of the report.** Rewrite for clarity and keep the meaning; do not add observations. Where a statement is an impression ("the ductwork looks tight to the ceiling"), record it as an impression, and say whether it was measured.
3. **Describe each photo** in one line per photo: area, what it shows, and the finding. Number photos and refer to the numbers in the text.
4. **Separate what was seen from what was concluded.** "The pipe insulation ends 300 mm before the valve" is an observation; "the insulation is incomplete" is a conclusion; "the installer will finish it before pressure testing" is a statement of intent and needs the person who said it.
5. **Progress**: state the activity, the percentage or the milestone reached, and the source of the percentage (the contractor's statement, the visitor's measurement, the site diary). Say which.
6. **Safety**: record what was observed: protective equipment in use or missing, edge protection, housekeeping, scaffolding tags, work at height, hot works permits, welfare. Never soften a safety observation, and never report a safety issue without saying where and when it was seen.
7. **Instructions and agreements**: who said what to whom, whether it was written, and what document followed. An instruction given on site without paperwork is recorded as such, with a note that it needs confirming in writing.
8. **Items to follow up**: one line each, with an owner and a date where known. Route them: correspondence or an RFI to `project-correspondence`, defects to `punch-list`, decisions to `meeting-minutes`.
9. **Afterwards, on a desktop**: number the report from the project register, produce `.docx` if required, attach the documents referred to (drawings, test certificates), and send it to the people named in the report.

## 4. Verify

- Every statement in the report traces to the visitor's words or to a numbered photo. Nothing else enters.
- Photos: each has a number, a place in the text, and its date. A photo without a date or a location is presented as such.
- Measurements: state whether a dimension was measured or estimated. Never present an estimate as a measurement.
- Weather and site conditions are recorded where they affect the work (concrete, earthworks, coatings, scaffolding).
- People are named by role and company, not by opinion. No blame, no adjectives about individuals.
- Safety observations are stated as seen, with time and place.
- Instructions given or received are attributed and flagged as written or verbal.
- The report says what was not seen as well as what was: an area not visited is stated, so nobody assumes it was inspected.
- Anything the visitor could not confirm goes to "to verify", not into the body as a fact.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Markdown by default (readable and sendable from a phone); `.docx` on request, from a desktop.

1. **Identification**: project, report number (if known), date and time, visitor, purpose, weather.
2. **Summary**: three to five lines - what was seen overall, the two or three things that matter.
3. **Present on site**: names, roles, companies.
4. **Progress**: activity, status, source of the percentage.
5. **Observations by area or level**: numbered items, each with its photo numbers.
6. **Safety**.
7. **Quality and defects**: items for `punch-list`.
8. **Materials, deliveries, plant**: what arrived, what was missing, what was idle.
9. **Instructions and agreements**: what was instructed, by whom, written or verbal.
10. **Items to follow up**: one row per item, with owner and date where known.
11. **Photos**: the list with numbers, each one line.
12. **Not visited / not recorded**.
13. **Next visit or next report**.

## Rules

- Record, do not judge. The report states what was there; the decision about consequences belongs to the contract manager, the designer or the authority.
- Safety entries carry the field "imminent danger: yes / no / not recorded". Purpose of the visit not stated means "not recorded", never "routine". Keep internal to-do items out of the client-bound text. The short form ends with one line: the `.docx`, the numbering and the attachments are done on a desktop.
- Imminent danger: when a serious or imminent danger is observed, first tell the user at once to inform the person responsible on site (the site manager), before anything else; the report is not the notification. Record who was told and when once known.
- Never invent an observation, a measurement, a person or a time. "Not recorded" is a valid entry and a useful one.
- Never propose a design change in a site report. Point it out and route it to the designer through `project-correspondence`.
- Do not modify or delete photos. Keep the originals; number copies in the report.
- Personal data: names, roles and companies only, as needed for the record.
- A site report is not a notice, an instruction, an acceptance or a certificate. Where the visit touches one of those, say so and route it to the skill that produces it.
