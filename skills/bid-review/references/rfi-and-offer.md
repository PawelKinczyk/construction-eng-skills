# RFI list, deviations register and offer structure

## 1. Clarification questions (RFI)

Rules
- One question per item. Two questions in one line get one answer, usually to the easier half.
- Quote the document, the clause and the page, and the drawing with its revision. Quote the wording being questioned, briefly.
- Say what the answer changes: price, programme, risk, or the design responsibility.
- Do not ask what a corrigendum already answers. Read the amendments list first, every time.
- Do not phrase a question as a proposal. Offer the alternatives in the deviations register, not in the question.
- Ask every question before the client's deadline. Group them in one submission, numbered, in the client's language.
- Record the answers, the date, and the document that carries them. An answer by phone is not an answer until it is written.

Format

| # | Question | Document / clause | What changes with the answer | Asked on | Answer | Answered on |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

Examples of question shapes (adapt, do not reuse the text)
- "Pos. 2.14 przedmiaru podaje 480 m² tynków, rysunek A-11 rew. B pokazuje ok. 640 m². Która ilość jest wiążąca i czy obmiar będzie weryfikowany przez zamawiającego?"
- "Nothing in the documents says who supplies the temporary power connection. Please confirm whether it is in our scope, and at which point of the site."
- "Clause 14.2 (particular conditions) amends the payment period to 90 days. Please confirm this is intentional."

## 2. Deviations and qualifications register

Purpose: state clearly what the offer does not accept as written. Written once, in the offer, it protects the bidder later; left out, it becomes an argument after award.

| # | Document / clause | As written | Proposed by us | Effect on price, time or risk | Accepted by client |
|---|---|---|---|---|---|
| 1 | | | | | |

Rules
- Propose alternative wording, not a complaint. Give the practical reason: a method, a manufacturer's requirement, a safety requirement, or a risk that cannot be carried at that price.
- Quantify the effect when it can be quantified, and say "not quantified" when it cannot. Never leave the effect blank.
- Keep the register short. A long list of qualifications reads as an unserious bid; group related points.
- A qualification that changes the technical solution must be checked against the specification and, where relevant, the permit conditions.
- Anything the client will not accept becomes either a priced risk or a reason not to bid. Decide it before submission, not after.

## 3. Offer structure

Follow the order the instructions require. If they do not require one, use this order. Write the offer in the client's language.

1. Cover letter: reference, project, price, validity, the person signing. Length: one page.
2. Table of contents and the checklist of submitted documents.
3. Technical part: scope confirmation, method statements, programme, resources, organisation chart, quality plan, HSE plan, reference projects and CVs required by the criteria.
4. Commercial part: priced BOQ or price form in the client's structure, price summary, cashflow
   schedule, securities offered, insurances.
5. Contract part: signed form of tender, the deviations and qualifications register, any required
   declarations.
6. Annexes: certificates, guarantees, data sheets, drawings, calculations.

Submission checklist (verify each one against the instructions)
- [ ] Every required document present, in the required format (signed, electronic, sealed).
- [ ] Price form filled in the client's units and currency; no lines left blank.
- [ ] Deviations register attached and referenced in the tender form.
- [ ] Signatures, powers of attorney and authorisations valid.
- [ ] Deadlines: questions, submission time, validity period.
- [ ] Submission channel and format as instructed (portal, envelope, number of copies).

## 4. Price build-up

```
base cost            from cost-estimate for the scope actually priced
+ risk allowance     from the risk register, per risk
+ overhead           stated percentage, with its basis
+ margin             stated percentage, on cost or on price (say which)
= offer price (net)
+ tax                per the jurisdiction and the contract
= offer price (gross)
```

Rules
- Say whether the margin is applied on cost or on price. The difference is a real percentage point and is a common source of confusion.
- The risk allowance is not a contingency for the unknown scope; unknown scope goes into the questions or the qualifications.
- Financing cost from the payment terms is a cost, not a risk allowance. Use `scripts/bid_calc.py cashflow`.
- Keep the build-up in one table so the approving manager can see it in a minute.
- The final price is decided by the responsible person in the company, per the company's approval limits.

## 5. FIDIC and NEC points to check

When the contract names a standard form, check the actual printed conditions plus the particular conditions, and record every amendment. Common points where the particular conditions change the risk balance:
- Payment terms, certification and the employer's payment obligations.
- Extension of time grounds, and whether the list is closed.
- Testing, taking over and the defects notification period.
- The role and neutrality of the engineer (FIDIC) or the project manager and the accepted programme (NEC).
- The FIDIC Silver Book shifts design and unforeseeable conditions risk to the contractor; check which book is used before assuming the Red Book balance.
- NEC compensation events and the early warning register have their own machinery; do not read them as FIDIC clauses.
Never quote a clause from memory. Cite the book, the edition and the clause from the document supplied.
