#!/usr/bin/env python3
"""Electrical sizing calculations for equipment selection. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

The script does no standard selection: it does not pick the supply system, the protection
device or the standard rating. Those come from HD 60364, the national law and the project.

Commands:
  load-current  current from power (kW or kVA)
                --power-kw 30 --voltage 400 --cos-phi 0.9 --phases 3
                --power-kva 50 --voltage 400 --phases 3
  cable-drop    voltage drop, or the minimum section for a drop limit
                --current-a 63 --length-m 80 --section-mm2 25 --voltage 400 --phases 3
                [--cos-phi 0.9] [--rho 0.0225] [--x-ohm-km 0.08] [--max-drop-percent 5 --size]
  correction    cable rating after correction factors
                --iz 63 --factor 0.82 --factor 0.90
  fault-current loop impedance to fault current
                --voltage 230 --impedance-mohm 320
  zs-max        maximum earth fault loop impedance for a device
                --u0 230 --ia-a 80 [--cmin 0.95]
  diversity     load list to design load
                --load-kw 120 --factor 0.7
  lighting      luminaire count for an illuminance
                --lux 300 --area-m2 120 --flux-lm 4000 --uf 0.75 --mf 0.80
  battery       battery capacity for an autonomy time
                --load-w 800 --autonomy-h 0.5 --voltage 48 --dod 0.8 [--eff 0.9]

Conductor resistivity defaults to copper at operating temperature (0.0225 ohm mm2/m). The
voltage drop ignores reactance when --x-ohm-km is set to 0, which is often done for small
sections; state that assumption when you do it.
"""

import argparse
import json
import math
import sys

SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
RHO_CU = 0.0225  # ohm mm2/m, copper at about 70 C
X_DEFAULT_OHM_KM = 0.08


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


def phase_factor(phases):
    return 2.0 if phases == 1 else math.sqrt(3.0)


def cmd_load_current(args):
    if args.power_kw is not None and args.power_kva is not None:
        raise ValueError("give only one of --power-kw or --power-kva")
    if args.power_kw is None and args.power_kva is None:
        raise ValueError("give --power-kw or --power-kva")
    if args.power_kw is not None and args.phases == 3 and args.cos_phi is None:
        raise ValueError("--cos-phi is required for a three-phase kW load")
    b = phase_factor(args.phases)
    if args.power_kw is not None:
        cp = args.cos_phi if args.cos_phi is not None else 1.0
        kva = args.power_kw / cp
        i = args.power_kw * 1000 / (b * args.voltage * cp)
        inputs = {"active power": f"{args.power_kw} kW", "voltage": f"{args.voltage} V",
                  "cos phi": cp, "phases": args.phases, "b factor": f"{r(b)}"}
        formula = "P1 = U * I * cos phi; P3 = sqrt(3) * U * I * cos phi"
    else:
        cp = args.cos_phi
        kva = args.power_kva
        i = args.power_kva * 1000 / (b * args.voltage)
        inputs = {"apparent power": f"{args.power_kva} kVA", "voltage": f"{args.voltage} V",
                  "phases": args.phases, "b factor": f"{r(b)}"}
        formula = "S = b * U * I"
    results = {"load current": f"{r(i, 2)} A", "apparent power": f"{r(kva, 3)} kVA"}
    if cp is not None:
        results["active power"] = f"{r(kva * cp, 3)} kW"
        results["reactive power"] = f"{r(kva * math.sqrt(max(0.0, 1 - cp * cp)), 3)} kvar"
    out(args, "Load current", inputs, formula, results,
        ["Next: choose the protective device rating above this current, then check that the "
         "cable rating after correction is at or above the device rating (Ib <= In <= Iz)."])


