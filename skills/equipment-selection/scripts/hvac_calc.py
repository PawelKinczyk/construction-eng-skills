#!/usr/bin/env python3
"""HVAC sizing calculations for equipment selection. Standard library only.

Every command prints inputs, formula, result and units. Add --json for machine output.

Commands:
  water-flow   heat or cooling load -> water flow
               --load-kw 120 --dt 20 [--temp 60] [--rho R --cp CP]
  air-flow     sensible load -> supply airflow
               --load-kw 12 --dt 8 [--air-temp 20]
  pipe-dp      friction and local loss in a pipe
               --flow-m3h 5.2 --id-mm 53.1 --length-m 120 [--temp 60] [--roughness-mm 0.045]
               [--zeta 6.5] [--rho R --mu-mpas MU]
  duct-dp      friction and local loss in a duct (round or rectangular)
               --flow-m3h 3600 (--d-mm 400 | --a-mm 500 --b-mm 300) --length-m 40
               [--roughness-mm 0.15] [--zeta 2.1] [--air-temp 20]
  pump-power   hydraulic and shaft power, head conversion
               --flow-m3h 5.2 (--head-m 6 | --dp-kpa 59) [--eff 0.55] [--temp 60]
  fan-power    shaft power and SFP
               --flow-m3h 10000 --dp-pa 650 [--eff 0.65]
  margin       apply a percentage margin
               --value 5.2 --percent 10

Fluid properties: water from a table 0-100 C (linear interpolation). Glycol mixtures are
NOT built in: pass --rho, --cp and --mu-mpas from the glycol manufacturer data sheet.
Air density: ideal gas at 101325 Pa.
"""

import argparse
import json
import math
import sys

G = 9.81  # m/s2
P_ATM = 101325.0  # Pa
R_AIR = 287.05  # J/(kg K)
CP_AIR = 1.005  # kJ/(kg K)
MU_AIR = 1.81e-5  # Pa s at about 20 C

# Water at 1 atm: T [C], density [kg/m3], cp [kJ/(kg K)], dynamic viscosity [mPa s]
WATER = [
    (0, 999.8, 4.217, 1.792), (10, 999.7, 4.192, 1.307), (20, 998.2, 4.182, 1.002),
    (30, 995.7, 4.178, 0.798), (40, 992.2, 4.179, 0.653), (50, 988.0, 4.181, 0.547),
    (60, 983.2, 4.185, 0.467), (70, 977.8, 4.190, 0.404), (80, 971.8, 4.197, 0.355),
    (90, 965.3, 4.205, 0.315), (100, 958.4, 4.216, 0.282),
]


def water_props(temp):
    if not 0 <= temp <= 100:
        raise ValueError("water table covers 0-100 C; pass --rho, --cp, --mu-mpas")
    for (t0, r0, c0, m0), (t1, r1, c1, m1) in zip(WATER, WATER[1:]):
        if t0 <= temp <= t1:
            k = (temp - t0) / (t1 - t0)
            return r0 + k * (r1 - r0), c0 + k * (c1 - c0), m0 + k * (m1 - m0)
    raise ValueError("temperature out of range")


def fluid(args):
    """Return (rho, cp, mu_mpas, source). User values override the water table.

    Missing values come from water at --temp, or at 20 C when --temp is not given.
    """
    temp = args.temp if args.temp is not None else 20.0
    w_rho, w_cp, w_mu = water_props(temp)
    user = {k: getattr(args, k) for k in ("rho", "cp", "mu_mpas") if getattr(args, k) is not None}
    rho = user.get("rho", w_rho)
    cp = user.get("cp", w_cp)
    mu = user.get("mu_mpas", w_mu)
    if not user:
        source = f"water at {temp} C (table)"
    else:
        source = "user data: " + ", ".join(user) + f"; other values: water at {temp} C"
    if args.temp is None and len(user) < 3:
        source += " (no --temp given, 20 C assumed)"
    return rho, cp, mu, source


def air_density(temp_c):
    return P_ATM / (R_AIR * (temp_c + 273.15))


def friction_factor(re, rel_rough):
    """Darcy friction factor: laminar 64/Re, else Colebrook-White solved by iteration."""
    if re < 2300:
        return 64.0 / re, "laminar (64/Re)"
    f = 0.02
    for _ in range(50):
        new = (-2.0 * math.log10(rel_rough / 3.7 + 2.51 / (re * math.sqrt(f)))) ** -2
        if abs(new - f) < 1e-10:
            break
        f = new
    regime = "transitional (2300-4000), result uncertain" if re < 4000 else "turbulent"
    return new, f"Colebrook-White, {regime}"


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


def r(x, n=3):
    return round(x, n)


