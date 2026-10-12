# Notices, deadlines and the register

This file lists the notice types to look for and what each must contain. It does NOT give the notice periods: those are in the contract documents supplied for the project, and they differ between forms and editions. Read the contract, write the period and the trigger into the register, and cite the clause as printed.

This is not legal advice. A notice that may carry a claim is checked by the contract manager or the lawyers before it is sent.

## 1. Notices to look for in a contract

| Notice | Usually concerns | What it must contain |
|---|---|---|
| Notice of a claim or of an event | an event that may lead to time or money | the event, the date, the clause, the reservation, that quantification follows |
| Extension of time | delay to completion or to a milestone | the cause, the activities affected, the period, the records |
| Additional or instructed work | a variation, a changed quantity, a changed condition | the instruction or the basis, the scope, the effect, the reservation |
| Payment application and certification | the monthly or milestone payment | the measured value, variations, previously certified amounts |
| Notice of delay to the other party | delay caused by the employer, the engineer or another contractor | what was needed, when, and what it held up |
| Defect or non-conformance notice | non-conforming work or material | location, requirement failed, evidence, required action and date |
| Notice of suspension or of intention to suspend | non-payment or another ground the contract allows | the ground, the clause, the period, the rights reserved |
| Notice of intention to terminate | a contract ground | the ground, the clause, the cure period, the reservation |
| Notice of readiness, testing, taking over | completion, section completion, testing | the date, the test results, the documents, the punch list status |
| Notice of force majeure or exceptional event | events outside the parties' control | the event, the date it started, the effect, what is being done |
| Notice of a change in the contractor's representative or key staff | organisation changes | the person, the role, the CV where the contract requires it |
| Notice of a claim against insurance | an insured event | the event, the date, the policy, the notification channel |
| Notice under the safety rules | a reportable accident, incident or dangerous occurrence | per the national rules and the site safety plan |

## 2. What protects the sender

1. **Form.** Use the form the contract requires. Some contracts require a specific document title, a specific address, or submission through a stated portal. A letter that ignores the form may not count as a notice.
2. **Timing.** Send inside the period, measured from the trigger the contract names (the event, the instruction, the date of knowledge). Record both the trigger date and the sending date.
3. **Content.** State the event, the clause, the effect and the reservation. Do not leave the effect blank; write "not yet quantified" if that is the truth.
4. **Proof of delivery.** Keep the portal receipt, the courier slip, the transmission log, or the email with its header. A notice that cannot be proved to have been received is a weak notice.
5. **Continuity.** Later documents repeat the number and the date of the original notice. Do not start a new chain for the same event.
6. **Records.** Contemporaneous records decide claims: site diaries, progress photos with dates, delivery notes, minutes signed at the meeting, the planned versus actual programme, the labour and plant returns.

## 3. Coordination with the programme and the cost file

- Every notice that mentions time must reference the affected activities, ideally by their identifier in the accepted programme. A delay without an activity is hard to value later.
- Every notice that mentions money must reference the cost basis: the BOQ position, the rate, the quotation, or the daywork record. Keep the cost build-up in one file, updated as information arrives.
- The risk register in `bid-review` and the correspondence register in this skill describe the same events from two sides: price the risk, then chase the answer. Keep the identifiers linked.

## 4. Correspondence register

The register is one file per project, JSON, updated at every outgoing and incoming document. `scripts/corr_log.py` reads and writes it.

```
{
  "project": "Biurowiec Zabłocie B2",
  "currency": "PLN",
  "prefix": "B2",
  "entries": [
    {"id": "B2-RFI-004", "type": "RFI", "date": "2026-10-02", "to": "Zamawiający",
     "subject": "Brak rzutu kanalizacji podposadzkowej", "due": "2026-10-09",
     "ref": "", "status": "open", "note": ""}
  ]
}
```

Rules
- One row per document. The register is not a summary; it is the index to the file.
- Statuses: `open`, `answered`, `closed`, `overdue` (set by the script), `cancelled`.
- The `due` date is the date an answer or an action is needed, with the reason kept in `note`
  ("needed before the pour on level 3").
- Numbers are never reused. A cancelled document keeps its number with the status `cancelled`.
- The register is reviewed in every progress meeting, and the overdue list is circulated.

## 5. Follow-up discipline

| Situation | Action |
|---|---|
| Answer not received by the due date | reminder quoting the original number and date, and stating the consequence of further delay |
| Answer received but incomplete | new document, referencing the answer, listing exactly what is missing |
| Answer refused | record the refusal, escalate to the next level in the contract, state the reservation |
| Verbal answer on site | confirm it in writing the same day: "as agreed at the site meeting on <date>, we understand ... " |
| Instruction received on site without paperwork | confirm in writing with what was instructed, and ask for it to be formalised as an instruction |
| Two documents contradict each other | write asking which prevails, and state which one you are working to in the meantime |

## 6. Quality check before sending

- Type chosen correctly, number taken from the register, no gaps and no reuse.
- Facts cited with document numbers, revisions and dates.
- Clause cited from the contract documents supplied, or the point written without a number and marked to verify.
- The addressee is the right person, with the right copies, at the right address or portal.
- The required date is stated, with the reason, and it is achievable.
- Reservation of rights present where the event may lead to time or money.
- Nothing admits liability or promises time, money or scope.
- Attachments complete, numbered and referenced in the body.
- Register updated: number, date, addressee, due date, links.
- Signature by the person with the authority for this document type.
