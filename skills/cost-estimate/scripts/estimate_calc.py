#!/usr/bin/env python3
"""Cost estimate calculations. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

The script does no pricing of its own: every unit rate, quantity and percentage comes from
the user, the tender documents, the project or a named price source. Lines without a source
are listed at the end of the rollup as "to verify".

Commands:
  line            value of one line
                  --qty 145.5 --unit-rate 210.50 --unit m2 [--name "..." ] [--kind r|m|s]
  rate-from-total unit rate back-calculated from a total
                  --total 30650.25 --qty 145.5 [--unit m2]
  rollup          group and line totals with the markup cascade (R, M, S then Kp, Z, Kz, VAT)
                  --file boq.json [--json]
  escalation      compound escalation between a price level and a later period
                  --value 1250000 --percent 4.5 --periods 2
  range           estimate range around a value
                  --value 1250000 --percent 15 [--low-percent 20]

rollup input file (JSON):
{
  "currency": "PLN",
  "price_level": "2026-09",
  "vat_percent": 23,
  "markups": {"kp_percent": 66.0, "z_percent": 11.0, "kz_percent": 4.0},
  "groups": [
    {"code": "1", "name": "Roboty ziemne",
     "lines": [{"name": "Wykop", "qty": 100, "unit": "m3", "unit_rate": 85.0,
                "kind": "r", "source": "KNR 2-01, tab. 0101"}]}
  ]
}

Markup cascade, applied once each, in this order:
  Kp = kp% * (R + S);  Z = z% * (R + S + Kp);  Kz = kz% * M
  net = direct + Kp + Z + Kz;  tax = vat% * net;  gross = net + tax
Kp, Z and Kz are applied only when the lines carry a kind (r, m or s), because their bases
need the split. Without kinds the rollup gives direct costs and VAT only, and says so.

Python floats are used for the arithmetic. For an estimate this is exact enough at 0.01;
a certified bill of quantities should be recalculated in the client's own system.
"""

import argparse
import json
import sys


def fmt(x, n=2):
    return f"{round(x, n):.{n}f}"


def num(x):
    return f"{x:,.2f}".replace(",", " ")


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


def cmd_line(args):
    value = args.qty * args.unit_rate
    inputs = {"name": args.name or "-", "quantity": f"{args.qty} {args.unit}",
              "unit rate": fmt(args.unit_rate)}
    if args.kind:
        inputs["cost kind"] = args.kind.upper()
    if args.source:
        inputs["rate source"] = args.source
    notes = []
    if not args.source:
        notes.append("no --source given: this rate has no source and goes to 'to verify'")
    out(args, "Estimate line value", inputs, "value = quantity * unit rate",
        {"value": fmt(value)}, notes)


def cmd_rate_from_total(args):
    if args.qty == 0:
        raise ValueError("--qty must not be 0")
    rate = args.total / args.qty
    out(args, "Unit rate from a total",
        {"total": fmt(args.total), "quantity": f"{args.qty} {args.unit or '-'}"},
        "unit rate = total / quantity",
        {"unit rate": fmt(rate)},
        ["Use this to compare a lump sum with a measured rate, or to check a rate the client "
         "gave as a total."])


