#!/usr/bin/env python3
"""Fire protection calculations for equipment selection. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

Fire pump head and power, and pipe pressure drop, are in hvac_calc.py; use them here too.

The script does NOT contain the design density, the design area, the water supply duration,
the detector spacing or the smoke control method. Take each one from the standard or from the
fire safety concept for the building, state the source and give the clause.

Commands:
  sprinkler-flow  design flow from density and design area
                  --density 5 --area-m2 216 [--hose-allowance-l-min 900]
  water-reserve   water reserve from flow and duration
                  --flow-l-min 1800 --duration-min 60
  smoke-exhaust   exhaust flow from an air change rate or from a design fire
                  --volume-m3 12000 --ach 10
                  --fire-kw 3000 --height-m 4 [--method plume] [--smoke-temp 60]
  detector-count  detector count from the spacing
                  --area-m2 1200 --spacing-m 10 [--factor 1.0]
"""

import argparse
import json
import math
import sys

CP_AIR = 1.005  # kJ/(kg K)
HEAT_TO_CONVECTIVE = 0.7  # Heskestad: convective part of the heat release rate


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


def cmd_sprinkler_flow(args):
    q = args.density * args.area_m2
    total = q + args.hose_allowance_l_min
    out(args, "Sprinkler design flow",
        {"design density": f"{args.density} mm/min", "design area": f"{args.area_m2} m2",
         "hose allowance": f"{args.hose_allowance_l_min} l/min",
         "density source": "to state: standard or fire safety concept, with the clause"},
        "Q = density * area + hose allowance",
        {"sprinkler flow l/min": f"{r(q, 0)} l/min", "sprinkler flow l/s": f"{r(q / 60, 2)} l/s",
         "hose allowance l/min": f"{args.hose_allowance_l_min} l/min",
         "total design flow l/min": f"{r(total, 0)} l/min",
         "total design flow l/s": f"{r(total / 60, 2)} l/s",
         "total m3/h": f"{r(total * 0.06, 1)} m3/h"},
        ["The density, the design area and the hose allowance come from the standard or the "
         "concept. The number of operating heads assumed by the standard is part of the "
         "hydraulic calculation, not of this flow.",
         "Next: hydraulic calculation of the most remote area with hvac_calc.py pipe-dp, then "
         "the pump duty with hvac_calc.py pump-power."])


def cmd_water_reserve(args):
    v = args.flow_l_min * args.duration_min / 1000
    out(args, "Fire water reserve",
        {"design flow": f"{args.flow_l_min} l/min", "supply duration": f"{args.duration_min} min",
         "duration source": "to state: standard or national rule, with the clause"},
        "V = Q * t",
        {"reserve volume m3": f"{r(v, 1)} m3",
         "reserve volume l": f"{r(v * 1000, 0)} l"},
        ["The duration comes from the standard or the national rule, not from this script.",
         "Check the refill time and its source (network, tanker, second tank) as well, and the "
         "tank's usable volume above the pump suction and below the overflow."])


def cmd_smoke_exhaust(args):
    if args.volume_m3 is not None and args.fire_kw is not None:
        raise ValueError("give either --volume-m3 with --ach, or --fire-kw with --height-m")
    if args.volume_m3 is not None:
        if args.ach is None:
            raise ValueError("--volume-m3 needs --ach")
        v = args.volume_m3 * args.ach
        out(args, "Smoke exhaust flow from an air change rate",
            {"room volume": f"{args.volume_m3} m3", "air change rate": f"{args.ach} 1/h",
             "air change rule source": "to state: national rule or fire safety concept"},
            "V = room volume * air change rate",
            {"exhaust flow m3/h": f"{r(v, 0)} m3/h", "exhaust flow m3/s": f"{r(v / 3600, 2)} m3/s"},
            ["The air change rate comes from the national rule or the concept for the room "
             "type. State the source and the clause.",
             "Check the make-up air path and its velocity, and the fan temperature class (F "
             "class) for the required duration."])
        return
    if args.fire_kw is None or args.height_m is None:
        raise ValueError("give --volume-m3 with --ach, or --fire-kw with --height-m")
    qc = HEAT_TO_CONVECTIVE * args.fire_kw
    m = 0.071 * (qc ** (1.0 / 3.0)) * (args.height_m ** (5.0 / 3.0)) + 0.0018 * qc
    rho = 353.0 / (args.smoke_temp + 273.15)
    v = m / rho
    out(args, "Smoke exhaust flow from a design fire (plume)",
        {"design fire": f"{args.fire_kw} kW", "convective fraction": HEAT_TO_CONVECTIVE,
         "height above the fire": f"{args.height_m} m", "smoke temperature": f"{args.smoke_temp} C",
         "smoke density": f"{r(rho)} kg/m3"},
        "Qc = 0.7 * Q; m = 0.071 * Qc^(1/3) * z^(5/3) + 0.0018 * Qc; V = m / rho",
        {"convective heat": f"{r(qc, 0)} kW", "plume mass flow": f"{r(m, 2)} kg/s",
         "exhaust flow m3/s": f"{r(v, 2)} m3/s", "exhaust flow m3/h": f"{r(v * 3600, 0)} m3/h"},
        ["Heskestad axisymmetric plume equation, as used in smoke control practice. Check it "
         "against the standard or the fire safety concept for the project before using it.",
         "The smoke temperature is an assumption here: the plume temperature depends on the "
         "fire, the height and the entrainment. State the temperature you used.",
         "Check the smoke layer height, the make-up air, and the fan temperature class (F class) "
         "with the required duration."])


def cmd_detector_count(args):
    effective = args.spacing_m / math.sqrt(args.factor)
    per = args.area_m2 / (effective * effective)
    n = math.ceil(per)
    out(args, "Detector count",
        {"area": f"{args.area_m2} m2", "detector spacing": f"{args.spacing_m} m",
         "spacing factor": args.factor,
         "spacing source": "to state: standard clause, with the ceiling height limit"},
        "N = area / spacing^2",
        {"spacing used": f"{r(effective, 2)} m", "calculated number": f"{r(per, 2)}",
         "round up to": f"{n}"},
        ["Spacing and the ceiling height limit come from the detection standard for the "
         "detector type (CEN/TS 54-14 and the detector manufacturer data).",
         "Add detectors for the walls, the corners, the beams and the obstructions per the "
         "standard; this count is a first estimate only.",
         "Check the detector type against the environment of the room (dust, steam, vehicles)."])


def build_parser():
    p = argparse.ArgumentParser(description="Fire protection calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    s = add("sprinkler-flow", cmd_sprinkler_flow)
    s.add_argument("--density", type=positive, required=True, help="mm/min")
    s.add_argument("--area-m2", type=positive, required=True)
    s.add_argument("--hose-allowance-l-min", type=positive, default=0.0)

    s = add("water-reserve", cmd_water_reserve)
    s.add_argument("--flow-l-min", type=positive, required=True)
    s.add_argument("--duration-min", type=positive, required=True)

    s = add("smoke-exhaust", cmd_smoke_exhaust)
    s.add_argument("--volume-m3", type=positive)
    s.add_argument("--ach", type=positive)
    s.add_argument("--fire-kw", type=positive)
    s.add_argument("--height-m", type=positive)
    s.add_argument("--method", choices=["plume"], default="plume")
    s.add_argument("--smoke-temp", type=float, default=60.0)

    s = add("detector-count", cmd_detector_count)
    s.add_argument("--area-m2", type=positive, required=True)
    s.add_argument("--spacing-m", type=positive, required=True)
    s.add_argument("--factor", type=positive, default=1.0)
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
