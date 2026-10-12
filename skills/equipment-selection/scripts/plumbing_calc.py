#!/usr/bin/env python3
"""Plumbing sizing calculations for equipment selection. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

Pipe pressure drop, pump power and water flow from load are in hvac_calc.py; use them here too.

Commands:
  peak-flow    cold water design flow from draw-off points
               --fixture basin:12 [--fixture wc:10] [--fixture shower:4:0.20] [-f FACTOR]
  dhw-mix      hot and cold water mixing
               --v-mix 200 --t-mix 45 --t-hot 60 --t-cold 10   (or --v-hot 150)
  dhw-demand   DHW peak power and energy from a draw
               --volume-l 200 --t-hot 60 --t-cold 10 --draw-time-min 10
  dhw-store    required storage volume after reheat during the draw
               --v-peak 300 --t-store 60 --t-cold 10 --t-mix 45 --continuous-kw 24 --draw-time-min 10
  dhw-circ     DHW circulation flow from the loop heat loss
               --heat-loss-w 500 --dt 5
  stack        drainage design flow from discharge units (EN 12056-2 method)
               --du 45 --k 0.7 [--capacity 6.2]
  rainwater    rainwater design flow from area, intensity and runoff
               --area-m2 1200 --intensity 300 --runoff 0.95

Fixture draw-off flows are TYPICAL values (EN 806-3 practice) and are marked "to verify" in
the output. The discharge units (--du) and the frequency factor K are NOT built in: give them
from the EN 12056-2 table for the project. Rainwater intensity is the local design value from
the jurisdiction rule; this script does not pick a return period.
"""

import argparse
import json
import sys

CP_WATER = 4.18  # kJ/(kg K), used for DHW energy
# Typical draw-off flow per fixture, l/s. Practice values, always to verify against EN 806-3.
FIXTURES = {
    "basin": 0.07, "washbasin": 0.07, "bidet": 0.07, "wc-cistern": 0.13, "wc": 0.13,
    "urinal": 0.07, "sink": 0.07, "kitchen-sink": 0.07, "shower": 0.15, "bath": 0.15,
    "washing-machine": 0.15, "dishwasher": 0.15, "tap-dn15": 0.15,
}


def r(x, n=3):
    return round(x, n)


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


def cmd_peak_flow(args):
    if args.factor is None:
        factor = 1.0
        factor_note = ("no --factor given, all draw-off points assumed open at the same time; "
                       "give the simultaneity factor from the sizing method (EN 806-3, or the "
                       "national method)")
    else:
        factor = args.factor
        factor_note = None
    rows, total = [], 0.0
    typed = []
    for spec in args.fixture:
        parts = spec.split(":")
        if not 1 <= len(parts) <= 3:
            raise ValueError(f"bad --fixture '{spec}'; use name:count[:flow]")
        name = parts[0].strip().lower()
        count = float(parts[1]) if len(parts) > 1 else 1.0
        if len(parts) == 3:
            flow, src = float(parts[2]), "user"
        elif name in FIXTURES:
            flow, src = FIXTURES[name], "typical, to verify"
        else:
            raise ValueError(f"unknown fixture '{name}'; give the flow as name:count:flow-l-s")
        subtotal = count * flow
        total += subtotal
        typed.append("typ" if src != "user" else "user")
        rows.append(f"{name} x{count:g} @ {flow} l/s = {r(subtotal)} l/s ({src})")
    design = total * factor
    notes = [f"  {row}" for row in rows]
    if "typ" in typed:
        notes.append("Fixture flows marked 'typical' must be confirmed against EN 806-3 or the "
                     "project fixture schedule.")
    if factor_note:
        notes.append(factor_note)
    notes.append("Next: size the pipes with hvac_calc.py pipe-dp at the chosen velocity, then sum "
                 "the index circuit losses (meter, PRV, pipes, fittings, valve, fixture).")
    out(args, "Cold water design flow",
        {"draw-off points": "; ".join(args.fixture), "sum of draw-off flows": f"{r(total)} l/s",
         "simultaneity factor": factor},
        "Qd = sum(count * flow per fixture) * factor",
        {"design flow": f"{r(design)} l/s", "design flow m3/h": f"{r(design * 3.6)} m3/h",
         "design flow l/min": f"{r(design * 60, 1)} l/min"}, notes)


