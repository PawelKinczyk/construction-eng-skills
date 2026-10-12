---
name: meeting-minutes
description: Write construction meeting minutes and run the decision and action registers - progress, design and coordination meetings, site meetings, kick-off and handover meetings. Turns notes, dictation, a transcription or a rough list into minutes with decisions, actions with an owner and an absolute deadline, matters arising from the previous meeting, plus a decision log and a follow-up list of overdue actions. Use when the user asks to write up a meeting, prepare minutes or a protokół, chase actions from the last meeting, list decisions taken, or keep a decision log.
---

# Meeting minutes

Goal: minutes that record what was decided and who does what by when, in a form that can be read in the meeting and checked later. Discussion is not recorded; decisions and actions are.

Two registers come out of this skill: an action register (owner, deadline, status) and a decision log (decision, who took it, when, what it changes). Both live as files next to the minutes and are carried forward from meeting to meeting.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, contract form, role, deliverable language, and whether the project uses a numbered minute series and an approval process.
- No `PROJECT.md`: offer `project-brief`. If declined, ask for the deliverable language, the project name and who approves the minutes.
- Load `references/shared/jurisdictions/<jurisdiction>.md` for document conventions if the minutes must follow a legal or contractual form (for example a kick-off or handover record).
- Load `references/minutes-format.md` (this skill) for the structure, the registers and the writing rules.
- Load the project's correspondence register (`project-correspondence`) if it exists, and take the minute number from it instead of inventing a series.

## 2. Collect inputs

1. **Raw material.** Notes, dictation, a transcript, an agenda with annotations, or the user's summary. Ask for the meeting date, place, number, chair and attendees with their organisations.
2. **The previous minutes and the action register.** Matters arising and carried actions cannot be written without them. Ask for the file, or say that the follow-up section is incomplete.
3. **The agenda**, and the items actually discussed. Minutes follow the agenda order.
4. **Decisions and actions.** If the raw material mixes discussion and decisions, ask which statements are decisions. Do not decide for the meeting.
5. **Language and distribution.** The deliverable language, who receives the minutes, who approves them (usually the chair), and the deadline for comments on them.

## 3. Work

1. **Register the meeting.** Number, date, place, chair, attendees, apologies, copies. Take the number from the project register, not from the sequence in your head.
2. **Follow the agenda item by item.** Under each item, record: what was reported (one or two lines, factual), and the decisions taken. Leave out opinion, blame and long discussion.
3. **Write the decisions** as statements in the active voice: what was decided, who decided it, and the effect (scope, cost, time, design). A decision without an actor is not a decision.
4. **Write the actions** one per row: action, owner (a named person, not a company), absolute deadline (date, not "next week"), and the item it belongs to.
   ```
   python scripts/actions.py add --file actions.json --item "3.1" --action "Przekazać rzut kanalizacji podposadzkowej" \
       --owner "Zamawiający / J. Kowalski" --due 2026-10-09 --source "B2-RFI-001"
   python scripts/actions.py list --file actions.json --open
   python scripts/actions.py list --file actions.json --overdue
   python scripts/actions.py close --file actions.json --id A-004 --status done --note "rzut przekazany 09.10.2026"
   python scripts/actions.py carry --file actions.json --to-minutes 2026-011
   ```
5. **Matters arising**: for every open action from the previous meeting, state the status and either close it or carry it with the new deadline. An action that silently disappears is the most common failure in project records.
6. **Decision log**: append the decisions with their date and meeting number. This log is what gets quoted months later when someone asks "when was that decided".
7. **Risks and issues raised**: record what was raised, by whom, and what is to be done about it. Do not soften a risk that a party flagged; record it.
8. **Next meeting**: date, place, and the items deferred to it.

## 4. Verify

- Every action has an owner, a deadline with a full date, and a source (the meeting item, or the document it comes from).
- Every decision names who took it. Decisions by the chair, by the client and by the designer are different things and are recorded as such.
- No invented details: no attendee, no date, no decision that is not in the raw material. Anything unclear is marked "to confirm with the chair" rather than guessed.
- Quantities, dates and document numbers match the source documents and the correspondence register.
- Actions from the previous meeting are all accounted for: closed, carried, or listed as not reported.
- The minutes state that they are a draft until the chair approves them, and carry the comment deadline.
- Contractual consequences of a decision (a variation, a notice, a change in the scope) are pointed out, and routed to `project-correspondence` as a notice or a change request. Minutes alone do not constitute a notice.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default Markdown; on request `.docx` in the project template.

Structure (details in `references/minutes-format.md`):

1. Head: number, date, place, chair, attendees, apologies, copies, approval line.
2. Matters arising: previous actions with their status.
3. Agenda items: report, decisions, actions per item.
4. Decisions taken in this meeting.
5. Action register extract: the actions of this meeting, plus the open ones.
6. Risks and issues raised.
7. Next meeting.
8. Attachments, and the comment deadline.

Also output, as separate files when the user wants them: the updated action register (`actions.json`) and the decision log.

## Rules

- Minutes record; they do not decide, justify or argue. No adjectives about people or companies.
- Never invent an attendee, a decision, a deadline or a number.
- An action is assigned to one owner. Shared ownership means no owner.
- Deadlines are absolute dates. "ASAP" and "next week" are not deadlines.
- The chair approves the minutes. Say they are a draft until that happens.
- Keep the registers in files, not only in the minutes: they are what the next meeting runs on.
- Personal data: minutes list attendees and their organisations. Do not add personal details beyond the role the person holds on the project.
