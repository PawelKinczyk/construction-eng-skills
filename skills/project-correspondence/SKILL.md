---
name: project-correspondence
description: Write and manage project correspondence - letters, RFIs and technical queries, transmittals, contractual notices (including FIDIC and national forms), change and variation requests, non-conformance and coordination issue reports, and meeting follow-up letters. Keeps a numbered correspondence register with response deadlines and overdue items, and warns about contract notice time bars. Use when the user asks to write a letter to the client, engineer, contractor or supplier, prepare an RFI or a notice, register correspondence, chase an overdue answer, or report a coordination issue.
---

# Project correspondence

Goal: every outgoing document is clear, numbered, dated, traceable to its documents, and written so that it protects the sender's position. Nothing goes out that the contract or the record will contradict later.

The skill drafts and registers. The responsible person signs and sends. This is not legal advice: for a notice that may end in a claim, the contract manager or the lawyers check it before it goes out.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, contract form, role (who writes to whom), deliverable language, project standards for document numbering, and the correspondence register location.
- No `PROJECT.md`: offer `project-brief`. If declined, ask for jurisdiction, contract form, role and deliverable language.
- Load `references/shared/jurisdictions/<jurisdiction>.md` for the contract forms, language conventions and the official legal sources.
- Load `references/letter-structure.md` (this skill) for the formats and the tone rules.
- Load `references/contract-notices.md` (this skill) for the notice types, their deadlines and what each must contain.

## 2. Collect inputs

1. **What and why.** The subject in one sentence, the outcome wanted from the reader, and the reason it is being sent now (not earlier or later). If the reason is a deadline, get the contract clause and the date it runs from.
2. **Facts.** Dates, events, documents with revision, quantities, costs, and who said what in which meeting. Every fact must be checkable. Ask for the missing ones; do not fill a fact from memory. Missing facts never mean questions only: still output a draft with visible placeholders such as `[clause - to verify]` or `[DO UZUPELNIENIA]`, followed by the questions.
3. **Contractual basis.** The clause, the contract form, and the notice period that applies. State the clause as it appears in the contract documents supplied.
4. **Reference chain.** Earlier letters, RFIs and minutes this document continues or answers. Get their numbers. A letter that answers an RFI quotes its number.
5. **Register.** Open the project register and take the next number from it. When no register exists, offer `python scripts/corr_log.py init --file register.json --prefix <project prefix>` (ask for the prefix) and then number from it.

## 3. Work

1. **Choose the document type** (letter, RFI, transmittal, notice, change request, non-conformance, coordination issue report) from `references/contract-notices.md`. The type decides the format and the deadline.
2. **Number and register it.** Use the project numbering from `PROJECT.md`. Never reuse a number and never leave gaps unexplained.
   ```
   python scripts/corr_log.py next --file register.json --type RFI
   python scripts/corr_log.py add --file register.json --type RFI --to "Zamawiający" \
       --subject "Brak rzutu kanalizacji podposadzkowej" --days 7 --ref "RFI-004"
   python scripts/corr_log.py list --file register.json --overdue
   python scripts/corr_log.py close --file register.json --id RFI-005 --status answered
   ```
   The script holds dates and deadlines. It does not write the text.
3. **Draft the content** in the format for its type. Keep to facts, requests and consequences:
   - what happened or what is being asked, with dates and document numbers;
   - what is needed and by when, and why that date matters;
   - what happens if nothing is received (reservation of rights, or the effect on the programme, cost or safety) - state it once, factually;
   - what is being reserved, not threatened.
4. **State the reservation of rights** whenever the document reports an event that may lead to time or money: state the event, the notice given under which clause, and that rights are reserved, without quantifying what is not yet known.
5. **Check the deadlines.** For any notice under the contract, verify the period and the trigger from the contract documents, and send well inside the period. Record the sending date and the delivery method in the register.
6. **Follow up.** From the register, list what is unanswered and approaching its deadline, and draft the reminder. Reminders quote the original number and date. For a reminder request, draft one reminder per overdue item from the register immediately (signatory as a placeholder, number, date and consequence taken from the register), and put the follow-up questions after the drafts, never instead of them.

## 4. Verify

- Every fact has a source: a document with revision, a date, a meeting minute, a site record, or a contract clause.
- Clause references come from the contract documents actually supplied. If the clause was not read, write the point without a number and mark it "to verify", or ask.
- Names, roles, addresses and signatories are correct. The right person signs: not the skill, and not someone below the authority level the letter needs.
- The language is the deliverable language of `PROJECT.md`, and the numbering follows the project standard.
- No admissions. A letter never states that the sender caused a delay, a defect or a cost, unless that is the purpose and the responsible person confirmed it.
- No promises about time, money or scope that are not approved.
- Legal or tax statements: only from the official government sources in the jurisdiction file, or not made at all.
- The register is updated: number, date sent, addressee, deadline, linked earlier documents.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default Markdown; on request `.docx` with the project's letter template (letterhead, reference block, signature block).

Sections per type are in `references/letter-structure.md`. Every output ends with:
1. **Document identity**: number, date, subject, addressee, our reference, their reference, attachments list.
2. **Body**: facts, request, date needed, reservation.
3. **Register update**: the row added to the register (number, type, to, deadline).
4. **To verify**: clauses to confirm, facts missing, approvals the letter needs before sending.

State clearly that the document is a draft for the responsible person to check, sign and send. Never claim it has been sent.

## Rules

- Never invent a document number, a clause, a date or a fact. Unknown means ask.
- Never send, sign or file anything on the user's behalf. Drafts only, unless the user explicitly asks for a file to be written to disk.
- Keep the register short and honest. A register that hides overdue items is worse than none.
- One subject per document. Two subjects in one letter get one answer.
- Plain language, no accusations, no adjectives about people. The record may be read by a tribunal years later.
