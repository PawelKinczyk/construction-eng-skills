# Minutes format, action register and decision log

## 1. Head block

```
Minutes of meeting <number>            Date: <YYYY-MM-DD>   Time: <from> - <to>
Project: <project name and number>     Place: <site office / video call>
Chair: <name, company>
Present: <name - company - role> (one line per person)
Apologies: <name - company>
Copies: <who else receives it, and why>
Attachments: <numbered list, with the document number and revision>
Status: draft for approval by the chair. Comments to <name> by <date>.
```

Rules
- Number from the project register. Never invent a number or reuse one.
- One line per attendee, with the organisation. Role only where it matters (designer, contractor, client, inspector).
- The chair is recorded even when the chair is silent in the meeting.
- Copies is not a formality: it shows who was informed, which matters for later disputes.

## 2. Matters arising

List every action from the previous minutes, in order, with one line each:

| # | Action (previous minutes) | Owner | Due | Status | Note |
|---|---|---|---|---|---|
| 1 | | | | closed / carried / not reported | |

Rules
- "Not reported" is an honest status and often the most useful line in the minutes.
- Carried actions keep their original number where the project uses one, and get the new deadline.
- A closed action states the evidence: the document number, the date, the work done.

## 3. Agenda items

Namespace items: `3.1`, `3.2`, or the agenda numbering the project uses. Under each item:

```
3.4 Ventilation, level 1
Report: <one or two factual lines - what was reported, what was shown>
Discussed: <only where the discussion changed something. Otherwise omit>
Decision: <what was decided, by whom>
Action: <see the action register; referenced by its ID>
```

Rules
- Write in the past tense for reports ("the contractor reported that the ductwork...") and in the active present for decisions and actions.
- Do not record who said what in an argument. Record the outcome. Where a party's position must be on record, record the position and the party, factually, once.
- Attribute reports that carry consequences: "the designer reported" is different from "it is the case".
- Numbers quoted in the minutes (quantities, dates, costs) come from the meeting documents, and the document is named.

## 4. Action register

One JSON file per project, updated at every meeting.

```
{
  "project": "Biurowiec Zabłocie B2",
  "entries": [
    {"id": "A-004", "item": "3.4", "action": "Przekazać rzut kanalizacji podposadzkowej",
     "owner": "Zamawiający / J. Kowalski", "due": "2026-10-09", "status": "open",
     "raised": "2026-010", "note": "", "source": "B2-RFI-001", "carried_to": ""}
  ]
}
```

Rules
- Owner is a person with a name, in a company. "The contractor" is not an owner.
- `due` is an absolute date in ISO format.
- Statuses: `open`, `done`, `carried`, `cancelled`.
- `raised` is the meeting in which the action was created; `carried_to` is set when it is moved to a later meeting.
- The ID is assigned by the script and never reused.
- An action closed without evidence ("done" and an empty note) is a warning sign in an audit; require the note.

## 5. Decision log

```
{
  "project": "...",
  "decisions": [
    {"id": "D-007", "date": "2026-10-12", "meeting": "2026-011",
     "decision": "Zmiana trasy pionu W2 na ścianie w osi B",
     "by": "Projektant / A. Nowak", "affects": "design", "reference": "rys. S-201 rew. C"}
  ]
}
```

Rules
- One decision per row, with the person or body that took it.
- `affects` names what the decision changes: design, scope, cost, programme, quality, contract.
- A decision that changes scope, cost or time is not complete until it is instructed or noticed. Point that out in the minutes and route it to `project-correspondence`.
- Decisions recorded in a meeting are minutes-level decisions. A formal instruction or a notice is a separate document, whatever the minutes say.

## 6. Writing rules

- Short sentences. One idea per sentence. One decision per line.
- No adjectives about people, no "unfortunately", no "again". The record outlives the annoyance.
- No passive hiding: "it was agreed" hides who agreed. Write who.
- Numbers as the project writes them (units, decimal separator, currency from the jurisdiction file).
- Do not attach blame. State the fact and the consequence; the dispute machinery is elsewhere.
- Anything the user's raw notes leave unclear goes to a "to confirm with the chair" list, not into the body as an assumption.
- Distribution: send the same text to everyone. No private versions of minutes.

## 7. Meeting types and what they must contain

| Meeting | Must contain |
|---|---|
| Kick-off | the parties and their roles, communication routes, the programme baseline, the document and approval procedures, interfaces |
| Progress meeting | progress against the programme, actions, risks, commercial items, information needed and by when |
| Design and coordination meeting | clashes and interfaces, design decisions, the model or drawing status, responsibility for each interface |
| Site meeting | works done and planned, resources, HSE, quality and defects, materials and deliveries, instructions given, visitors |
| Handover and acceptance | the works accepted, the punch list and its status, the documents handed over, the training given, the warranty start |
| Claim or change meeting | the positions of the parties, what was agreed, what remains disputed and by when the next step is due |