def cmd_dhw_mix(args):
    if (args.v_mix is None) == (args.v_hot is None):
        raise ValueError("give exactly one of --v-mix or --v-hot")
    dh, dc = args.t_hot - args.t_cold, args.t_mix - args.t_cold
    if dh <= 0 or dc < 0 or args.t_mix > args.t_hot:
        raise ValueError("temperatures must satisfy t_cold <= t_mix <= t_hot")
    frac = dc / dh
    if args.v_mix is not None:
        v_mix, v_hot = args.v_mix, args.v_mix * frac
    else:
        v_hot = args.v_hot
        v_mix = v_hot / frac
    out(args, "Hot and cold water mixing",
        {"mixed volume": f"{r(v_mix, 1)} l", "mixed temperature": f"{args.t_mix} C",
         "hot temperature": f"{args.t_hot} C", "cold temperature": f"{args.t_cold} C"},
        "V_hot = V_mix * (t_mix - t_cold) / (t_hot - t_cold)",
        {"hot water needed": f"{r(v_hot, 1)} l", "cold water needed": f"{r(v_mix - v_hot, 1)} l",
         "hot fraction": r(frac, 4)},
        ["Mixing assumes no heat loss between the store and the outlet."])


def cmd_dhw_demand(args):
    e_kwh = args.volume_l * CP_WATER * (args.t_hot - args.t_cold) / 3600
    p_kw = e_kwh * 60 / args.draw_time_min
    out(args, "DHW peak power from a draw",
        {"draw volume": f"{args.volume_l} l", "hot temperature": f"{args.t_hot} C",
         "cold temperature": f"{args.t_cold} C", "draw time": f"{args.draw_time_min} min",
         "cp": f"{CP_WATER} kJ/(kg K)"},
        "E = V * cp * (t_hot - t_cold); P = E / draw time",
        {"energy": f"{r(e_kwh, 2)} kWh", "peak power during the draw": f"{r(p_kw, 1)} kW"},
        ["Check the heat source can deliver this power; otherwise storage covers the difference.",
         "The draw profile (volume and duration) comes from the project or the national rule."])


def cmd_dhw_store(args):
    dh = args.t_store - args.t_cold
    if dh <= 0 or not args.t_cold <= args.t_mix <= args.t_store:
        raise ValueError("temperatures must satisfy t_cold <= t_mix <= t_store, and "
                         "t_store > t_cold")
    v_store = args.v_peak * (args.t_mix - args.t_cold) / dh
    if args.continuous_kw:
        e_kwh = args.continuous_kw * args.draw_time_min / 60
        v_reheat = e_kwh * 3600 / (CP_WATER * dh)
    else:
        v_reheat = 0.0
    need = max(0.0, v_store - v_reheat)
    out(args, "DHW storage volume",
        {"peak mixed draw": f"{args.v_peak} l", "store temperature": f"{args.t_store} C",
         "cold temperature": f"{args.t_cold} C", "mixed temperature": f"{args.t_mix} C",
         "heat source continuous output": f"{args.continuous_kw} kW",
         "draw duration": f"{args.draw_time_min} min"},
        "V_store = V_peak * (t_mix - t_cold) / (t_store - t_cold); "
        "V_reheat = P * t / (cp * (t_store - t_cold))",
        {"volume at store temperature": f"{r(v_store, 0)} l",
         "volume reheated during the draw": f"{r(v_reheat, 0)} l",
         "storage to select (at least)": f"{r(need, 0)} l"},
        ["Add the draw-off from the store during the draw plus the reheat time when the peak "
         "lasts longer than one draw; check the recovery time the client accepts.",
         "Select a cylinder with a declared DHW performance (peak flow and continuous flow) "
         "from the manufacturer data, not by volume alone."])


def cmd_dhw_circ(args):
    # rho*cp ~ 4180 J/(l K); W / (J/(l K) * K) = l/s
    q_ls = args.heat_loss_w / (CP_WATER * 1000 * args.dt)
    out(args, "DHW circulation flow",
        {"loop heat loss": f"{args.heat_loss_w} W", "accepted temperature drop": f"{args.dt} K"},
        "V = Q_loss / (rho * cp * dT)",
        {"circulation flow": f"{r(q_ls)} l/s", "circulation flow l/h": f"{r(q_ls * 3600, 0)} l/h"},
        ["Loop heat loss comes from the pipe lengths, insulation and temperatures; calculate it "
         "or take it from the project.",
         "Pump head: sum the circulation loop pressure drop with hvac_calc.py pipe-dp, then "
         "hvac_calc.py pump-power."])