def cmd_water_flow(args):
    rho, cp, _, source = fluid(args)
    m = args.load_kw / (cp * args.dt)  # kg/s
    v = m / rho  # m3/s
    out(args, "Water flow from load",
        {"load": f"{args.load_kw} kW", "dT": f"{args.dt} K", "fluid": source,
         "rho": f"{r(rho, 1)} kg/m3", "cp": f"{r(cp)} kJ/(kg K)"},
        "m = Q / (cp * dT); V = m / rho",
        {"mass flow": f"{r(m, 4)} kg/s", "volume flow": f"{r(v * 3600)} m3/h",
         "volume flow l/s": f"{r(v * 1000)} l/s"})


def cmd_air_flow(args):
    rho = air_density(args.air_temp)
    m = args.load_kw / (CP_AIR * args.dt)
    v = m / rho
    out(args, "Supply airflow from sensible load",
        {"sensible load": f"{args.load_kw} kW", "dT supply-room": f"{args.dt} K",
         "air temp for density": f"{args.air_temp} C", "rho": f"{r(rho)} kg/m3",
         "cp": f"{CP_AIR} kJ/(kg K)"},
        "m = Q / (cp * dT); V = m / rho",
        {"airflow": f"{r(v * 3600, 0)} m3/h", "airflow m3/s": f"{r(v)} m3/s"},
        ["Sensible load only. Check latent load and minimum fresh air separately."])


def cmd_pipe_dp(args):
    rho, _, mu, source = fluid(args)
    d = args.id_mm / 1000
    area = math.pi * d * d / 4
    q = args.flow_m3h / 3600
    v = q / area
    re = rho * v * d / (mu / 1000)
    f, method = friction_factor(re, args.roughness_mm / args.id_mm)
    r_pa_m = f / d * rho * v * v / 2
    friction = r_pa_m * args.length_m
    local = args.zeta * rho * v * v / 2
    total = friction + local
    notes = []
    if v > 2.0:
        notes.append("velocity above 2.0 m/s: check noise and erosion")
    if r_pa_m > 300:
        notes.append("pressure gradient above 300 Pa/m: usually too high for building services")
    out(args, "Pipe pressure drop",
        {"flow": f"{args.flow_m3h} m3/h", "inner diameter": f"{args.id_mm} mm",
         "length": f"{args.length_m} m", "roughness": f"{args.roughness_mm} mm",
         "sum of local loss coefficients": args.zeta, "fluid": source,
         "rho": f"{r(rho, 1)} kg/m3", "mu": f"{r(mu, 4)} mPa s"},
        "dp = (f * L / D + sum zeta) * rho * v^2 / 2; f from " + method,
        {"velocity": f"{r(v)} m/s", "Reynolds": f"{r(re, 0)}", "friction factor": r(f, 5),
         "gradient R": f"{r(r_pa_m, 1)} Pa/m", "friction dp": f"{r(friction / 1000)} kPa",
         "local dp": f"{r(local / 1000)} kPa", "total dp": f"{r(total / 1000)} kPa",
         "total head": f"{r(total / (rho * G))} m"}, notes)


def cmd_duct_dp(args):
    rho = air_density(args.air_temp)
    q = args.flow_m3h / 3600
    if args.d_mm:
        d_eq = args.d_mm / 1000
        area = math.pi * d_eq * d_eq / 4
        shape = f"round D={args.d_mm} mm"
    else:
        a, b = args.a_mm / 1000, args.b_mm / 1000
        area = a * b
        d_eq = 1.30 * (a * b) ** 0.625 / (a + b) ** 0.25  # Huebscher, equal friction
        shape = f"rectangular {args.a_mm}x{args.b_mm} mm"
    v = q / area
    # Friction uses the equivalent round duct carrying the same airflow.
    v_eq = q / (math.pi * d_eq * d_eq / 4)
    re = rho * v_eq * d_eq / MU_AIR
    f, method = friction_factor(re, args.roughness_mm / 1000 / d_eq)
    r_pa_m = f / d_eq * rho * v_eq * v_eq / 2
    friction = r_pa_m * args.length_m
    local = args.zeta * rho * v * v / 2
    out(args, "Duct pressure drop",
        {"airflow": f"{args.flow_m3h} m3/h", "duct": shape, "length": f"{args.length_m} m",
         "roughness": f"{args.roughness_mm} mm", "sum of local loss coefficients": args.zeta,
         "rho": f"{r(rho)} kg/m3"},
        "dp = f * L / De * rho * v_eq^2 / 2 + sum zeta * rho * v^2 / 2; De (Huebscher) = "
        "1.30 (ab)^0.625 / (a+b)^0.25; f from " + method,
        {"velocity in duct": f"{r(v, 2)} m/s", "equivalent diameter": f"{r(d_eq * 1000, 0)} mm",
         "gradient R": f"{r(r_pa_m, 2)} Pa/m", "friction dp": f"{r(friction, 1)} Pa",
         "local dp": f"{r(local, 1)} Pa", "total dp": f"{r(friction + local, 1)} Pa"})


