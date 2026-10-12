#!/usr/bin/env python3
"""Bid review calculations. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

The script does no guessing: probabilities, impacts, percentages and payment terms come from
the user, the risk register or the contract documents.

Commands:
  risk      expected value of the risks in a register
            --file risks.json [--json]
  price     price build-up from cost, risk allowance, overhead and margin
            --cost 4200000 [--risk-allowance 180000] [--overhead-percent 6]
            [--margin-percent 8] [--margin-on cost|price] [--tax-percent 23]
  cashflow  financing cost from the payment terms
            --contract-value 5000000 [--cost-ratio 1.0] [--duration-months 12]
            [--advance-percent 10] [--retention-percent 5] [--payment-days 45]
            [--retention-release-months 12] [--interest-percent 8.5]

risk file (JSON):
{
  "currency": "PLN",
  "risks": [
    {"id": "R1", "name": "Ground conditions", "category": "site",
     "probability": 0.3, "impact": 500000, "contract": "client",
     "treatment": "price", "source": "ITT clause 4.2"}
  ]
}
Risks without a probability or an impact are listed as unquantified and are NOT included in
the expected value. They must be priced after quantification or carried as a qualification.

cashflow model and its assumptions (state them in the report):
  - work and cost are spread evenly over the duration
  - value is certified at each month end and paid after the payment delay
  - the advance is received at the start and recovered pro rata from the payments
  - retention is withheld from each payment and released after the release period
  - financing cost = sum of monthly deficits * monthly interest rate
"""

import argparse
import json
import math
import sys


def num(x, n=2):
    return f"{x:,.{n}f}".replace(",", " ")


def out(args, title, inputs, formula, results, notes=()):
    if args.json:
        print(json.dumps({"calculation": title, "inputs": inputs, "formula": formula,
                          "results": results, "notes": list(notes)}, ensure_ascii=False, indent=2))
        return
    print(f"== {title} ==")
    print("Inputs:")
    for k, v in inputs.items():
        print(f"  {k}: {v}")
    print(f"Formula: {formula}")
    print("Results:")
    for k, v in results.items():
        print(f"  {k}: {v}")
    for n in notes:
        print(f"Note: {n}")


def positive(x):
    v = float(x)
    if v <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return v


def cmd_risk(args):
    with open(args.file, encoding="utf-8") as fh:
        data = json.load(fh)
    risks = data.get("risks", [])
    if not risks:
        raise ValueError("the file has no 'risks' list")
    currency = data.get("currency", "")
    rows, unquantified, total = [], [], 0.0
    for risk in risks:
        p, impact = risk.get("probability"), risk.get("impact")
        if p is None or impact is None:
            unquantified.append(risk)
            continue
        ev = float(p) * float(impact)
        total += ev
        rows.append({"id": risk.get("id", ""), "name": risk.get("name", ""),
                     "category": risk.get("category", ""), "probability": float(p),
                     "impact": float(impact), "expected_value": ev,
                     "contract": risk.get("contract", ""), "treatment": risk.get("treatment", ""),
                     "source": risk.get("source", "")})
    rows.sort(key=lambda item: item["expected_value"], reverse=True)
    notes = []
    if unquantified:
        notes.append(f"{len(unquantified)} risk(s) have no probability or no impact and are "
                     "NOT in the expected value: quantify them or carry them as a qualification")
    no_source = [row for row in rows if not row["source"]]
    if no_source:
        notes.append(f"{len(no_source)} quantified risk(s) have no document reference; every "
                     "risk must trace to a document and a clause")
    if args.json:
        print(json.dumps({"currency": currency, "risks": rows, "expected_value": total,
                          "unquantified": [r.get("name", "") for r in unquantified],
                          "notes": notes}, ensure_ascii=False, indent=2))
        return
    print(f"== Risk expected value ==   currency: {currency or 'not stated'}")
    print(f"{'ID':<6} {'Risk':<38} {'P':>6} {'Impact':>14} {'Expected':>14}  Treatment")
    for row in rows:
        print(f"{row['id']:<6} {row['name'][:37]:<38} {row['probability']:>6.2f} "
              f"{num(row['impact']):>14} {num(row['expected_value']):>14}  {row['treatment']}")
    print(f"\nRisk allowance (sum of expected values): {num(total)} {currency}")
    if unquantified:
        print("\nUnquantified risks (not in the sum):")
        for risk in unquantified:
            print(f"  - {risk.get('id','')} {risk.get('name','')} "
                  f"({risk.get('source','no source')})")
    for n in notes:
        print(f"Note: {n}")


def cmd_price(args):
    overhead = args.cost * args.overhead_percent / 100
    subtotal = args.cost + args.risk_allowance + overhead
    if args.margin_on == "price":
        margin = subtotal * args.margin_percent / (100 - args.margin_percent)
    else:
        margin = subtotal * args.margin_percent / 100
    price_net = subtotal + margin
    tax = price_net * args.tax_percent / 100
    price_gross = price_net + tax
    margin_on_price = margin / price_net * 100 if price_net else 0.0
    results = {
        "base cost": num(args.cost),
        "risk allowance": num(args.risk_allowance),
        f"overhead {args.overhead_percent}%": num(overhead),
        "subtotal": num(subtotal),
        f"margin {args.margin_percent}% on {args.margin_on}": num(margin),
        "price net": num(price_net),
        "margin as percent of price": f"{margin_on_price:.2f} %",
    }
    if args.tax_percent:
        results[f"tax {args.tax_percent}%"] = num(tax)
        results["price gross"] = num(price_gross)
    notes = ["Say in the report whether the margin is on cost or on price: the same percentage "
             "gives different prices.",
             "The risk allowance is not a contingency for unknown scope. Unknown scope goes to "
             "the questions or the qualifications."]
    if not args.risk_allowance:
        notes.append("no risk allowance given: either there are no quantified risks, or they "
                     "were not priced. State which")
    out(args, "Price build-up",
        {"base cost": num(args.cost), "risk allowance": num(args.risk_allowance),
         "overhead": f"{args.overhead_percent} %", "margin": f"{args.margin_percent} %",
         "margin basis": args.margin_on, "tax": f"{args.tax_percent} %"},
        "overhead = ovh% * cost; subtotal = cost + risk + overhead; "
        "margin = m% * subtotal (or subtotal * m/(100-m) on price); price = subtotal + margin",
        results, notes)