def cmd_stack(args):
    q = args.k * (args.du ** 0.5)
    notes = ["Method per EN 12056-2 (design flow from discharge units and the frequency "
             "factor). Check the formula and the capacity table in the licensed standard copy."]
    results = {"design flow": f"{r(q, 2)} l/s", "sum of discharge units": f"{args.du:g}",
               "frequency factor K": f"{args.k}"}
    if args.capacity is not None:
        results["stack capacity given"] = f"{args.capacity} l/s"
        results["verdict"] = "OK" if q <= args.capacity else "EXCEEDS CAPACITY"
        if q > args.capacity:
            notes.append("Design flow above the capacity: use a larger stack, ventilate the "
                         "stack, or split the discharge.")
    else:
        notes.append("Give --capacity from the EN 12056-2 table for the chosen stack diameter "
                     "to check the selection.")
    out(args, "Drainage design flow",
        {"sum of discharge units DU": f"{args.du:g}", "frequency factor K": f"{args.k}"},
        "Qww = K * sqrt(DU)",
        results, notes)


def cmd_rainwater(args):
    q = args.intensity * args.area_m2 * args.runoff / 10000  # l/(s ha) * m2 -> l/s
    out(args, "Rainwater design flow",
        {"drained area (plan view)": f"{args.area_m2} m2",
         "design rainfall intensity": f"{args.intensity} l/(s ha)",
         "runoff coefficient": f"{args.runoff}"},
        "Q = r * A * C / 10000",
        {"design flow": f"{r(q, 2)} l/s", "design flow l/min": f"{r(q * 60, 0)} l/min"},
        ["Rainfall intensity and the return period come from the jurisdiction rule or the "
         "national standard (EN 12056-3, EN 752). State both.",
         "Size the secondary (overflow) system for a longer return period than the primary, "
         "and check the outlet and gutter capacity at the design flow."])


def build_parser():
    p = argparse.ArgumentParser(description="Plumbing sizing calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    s = add("peak-flow", cmd_peak_flow)
    s.add_argument("--fixture", action="append", required=True, metavar="NAME:COUNT[:FLOW]")
    s.add_argument("-f", "--factor", type=positive, default=None)

    s = add("dhw-mix", cmd_dhw_mix)
    s.add_argument("--v-mix", type=positive)
    s.add_argument("--v-hot", type=positive)
    s.add_argument("--t-mix", type=float, required=True)
    s.add_argument("--t-hot", type=float, required=True)
    s.add_argument("--t-cold", type=float, required=True)

    s = add("dhw-demand", cmd_dhw_demand)
    s.add_argument("--volume-l", type=positive, required=True)
    s.add_argument("--t-hot", type=float, required=True)
    s.add_argument("--t-cold", type=float, required=True)
    s.add_argument("--draw-time-min", type=positive, required=True)

    s = add("dhw-store", cmd_dhw_store)
    s.add_argument("--v-peak", type=positive, required=True)
    s.add_argument("--t-store", type=float, required=True)
    s.add_argument("--t-cold", type=float, required=True)
    s.add_argument("--t-mix", type=float, required=True)
    s.add_argument("--continuous-kw", type=float, default=0.0)
    s.add_argument("--draw-time-min", type=positive, default=10.0)

    s = add("dhw-circ", cmd_dhw_circ)
    s.add_argument("--heat-loss-w", type=positive, required=True)
    s.add_argument("--dt", type=positive, required=True)

    s = add("stack", cmd_stack)
    s.add_argument("--du", type=positive, required=True)
    s.add_argument("--k", type=positive, required=True)
    s.add_argument("--capacity", type=positive)

    s = add("rainwater", cmd_rainwater)
    s.add_argument("--area-m2", type=positive, required=True)
    s.add_argument("--intensity", type=positive, required=True)
    s.add_argument("--runoff", type=positive, default=1.0)
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
