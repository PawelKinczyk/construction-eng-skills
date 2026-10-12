---
name: bid-review
description: Review tender and client documents before bidding or during a tender - instructions to tenderers, scope of works, technical specifications, contract conditions (FIDIC, NEC, national forms), programme, price and payment terms, quality and HSE requirements. Produces a risk register, clarification questions (RFI) for the client, a deviations and qualifications list, assumptions and exclusions, and the structure of the offer. Use when the user asks to review a tender, check an inquiry or RFP, prepare questions to the client, decide whether to bid, price the risks of a contract, or prepare an offer or bid submission.
---

# Bid review

Goal: before the offer goes out, the team knows the scope, the risks, the questions the client must answer, and what the offer says about all three. Output: a review report, an RFI list, a deviations register and the offer structure with its price build-up.

This skill does not price the works line by line; that is `cost-estimate`. It does not write the offer letter; that is `project-correspondence`. It decides what the offer must contain, and what must be asked before the price is fixed.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, contract form in use, role (bidder or client), deliverable language, risk appetite or approval rules.
- No `PROJECT.md`: offer `project-brief`. If declined, ask for jurisdiction, contract form, role and deliverable language.
- Load `references/shared/jurisdictions/<jurisdiction>.md` for procurement law, contract forms and price sources. Public procurement rules differ from private ones; get the regime right first.
- Load `references/tender-review-checklist.md` (this skill) for the document set and the review questions.
- Load `references/rfi-and-offer.md` (this skill) for the RFI format, the deviations register and the offer structure.

## 2. Collect inputs

Ask for the document set in one message, and mark what was not received. Without these, the review has holes and must say so:

1. **Invitation and instructions**: ITT or SWZ, evaluation criteria, deadlines, submission format, question deadlines, validity period of the offer.
2. **Scope**: technical description, BOQ or price form, drawings and schedules with revisions, specification (STWiOR or equivalent), scope split with other contracts.
3. **Contract conditions**: the form (FIDIC book and edition, NEC option, or national/ bespoke), particular conditions, amendments to the general conditions, guarantees, liquidated damages, caps and liability limits, suspension, termination, force majeure, dispute resolution.
4. **Commercial terms**: payment terms, advance and retention, payment periods and certification, price adjustment and indexation, currency, securities (performance bond, retention bond, parent company guarantee), insurances required.
5. **Programme and site**: required or expected programme, milestones, working hours, access and possession, site conditions and surveys, permits and utilities, restrictions (noise, traffic, occupied building).
6. **Quality, HSE and handover**: quality plan, inspection and testing, documentation and as-builts, training, warranty period and defects liability, O&M manuals, spare parts, BIM and information requirements.
7. **Evaluation**: how the price and the non-price criteria are scored, and any cap or formula.

Read every document and record the revision. Work from the documents, not from the client's summary.

## 3. Work

1. **Scope check.** Build the scope list from the documents. Mark: works that must be priced, works that look missing, works that may be someone else's (interface), and works whose quantity or definition is unclear. Compare the BOQ with the drawings and the specification; no BOQ is complete.
2. **Contract review.** Go through the conditions clause by clause against the checklist. Record deviations from the standard form, and each one's commercial effect: who owns the risk, what it could cost, how it is triggered. Use `references/tender-review-checklist.md`, section "Contract conditions".
3. **Risk register.** For each risk: description, category, trigger, consequence, who bears it under the contract, and the treatment (price it, qualify it, ask, insure it, accept it). Rank by exposure, not by likelihood alone.
4. **Price the risks.** Risk allowance from the register, after any qualifications:
   ```
   python scripts/bid_calc.py risk --file risks.json --json
   python scripts/bid_calc.py price --cost 4200000 --risk-allowance 180000 --overhead-percent 6 --margin-percent 8
   python scripts/bid_calc.py cashflow --contract-value 5000000 --advance-percent 10 --retention-percent 5 --payment-days 45 --interest-percent 8.5
   ```
   Never put an unquantified worry into the price as a round number. Either quantify it with stated inputs, or carry it as a qualification in the offer.
5. **Questions (RFI).** Every unclear point becomes a question, in the client's language. One point per question, with the document and clause it comes from, and the effect if unanswered. Send them before the deadline the instructions set.
6. **Deviations and qualifications.** For each point the offer will not accept as written: what the documents say, what the offer proposes, and the commercial effect. This is the part that protects the offer later.
7. **Bid or no-bid.** Summarise: scope fit, risk exposure, competition, capability and capacity, the contract terms that could not be changed, and the deadline feasibility. Recommend, and leave the decision to the user.

## 4. Verify

- Every risk traces to a document and a clause, or to a site or programme fact. No risks from general feeling.
- Every question traces to a document, clause or drawing revision. Questions already answered in a corrigendum are not repeated; check the amendments list first.
- Every deviation has the original text referenced and the proposed alternative.
- Contract-form statements are checked against the actual document supplied, not from memory of the standard form. If only the reference is given and not the text, the point goes to "to verify".
- Procurement law points come only from the official government sources in the jurisdiction file, with the act and article. This is not legal advice; contested points go to the lawyers.
- Price build-up: every element is traceable to `cost-estimate`, the risk register, or a stated percentage with its source.
- The evaluation criteria and the submission checklist are re-read before submission; a missing document is a rejected bid.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default format Markdown, on request `.docx`.

1. **Summary**: project, contract form, scope in one paragraph, bid or no-bid recommendation, the three biggest risks, the number of open questions.
2. **Scope review**: priced scope, gaps, interfaces, unclear items.
3. **Risk register**: table with ID, risk, category, contract allocation, effect, treatment, allowance.
   | # | Risk | Category | Who bears it | Effect | Treatment | Allowance |
4. **Contract review**: deviations from the standard form, each with clause reference and commercial effect.
5. **RFI list**: one row per question, ready to paste into the client's template.
   | # | Question | Document / clause | Why it matters | Answer |
6. **Deviations and qualifications**: what is proposed for the offer.
7. **Price build-up**: cost, risk allowance, overhead, margin, price; cashflow and financing cost.
8. **Offer structure**: sections the offer must have, in the order the instructions require.
9. **To verify**: documents not received, points needing the client, legal or tax questions, and the approval the price needs.

## Rules

- Do not invent clause numbers, prices, client requirements or competition data.
- Do not sign, submit or send anything. The offer is issued by the responsible person in the company.
- Do not conceal a risk to make a bid look better. A bid won with an unpriced risk is a loss.
- A question the client refuses to answer is itself a risk; record it as such.
- Keep the review reproducible: every statement points to a document, a revision and a clause or page.