def load_boq(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if "groups" not in data:
        raise ValueError("the file has no 'groups' list")
    return data


def cmd_rollup(args):
    data = load_boq(args.file)
    currency = data.get("currency", "")
    vat_percent = data.get("vat_percent")
    markups = data.get("markups", {}) or {}
    kp_percent = markups.get("kp_percent", 0.0) or 0.0
    z_percent = markups.get("z_percent", 0.0) or 0.0
    kz_percent = markups.get("kz_percent", 0.0) or 0.0

    groups_out, unsourced = [], []
    total_direct = 0.0
    sum_r = sum_m = sum_s = sum_other = 0.0
    kinds_used = False
    for group in data["groups"]:
        lines_out = []
        group_total = 0.0
        for line in group.get("lines", []):
            qty = float(line.get("qty", 0) or 0)
            rate = line.get("unit_rate")
            if rate is None:
                raise ValueError(f"line '{line.get('name','?')}' in group "
                                 f"'{group.get('name','?')}' has no unit_rate")
            rate = float(rate)
            value = qty * rate
            kind = (line.get("kind") or "").lower()
            if kind:
                kinds_used = True
            if kind == "r":
                sum_r += value
            elif kind == "m":
                sum_m += value
            elif kind == "s":
                sum_s += value
            else:
                sum_other += value
            if not line.get("source"):
                unsourced.append(f"{group.get('name','?')} / {line.get('name','?')}")
            group_total += value
            lines_out.append({"name": line.get("name", ""), "qty": qty,
                              "unit": line.get("unit", ""), "unit_rate": rate, "value": value,
                              "kind": kind, "source": line.get("source", "")})
        total_direct += group_total
        groups_out.append({"code": group.get("code", ""), "name": group.get("name", ""),
                           "total": group_total, "lines": lines_out})

    kp = kp_percent / 100 * (sum_r + sum_s) if kinds_used else 0.0
    z = z_percent / 100 * (sum_r + sum_s + kp) if kinds_used else 0.0
    kz = kz_percent / 100 * sum_m if kinds_used else 0.0
    net = total_direct + kp + z + kz
    vat = (vat_percent / 100 * net) if vat_percent else 0.0
    gross = net + vat

    notes = []
    if not kinds_used:
        notes.append("no line carries a kind (r, m or s), so Kp, Z and Kz were not applied. "
                     "Give kinds when the method needs the R, M, S split.")
    elif sum_other:
        notes.append(f"{sum_other:,.2f} of direct costs have no kind: they take no Kp, Z or Kz "
                     "basis. Label them or say why they stay unlabelled.".replace(",", " "))
    if not vat_percent:
        notes.append("no vat_percent in the file: the gross total is equal to net")
    if unsourced:
        notes.append(f"{len(unsourced)} line(s) have no rate source and are 'to verify'")
    for pct, name in ((kp_percent, "kp"), (z_percent, "z"), (kz_percent, "kz")):
        if not markups.get(f"{name}_source") and pct:
            notes.append(f"{name.upper()} = {pct} % has no source in the file; the contract or "
                         "the client must give it")

    results = {"direct costs": num(total_direct)}
    if kinds_used:
        results.update({"R labour": num(sum_r), "M materials": num(sum_m),
                        "S equipment": num(sum_s)})
        if kp_percent:
            results[f"Kp {kp_percent} % of (R+S)"] = num(kp)
        if z_percent:
            results[f"Z {z_percent} % of (R+S+Kp)"] = num(z)
        if kz_percent:
            results[f"Kz {kz_percent} % of M"] = num(kz)
    results["net total"] = num(net)
    if vat_percent:
        results[f"VAT {vat_percent} %"] = num(vat)
    results["gross total"] = num(gross)
    results["currency"] = currency or "not stated"
    results["price level"] = data.get("price_level", "not stated")

    if args.json:
        payload = {"currency": currency, "price_level": data.get("price_level"),
                   "groups": groups_out, "direct": total_direct, "r": sum_r, "m": sum_m,
                   "s": sum_s, "unclassified": sum_other, "kp": kp, "z": z, "kz": kz,
                   "net": net, "vat": vat, "gross": gross, "unsourced": unsourced,
                   "notes": notes}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"== Estimate rollup ==   currency: {currency or 'not stated'}   "
          f"price level: {data.get('price_level', 'not stated')}")
    for group in groups_out:
        print(f"\n[{group['code']}] {group['name']}   subtotal: {num(group['total'])}")
        for line in group["lines"]:
            flag = "" if line["source"] else "   <-- TO VERIFY (no source)"
            print(f"  {line['name']}: {line['qty']} {line['unit']} x {fmt(line['unit_rate'])}"
                  f" = {num(line['value'])}{flag}")
    print("\nTotals:")
    for k, v in results.items():
        print(f"  {k}: {v}")
    if unsourced:
        print("\nLines without a source (to verify):")
        for item in unsourced:
            print(f"  - {item}")
    for n in notes:
        print(f"Note: {n}")


def cmd_escalation(args):
    value = args.value
    escalated = value * (1 + args.percent / 100) ** args.periods
    out(args, "Escalation",
        {"value at the price level": num(value), "index per period": f"{args.percent} %",
         "periods": args.periods},
        "value_2 = value_1 * (1 + i)^n",
        {"escalated value": num(escalated),
         "increase": num(escalated - value),
         "increase percent": f"{fmt((escalated / value - 1) * 100)} %"},
        ["Cite the index and its source. Escalation is not a contingency: keep them separate.",
         "One period is one year of the index series unless the contract says otherwise."])


def cmd_range(args):
    low_pct = args.low_percent if args.low_percent is not None else args.percent
    low = args.value * (1 - low_pct / 100)
    high = args.value * (1 + args.percent / 100)
    out(args, "Estimate range",
        {"central value": num(args.value), "range up": f"{args.percent} %",
         "range down": f"{low_pct} %"},
        "low = value * (1 - low%); high = value * (1 + high%)",
        {"low": num(low), "central": num(args.value), "high": num(high)},
        ["State the estimate class behind the range (conceptual, early design, detailed "
         "takeoff, priced BOQ) and what the estimate is based on."])


def positive(x):
    v = float(x)
    if v <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return v


def build_parser():
    p = argparse.ArgumentParser(description="Cost estimate calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    s = add("line", cmd_line)
    s.add_argument("--qty", type=float, required=True)
    s.add_argument("--unit-rate", type=float, required=True)
    s.add_argument("--unit", default="")
    s.add_argument("--name", default="")
    s.add_argument("--kind", choices=["r", "m", "s"])
    s.add_argument("--source", default="")

    s = add("rate-from-total", cmd_rate_from_total)
    s.add_argument("--total", type=float, required=True)
    s.add_argument("--qty", type=float, required=True)
    s.add_argument("--unit", default="")

    s = add("rollup", cmd_rollup)
    s.add_argument("--file", required=True)

    s = add("escalation", cmd_escalation)
    s.add_argument("--value", type=positive, required=True)
    s.add_argument("--percent", type=float, required=True)
    s.add_argument("--periods", type=positive, default=1.0)

    s = add("range", cmd_range)
    s.add_argument("--value", type=positive, required=True)
    s.add_argument("--percent", type=float, required=True)
    s.add_argument("--low-percent", type=float)
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