def cmd_pump_power(args):
    rho, _, _, source = fluid(args)
    q = args.flow_m3h / 3600
    if args.head_m is not None:
        head = args.head_m
        dp = head * rho * G
    else:
        dp = args.dp_kpa * 1000
        head = dp / (rho * G)
    p_hyd = q * dp
    p_shaft = p_hyd / args.eff
    out(args, "Pump power",
        {"flow": f"{args.flow_m3h} m3/h", "fluid": source, "rho": f"{r(rho, 1)} kg/m3",
         "pump efficiency (assumed unless from data sheet)": args.eff},
        "H = dp / (rho * g); P_hyd = V * dp; P_shaft = P_hyd / eta",
        {"head": f"{r(head)} m", "differential pressure": f"{r(dp / 1000)} kPa",
         "hydraulic power": f"{r(p_hyd / 1000)} kW", "shaft power": f"{r(p_shaft / 1000)} kW"},
        ["Use the efficiency at the duty point from the manufacturer curve when known."])


def cmd_fan_power(args):
    q = args.flow_m3h / 3600
    p_shaft = q * args.dp_pa / args.eff
    out(args, "Fan power and SFP",
        {"airflow": f"{args.flow_m3h} m3/h", "total pressure": f"{args.dp_pa} Pa",
         "overall efficiency (assumed unless from data sheet)": args.eff},
        "P = V * dp / eta; SFP = P / V",
        {"power": f"{r(p_shaft / 1000)} kW", "SFP": f"{r(p_shaft / 1000 / q)} kW/(m3/s)"},
        ["SFP here is for one fan. Add supply and extract for the unit SFP.",
         "Ecodesign SFPint (Regulation 1253/2014) is a different, internal value. Use the "
         "manufacturer's declared SFPint for compliance."])


def cmd_margin(args):
    out(args, "Margin",
        {"value": args.value, "margin": f"{args.percent} %"},
        "value * (1 + margin / 100)",
        {"result": r(args.value * (1 + args.percent / 100), 4)})


def positive(x):
    v = float(x)
    if v <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return v


def build_parser():
    p = argparse.ArgumentParser(description="HVAC sizing calculations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
        s.set_defaults(func=func)
        return s

    def fluid_args(s):
        s.add_argument("--temp", type=float, default=None, help="water temperature C")
        s.add_argument("--rho", type=positive)
        s.add_argument("--cp", type=positive)
        s.add_argument("--mu-mpas", type=positive)

    s = add("water-flow", cmd_water_flow)
    s.add_argument("--load-kw", type=positive, required=True)
    s.add_argument("--dt", type=positive, required=True)
    fluid_args(s)

    s = add("air-flow", cmd_air_flow)
    s.add_argument("--load-kw", type=positive, required=True)
    s.add_argument("--dt", type=positive, required=True)
    s.add_argument("--air-temp", type=float, default=20.0)

    s = add("pipe-dp", cmd_pipe_dp)
    s.add_argument("--flow-m3h", type=positive, required=True)
    s.add_argument("--id-mm", type=positive, required=True)
    s.add_argument("--length-m", type=float, required=True)
    s.add_argument("--roughness-mm", type=float, default=0.045)
    s.add_argument("--zeta", type=float, default=0.0)
    fluid_args(s)

    s = add("duct-dp", cmd_duct_dp)
    s.add_argument("--flow-m3h", type=positive, required=True)
    s.add_argument("--d-mm", type=positive)
    s.add_argument("--a-mm", type=positive)
    s.add_argument("--b-mm", type=positive)
    s.add_argument("--length-m", type=float, required=True)
    s.add_argument("--roughness-mm", type=float, default=0.15)
    s.add_argument("--zeta", type=float, default=0.0)
    s.add_argument("--air-temp", type=float, default=20.0)

    s = add("pump-power", cmd_pump_power)
    s.add_argument("--flow-m3h", type=positive, required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--head-m", type=positive)
    g.add_argument("--dp-kpa", type=positive)
    s.add_argument("--eff", type=positive, default=0.55)
    fluid_args(s)

    s = add("fan-power", cmd_fan_power)
    s.add_argument("--flow-m3h", type=positive, required=True)
    s.add_argument("--dp-pa", type=positive, required=True)
    s.add_argument("--eff", type=positive, default=0.65)

    s = add("margin", cmd_margin)
    s.add_argument("--value", type=float, required=True)
    s.add_argument("--percent", type=float, required=True)
    return p


def main():
    args = build_parser().parse_args()
    if args.cmd == "duct-dp" and not (args.d_mm or (args.a_mm and args.b_mm)):
        print("ERROR: give --d-mm, or both --a-mm and --b-mm", file=sys.stderr)
        return 2
    if getattr(args, "eff", 1) > 1:
        print("ERROR: --eff is a fraction, for example 0.6", file=sys.stderr)
        return 2
    try:
        args.func(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
