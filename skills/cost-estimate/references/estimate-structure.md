# Estimate structure, markups and rounding

Assumption behind this file: prices and percentages come from the project, the contract or the jurisdiction price source. This file gives the structure and the arithmetic order. It never gives a rate, and its example percentages are illustrative only.

## 1. Two common structures

### Polish detailed estimate (kosztorys szczegółowy)

| Component | Meaning | Basis |
|---|---|---|
| R | labour (robocizna) | from the catalogue norm (nakład) times the labour rate |
| M | materials (materiały) | from the norm times the material price |
| S | equipment (sprzęt) | from the norm times the equipment rate |
| Kp | overheads (koszty pośrednie) | percentage of R + S |
| Z | profit (zysk) | percentage of R + S + Kp |
| Kz | purchase costs (koszty zakupu materiałów) | percentage of M |
| Net | direct costs + Kp + Z + Kz | |
| VAT | value added tax | percentage of net; the rate depends on the works and the jurisdiction |

Rules:
- Kp, Z and Kz are contractual. They are set in the contract, the tender documents or the client's method statement. The estimator reads them, never assumes them.
- Apply each markup once, in this order. Do not apply a markup on another markup unless the method says so (Z is the exception: its basis includes Kp).
- A simplified estimate (kosztorys uproszczony) uses a single unit rate per position with no breakdown. Then Kp, Z and Kz are already inside the rate; do not add them again.

### BOQ with contractor pricing (UK, US, international)

| Level | Content |
|---|---|
| Measured works | grouped by element or trade, one unit rate per item, priced by the contractor |
| Preliminaries | site management, temporary works, insurances, cleaning, as a lump sum or a percentage |
| Overheads and profit | usually inside the unit rates; if shown separately, state the percentage |
| Contingency | risk allowance, as a percentage of the works or a stated lump sum |
| Escalation, inflation | only when the price level and the construction period differ |
| Tax | VAT or sales tax per the jurisdiction |
| Rounding and adjustments | stated by the client |

Rules:
- Preliminaries are frequently the biggest source of error in a comparison. Never compare two offers on the measured works only.
- Provisional sums and dayworks are not estimated rates. Carry them as given, and say so.

## 2. Markup cascade

```
direct  = sum(lines)
R, M, S = split of direct (when the structure asks for it)
Kp      = kp%  * (R + S)
Z       = z%   * (R + S + Kp)
Kz      = kz%  * M
net     = direct + Kp + Z + Kz
tax     = vat% * net
gross   = net + tax
```

`scripts/estimate_calc.py rollup` runs exactly this cascade. Without a kind given per line, all lines count as direct costs and the script skips Kp, Z and Kz; it then applies only the markups whose bases exist.

## 3. Uncertainty, contingency and escalation

| Item | How to handle |
|---|---|
| Estimate class | State it: a takeoff from detailed drawings is not the same as a rate per m2 of floor area. Say what the estimate is based on |
| Accuracy range | `range --value --percent`. Typical working ranges: conceptual ±30 %, early design ±20 %, detailed takeoff with priced rates ±10 %, priced contract BOQ ±5 %. These are conventions for communication, not a guarantee. Say which one you used |
| Contingency | A percentage or a lump sum, stated separately from the markups, decided by the client. Not a substitute for a missing quantity |
| Escalation | `escalation --value --percent --periods` for compound indexation between the price level and the construction period. Only when the contract has an indexation clause or the price level differs from the performance period. Cite the index and its source |
| Currency | One currency per estimate. For a second currency, state the rate, its source and the date. Never mix currencies in one column |

## 4. Rounding and units

- Keep the full precision inside the calculation. Round at the end, not per line.
- Round the line value to the currency's minor unit (0.01 PLN, 0.01 EUR, 0.01 GBP, 0.01 USD).
- Round quantities to the precision of their unit: m3 to 0.01, m2 to 0.01, m to 0.01, t to 0.001, pieces to 1.
- State whether the total is net or gross. In Poland: "netto" and "brutto" stated explicitly, decimal comma, space as the thousands separator (12 500,00 zł). Dates DD.MM.YYYY.
- Do not show a total with more precision than its inputs justify. A rate rounded to 0.01 charged against a rounded quantity gives a value that is exact enough at 0.01, but the percentage markups must run on unrounded values.

## 5. Price comparison between offers

1. Normalise the scope first. Build the comparison on the client's BOQ positions, not on the offers' own tables.
2. Compare line by line, not only the total, and flag lines where the deviation is large in both directions.
3. Check that each offer covers the same things: preliminaries, temporary works, testing and commissioning, as-built documents, training, warranty, spare parts.
4. State the price level and the validity date of each offer.
5. Report deviations as "missing in offer", "extra in offer", "quantity differs" and "rate differs", per line.
