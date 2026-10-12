# Punch list fields, workflow and handover rules

## 1. Fields

| Field | Meaning | Rules |
|---|---|---|
| id | item number | from the register, never reused |
| location | level, zone, room, grid | as the project names them (from `project-standards`); a room number, not "near the lift" |
| element | what the defect is on | the element as built: wall, ceiling, pipe, valve, panel, door |
| trade | discipline or works package | one trade per item, so it can be allocated and counted |
| description | the fact observed | measurable, no adjectives; a tolerance only with its source and clause |
| severity | A / B / C / D (see below) | drives the deadline |
| photo | photo reference(s) | item without a photo is flagged, not hidden |
| owner | the party responsible | under the contract, as a company with the contact person |
| due | deadline | absolute date |
| status | open, in progress, fixed, verified, closed, rejected | see the workflow |
| raised | walkthrough date and its reference | site report number, inspection, or the person who reported it |
| verified_by, verified_on | who checked the fix, when | the verifier is not the party who fixed it |
| note | evidence and history | closure requires a note naming the evidence |

## 2. Severity classes (default)

Use the project's own convention when it has one, and say which one is in use.

| Class | Meaning | Typical deadline |
|---|---|---|
| A | safety-critical, structural, or blocks another trade from proceeding | reported immediately, fixed before the next working shift, or as agreed in writing |
| B | functional: the works will not perform or will not be accepted as designed | before the next inspection or within one to two weeks |
| C | cosmetic or minor: finish, paint, alignment, cleaning | before handover |
| D | observation, no action agreed | recorded, not chased |

Deadlines in this table are a default for projects without their own convention. The contract, the handover date or the client's instruction sets the real ones.

## 3. Workflow

```
open            raised, not started
in progress     the responsible party started (say since when)
fixed           the party claims it is done - needs evidence: photo, test, measurement
verified        someone other than the doer checked it against the requirement
closed          verified and accepted; the note names the evidence
rejected        not accepted as a defect by the responsible party, or rejected by the
                inspector after a claimed fix; the note says who rejected it and why
```

Rules
- "Fixed" is a claim. "Verified" is a check. Never collapse the two: closing on a claim is how defects reappear after handover.
- A rejected item stays in the register. Deleting it loses the record of the dispute.
- Re-opening a closed item is allowed and common (the defect returns); the note says when and why.
- Items are never deleted. Superseded items are marked rejected or merged, with a reference to the item that replaces them.

## 4. What is a punch item and what is not

| Is a punch item | Is not a punch item |
|---|---|
| a defect against the specification, drawing or manufacturer's instructions | a change to the design asked for after construction |
| damage caused by another trade | additional works the client now wants |
| incomplete work within the contract scope | work outside the contract scope |
| a tolerance failure, with the tolerance named | a preference ("we would have used a different brand") |
| missing labels, guards, covers, seals | a maintenance task for the future |
| a test failure | a design question ("the valve cannot be reached") -> designer, in writing |

Rules
- A design question goes to the designer with a written record (`project-correspondence`), not into the defect list.
- Additional works go through the change mechanism (`project-correspondence`), not the punch list.
- Where the classification is unclear, raise it as an item with severity D and the note "to classify", rather than dropping it.

## 5. Photo evidence

| Situation | What is needed |
|---|---|
| Any defect | one wide view placing the item, one close-up showing it |
| A dimension defect | a scale in the frame (tape, known object), or a measured value in the description |
| A water or air leak | the wet area and the source, plus the test record if one exists |
| After the fix | the same view as before the fix, so the two can be compared |
| A serial defect (same defect in many rooms) | one item per room with its own photo, or one item with the room list and a photo per room attached - state which convention the list uses |

Rules
- Never edit an original photo. Crop or annotate copies for reports only.
- A photo from another date or another source is labelled as such; it is not evidence of this walkthrough.
- Where a photo is missing, the item says so. An unphotographed defect is the first one disputed at handover.

## 6. Handover view

Prepare this view for the walkthrough with the client:

1. Group by room, then by trade within the room. The client walks room by room.
2. Show every item with its status, and mark the open ones.
3. List separately: items with severity A or B still open, items without photos, items whose owner is disputed.
4. State the walkthrough date, the areas covered, and the areas not inspected.
5. State what the acceptance does and does not mean: accepting the handover with open items means they are listed with a plan and dates; it does not mean the works are complete.

Rules
- Never present a list as complete when the areas were not all inspected. Say which were not.
- Do not close items to make the handover view cleaner. The client's inspector will find them anyway, and the credibility loss is worse than the open item.
- Keep the same numbering in the handover view, the working list and the photos.

## 7. Reporting and counting

- Counts by status, severity and trade; the overdue count by owner.
- The same item counted twice (by trade and by severity) is normal; totals must say what they count.
- The register holds history: every status change has a date and a note. That history is what answers "when was this fixed and who checked it" months later.
- The register stays live through the defects liability period; the end point is closing the last item, not the handover date.
