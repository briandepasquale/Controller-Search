"""
Evaluator for evolved controller candidates.

OpenEvolve imports this module and calls evaluate(program_path).
Returns a dict of metrics; higher values are better.

Scoring:
  compile_ok  : 1.0 if the program runs, 0.0 on any exception
  score       : composite metric in [0, 1] (higher = better)
                combines ISE, overshoot, and steady-state error
  ise         : integral squared error (lower is better, stored for reference)
  overshoot   : fractional overshoot above setpoint (lower is better)
  ss_error    : |y_final - setpoint| (lower is better)
"""

import importlib.util


# ── Plant / simulation parameters (fixed) ─────────────────────────────────────
SETPOINTS = [1.0, 0.5, 2.0]   # evaluate across multiple setpoints
DURATION  = 10.0
DT        = 0.01
A, B      = 2.0, 3.0           # dy/dt = -A*y + B*u
U_MAX     = 10.0
U_MIN     = -10.0


def _simulate(controller_class, setpoint: float) -> dict:
    """Run one simulation and return performance metrics."""
    ctrl  = controller_class(DT)
    y     = 0.0
    ise   = 0.0
    peak_y = 0.0

    for _ in range(int(DURATION / DT)):
        u = ctrl.compute(setpoint, y)
        u = max(U_MIN, min(U_MAX, u))
        y += (-A * y + B * u) * DT

        ise += (setpoint - y) ** 2 * DT
        if y > peak_y:
            peak_y = y

    ss_error  = abs(setpoint - y)
    overshoot = max(0.0, (peak_y - setpoint) / abs(setpoint)) if setpoint != 0 else 0.0

    return {"ise": ise, "ss_error": ss_error, "overshoot": overshoot}


def evaluate(program_path: str) -> dict:
    """Load a candidate program and score it across all test setpoints."""
    try:
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        Controller = mod.Controller
    except Exception:
        return {"compile_ok": 0.0, "score": 0.0, "ise": 1e9,
                "overshoot": 1.0, "ss_error": 1.0}

    try:
        results = [_simulate(Controller, sp) for sp in SETPOINTS]
    except Exception:
        return {"compile_ok": 1.0, "score": 0.0, "ise": 1e9,
                "overshoot": 1.0, "ss_error": 1.0}

    avg_ise       = sum(r["ise"]       for r in results) / len(results)
    avg_overshoot = sum(r["overshoot"] for r in results) / len(results)
    avg_ss_error  = sum(r["ss_error"]  for r in results) / len(results)

    score_ise = 1.0 / (1.0 + avg_ise)
    score_os  = 1.0 / (1.0 + 5.0  * avg_overshoot)
    score_ss  = 1.0 / (1.0 + 20.0 * avg_ss_error)
    score     = 0.5 * score_ise + 0.3 * score_os + 0.2 * score_ss

    return {
        "compile_ok": 1.0,
        "score":      round(score, 6),
        "ise":        round(avg_ise, 6),
        "overshoot":  round(avg_overshoot, 6),
        "ss_error":   round(avg_ss_error, 6),
    }