def cmd_cable_drop(args):
    x_ohm_m = args.x_ohm_km / 1000.0
    cp = args.cos_phi
    sp = math.sqrt(max(0.0, 1 - cp * cp))
    b = phase_factor(args.phases)
    notes = []
    if args.x_ohm_km == 0:
        notes.append("reactance set to 0: valid for short runs and small sections, say so in "
                     "the sheet")
    if args.size:
        if args.max_drop_percent is None:
            raise ValueError("--size needs --max-drop-percent")
        du_max = args.max_drop_percent / 100 * args.voltage
        s_min = b * args.current_a * args.length_m * args.rho * cp / du_max
        chosen = next((s for s in SIZES if s >= s_min), None)
        if chosen is None:
            notes.append("required section above the list; split the circuit or use a busbar")
        out(args, "Minimum cable section for a voltage drop limit",
            {"current": f"{args.current_a} A", "length": f"{args.length_m} m",
             "voltage": f"{args.voltage} V", "phases": args.phases, "cos phi": cp,
             "rho": f"{args.rho} ohm mm2/m", "max drop": f"{args.max_drop_percent} %",
             "max drop volts": f"{r(du_max, 2)} V"},
            "S >= b * I * L * rho * cos phi / du_max (reactance neglected)",
            {"required section": f"{r(s_min, 2)} mm2",
             "next standard size": f"{chosen} mm2" if chosen else "above 300 mm2"}, notes)
        return
    if args.section_mm2 is None:
        raise ValueError("give --section-mm2, or --max-drop-percent with --size")
    r_ohm_m = args.rho / args.section_mm2
    du = b * args.current_a * args.length_m * (r_ohm_m * cp + x_ohm_m * sp)
    percent = du / args.voltage * 100
    if args.max_drop_percent is not None:
        notes.append("verdict: " + ("OK" if percent <= args.max_drop_percent
                                    else f"EXCEEDS the {args.max_drop_percent} % limit"))
    else:
        notes.append("compare with the limit for this circuit type (typical 3 % lighting, "
                     "5 % other) or the national rule")
    out(args, "Cable voltage drop",
        {"current": f"{args.current_a} A", "length": f"{args.length_m} m",
         "section": f"{args.section_mm2} mm2", "conductor": f"{args.material}",
         "rho": f"{args.rho} ohm mm2/m", "reactance": f"{args.x_ohm_km} ohm/km",
         "voltage": f"{args.voltage} V", "phases": args.phases, "cos phi": cp},
        "du = b * I * L * (rho/S * cos phi + X * sin phi); percent = du / U * 100",
        {"resistance": f"{r(r_ohm_m * 1000, 4)} mohm/m", "voltage drop V": f"{r(du, 2)} V",
         "voltage drop %": f"{r(percent, 2)} %",
         "voltage at the load": f"{r(args.voltage - du, 1)} V"}, notes)


def cmd_correction(args):
    product = 1.0
    for f in args.factor:
        product *= f
    iz = args.iz * product
    low = [f for f in args.factor if f < 0.7]
    notes = ["Correction factors come from HD 60364-5-52 tables (ambient temperature, "
             "grouping, soil, thermal insulation). Take each one from the table for the "
             "actual installation method."]
    if low:
        notes.append("A factor below 0.7 is rare; check the table entry and the installation "
                     "method again.")
    out(args, "Cable rating after correction",
        {"tabulated rating Iz0": f"{args.iz} A",
         "factors": " * ".join(f"{f}" for f in args.factor)},
        "Iz = Iz0 * f1 * f2 * ...",
        {"combined factor": r(product, 4), "corrected rating Iz": f"{r(iz, 2)} A",
         "max design current Ib": f"{r(iz, 2)} A"}, notes)


def cmd_fault_current(args):
    z = args.impedance_mohm / 1000.0
    i = args.voltage / z
    out(args, "Fault current from loop impedance",
        {"nominal voltage": f"{args.voltage} V", "loop impedance": f"{args.impedance_mohm} mohm",
         "rho note": "impedance is the whole loop (phase + protective conductor, or source)"},
        "Ik = U / Z_loop",
        {"fault current": f"{r(i, 1)} A", "in kA": f"{r(i / 1000, 3)} kA"},
        ["For a three-phase fault use the line voltage and the line-to-line loop impedance. "
         "Here a single-phase (phase to neutral or phase to earth) fault is assumed."])


def cmd_zs_max(args):
    zs = args.cmin * args.u0 / args.ia_a
    out(args, "Maximum earth fault loop impedance",
        {"nominal voltage U0": f"{args.u0} V", "device current Ia": f"{args.ia_a} A",
         "Cmin": args.cmin},
        "Zs_max = Cmin * U0 / Ia",
        {"Zs_max": f"{r(zs, 4)} ohm"},
        ["Ia is the current that operates the protective device within the disconnection time "
         "required by HD 60364 for this circuit (from the device trip curve, not from In).",
         "Compare with the measured or calculated Zs of the circuit, and check the disconnection "
         "time for the circuit type."])


def cmd_diversity(args):
    out(args, "Diversity applied to a load list",
        {"connected load": f"{args.load_kw} kW", "diversity factor": args.factor},
        "design load = connected load * factor",
        {"design load": f"{r(args.load_kw * args.factor, 3)} kW"},
        ["Apply the diversity once, at this level. Do not apply it again upstream, and keep any "
         "growth allowance separate and stated."])