def cmd_cashflow(args):
    months = max(1, int(round(args.duration_months)))
    delay = max(0, int(math.ceil(args.payment_days / 30.0)))
    value = args.contract_value
    cost_total = value * args.cost_ratio
    monthly_value = value / months
    monthly_cost = cost_total / months
    advance = value * args.advance_percent / 100
    retention_rate = args.retention_percent / 100
    total_retention = value * retention_rate
    i_month = args.interest_percent / 100 / 12

    release_month = months + delay + int(math.ceil(args.retention_release_months))
    horizon = release_month
    payments = {0: advance}
    for m in range(1, months + 1):
        payments[m + delay] = payments.get(m + delay, 0.0) + monthly_value * (
            1 - retention_rate - args.advance_percent / 100)
    payments[release_month] = payments.get(release_month, 0.0) + total_retention

    rows = []
    cash_received = 0.0
    cash_spent = 0.0
    interest_total = 0.0
    peak_deficit = 0.0
    for m in range(0, horizon + 1):
        spent = monthly_cost if 1 <= m <= months else 0.0
        paid = payments.get(m, 0.0)
        cash_spent += spent
        cash_received += paid
        balance = cash_received - cash_spent
        deficit = max(0.0, -balance)
        interest = deficit * i_month
        interest_total += interest
        peak_deficit = max(peak_deficit, deficit)
        rows.append((m, spent, paid, balance, deficit, interest))

    results = {"contract value": num(value),
               "payment delay used": f"{delay} month(s) from {args.payment_days} days",
               "retention withheld": num(total_retention),
               "peak funding need": num(peak_deficit),
               "financing cost": num(interest_total),
               "financing cost percent of value": f"{interest_total / value * 100:.2f} %"}
    notes = ["Assumptions: even spread of cost and value, certification at each month end, "
             "advance recovered pro rata from the payments, retention released after the "
             "release period. State them in the report, and adjust them to the actual programme "
             "and payment terms.",
             "The financing cost is a cost, not a risk allowance. Carry it in the price build-up.",
             "A negative balance means the project is funded by the company; check the working "
             "capital limit and the cost of that money, not only the interest rate."]
    if args.json:
        print(json.dumps({"inputs": {"contract_value": value, "cost_ratio": args.cost_ratio,
                                     "duration_months": months, "advance_percent": args.advance_percent,
                                     "retention_percent": args.retention_percent,
                                     "payment_days": args.payment_days,
                                     "retention_release_months": args.retention_release_months,
                                     "interest_percent": args.interest_percent},
                          "results": results,
                          "months": [{"month": m, "cost": s, "received": p, "balance": b,
                                      "deficit": d, "interest": i}
                                     for m, s, p, b, d, i in rows],
                          "notes": notes}, ensure_ascii=False, indent=2))
        return
    out(args, "Bid cashflow and financing cost",
        {"contract value": num(value), "cost as fraction of value": args.cost_ratio,
         "duration": f"{months} month(s)", "advance": f"{args.advance_percent} %",
         "retention": f"{args.retention_percent} %",
         "payment delay": f"{args.payment_days} days ({delay} month)",
         "retention release": f"{args.retention_release_months} month(s) after the last payment",
         "interest rate": f"{args.interest_percent} % per year"},
        "monthly balance = cumulative received - cumulative cost; "
        "financing cost = sum of monthly deficits * i/12",
        results, notes)
    print("\nMonthly balances (month, cost, received, balance):")
    for m, spent, paid, balance, _d, _i in rows:
        print(f"  {m:>3}: cost {num(spent):>14}  received {num(paid):>14}  "
              f"balance {num(balance):>16}")


def build_parser():
    p = argparse.ArgumentParser(description="Bid review calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    s = add("risk", cmd_risk)
    s.add_argument("--file", required=True)

    s = add("price", cmd_price)
    s.add_argument("--cost", type=positive, required=True)
    s.add_argument("--risk-allowance", type=float, default=0.0)
    s.add_argument("--overhead-percent", type=float, default=0.0)
    s.add_argument("--margin-percent", type=float, default=0.0)
    s.add_argument("--margin-on", choices=["cost", "price"], default="cost")
    s.add_argument("--tax-percent", type=float, default=0.0)

    s = add("cashflow", cmd_cashflow)
    s.add_argument("--contract-value", type=positive, required=True)
    s.add_argument("--cost-ratio", type=positive, default=1.0)
    s.add_argument("--duration-months", type=positive, default=12.0)
    s.add_argument("--advance-percent", type=float, default=0.0)
    s.add_argument("--retention-percent", type=float, default=0.0)
    s.add_argument("--payment-days", type=float, default=30.0)
    s.add_argument("--retention-release-months", type=float, default=0.0)
    s.add_argument("--interest-percent", type=float, default=8.0)
    return p


def main():
    args = build_parser().parse_args()
    if getattr(args, "margin_on", "cost") == "price" and getattr(args, "margin_percent", 0) >= 100:
        print("ERROR: --margin-percent must be below 100 when the margin is on price",
              file=sys.stderr)
        return 2
    try:
        args.func(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