def cmd_lighting(args):
    raw = args.lux * args.area_m2 / (args.flux_lm * args.uf * args.mf)
    n = math.ceil(raw)
    achieved = n * args.flux_lm * args.uf * args.mf / args.area_m2
    out(args, "Luminaire count",
        {"required illuminance": f"{args.lux} lx", "area": f"{args.area_m2} m2",
         "luminaire flux": f"{args.flux_lm} lm", "utilisation factor": args.uf,
         "maintenance factor": args.mf},
        "N = E * A / (flux * UF * MF)",
        {"calculated number": f"{r(raw, 2)}", "round up to": f"{n}",
         "achieved illuminance": f"{r(achieved, 0)} lx"},
        ["This is a lumen method check, not a lighting design. Glare (UGR), uniformity and "
         "room surfaces need a real lighting calculation.",
         "Take UF from the luminaire manufacturer data for the room index, and MF from the "
         "cleaning and replacement cycle the client accepts."])


def cmd_battery(args):
    ah = args.load_w * args.autonomy_h / (args.eff * args.voltage * args.dod)
    out(args, "Battery capacity for an autonomy time",
        {"load": f"{args.load_w} W", "autonomy": f"{args.autonomy_h} h",
         "system voltage": f"{args.voltage} V", "depth of discharge": args.dod,
         "efficiency": args.eff},
        "Ah = P * t / (eta * U * DOD)",
        {"required capacity": f"{r(ah, 1)} Ah",
         "energy delivered": f"{r(args.load_w * args.autonomy_h / args.eff / 1000, 2)} kWh"},
        ["Add the ageing allowance the client accepts and check the discharge rate; capacity "
         "falls at high discharge current. Check the room ventilation for the battery type."])


def build_parser():
    p = argparse.ArgumentParser(description="Electrical sizing calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    s = add("load-current", cmd_load_current)
    s.add_argument("--power-kw", type=positive)
    s.add_argument("--power-kva", type=positive)
    s.add_argument("--voltage", type=positive, required=True)
    s.add_argument("--cos-phi", type=float)
    s.add_argument("--phases", type=int, choices=[1, 3], default=3)

    s = add("cable-drop", cmd_cable_drop)
    s.add_argument("--current-a", type=positive, required=True)
    s.add_argument("--length-m", type=positive, required=True)
    s.add_argument("--section-mm2", type=positive)
    s.add_argument("--voltage", type=positive, required=True)
    s.add_argument("--phases", type=int, choices=[1, 3], default=3)
    s.add_argument("--cos-phi", type=float, default=0.9)
    s.add_argument("--rho", type=positive, default=RHO_CU)
    s.add_argument("--material", default="copper")
    s.add_argument("--x-ohm-km", type=float, default=X_DEFAULT_OHM_KM)
    s.add_argument("--max-drop-percent", type=positive)
    s.add_argument("--size", action="store_true")

    s = add("correction", cmd_correction)
    s.add_argument("--iz", type=positive, required=True)
    s.add_argument("--factor", type=positive, action="append", required=True)

    s = add("fault-current", cmd_fault_current)
    s.add_argument("--voltage", type=positive, default=230.0)
    s.add_argument("--impedance-mohm", type=positive, required=True)

    s = add("zs-max", cmd_zs_max)
    s.add_argument("--u0", type=positive, default=230.0)
    s.add_argument("--ia-a", type=positive, required=True)
    s.add_argument("--cmin", type=positive, default=0.95)

    s = add("diversity", cmd_diversity)
    s.add_argument("--load-kw", type=positive, required=True)
    s.add_argument("--factor", type=positive, required=True)

    s = add("lighting", cmd_lighting)
    s.add_argument("--lux", type=positive, required=True)
    s.add_argument("--area-m2", type=positive, required=True)
    s.add_argument("--flux-lm", type=positive, required=True)
    s.add_argument("--uf", type=positive, default=0.75)
    s.add_argument("--mf", type=positive, default=0.80)

    s = add("battery", cmd_battery)
    s.add_argument("--load-w", type=positive, required=True)
    s.add_argument("--autonomy-h", type=positive, required=True)
    s.add_argument("--voltage", type=positive, required=True)
    s.add_argument("--dod", type=positive, default=0.8)
    s.add_argument("--eff", type=positive, default=0.9)
    return p


def main():
    args = build_parser().parse_args()
    cp = getattr(args, "cos_phi", None)
    if cp is not None and not 0 < cp <= 1:
        print("ERROR: --cos-phi must be in (0, 1]", file=sys.stderr)
        return 2
    for name in ("dod", "uf", "mf"):
        v = getattr(args, name, None)
        if v is not None and v > 1:
            print(f"ERROR: --{name.replace('_', '-')} is a fraction, for example 0.8", file=sys.stderr)
            return 2
    try:
        args.func(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
