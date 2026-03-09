# Controller-Search Project

## Project Overview
This project explores **evolutionary search for feedback controllers** using LLMs (via OpenEvolve / AlphaEvolve).
The baseline is a hand-tuned PID controller; the goal is to evolve program-level controller code that performs as well or better.

## Repository Structure
- [feedback_controller.py](feedback_controller.py) — PID controller + first-order plant simulator. Entry point: `simulate()`.
- [plot_pid.py](plot_pid.py) — Generates `pid_diagram.png`, a block diagram of the PID feedback loop using matplotlib.
- [pid_diagram.png](pid_diagram.png) — Rendered block diagram (Setpoint → Summing junction → PID → Plant → Output, with sensor feedback path).
- [evolve_controller.ipynb](evolve_controller.ipynb) — Notebook scaffolding for OpenEvolve integration (in progress; currently has intro markdown only).

## PID Baseline
- Plant: first-order system `dy/dt = -a*y + b*u`, with `a=2.0`, `b=3.0`
- Gains: `Kp=3.0`, `Ki=2.0`, `Kd=0.1`, `dt=0.01`
- Actuator saturation: `[-10, 10]`
- Default setpoint: `1.0`, duration: `10.0 s`
- Achieves near-zero steady-state error

## Planned Work
- Use [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve) (open-source AlphaEvolve) to mutate controller code inside `# EVOLVE-BLOCK-START / END` markers
- Evaluator scores candidates on how well they drive the simulated plant to a setpoint
- Notebook `evolve_controller.ipynb` is the intended integration point

## Environment
- Cluster: Boston University SCC (`/projectnb/depaqlab/`)
- Python 3 available via `python3`
- Git repo initialized; single commit so far (`0abc222`)

## Session History
- **Session 1 (initial):** Created baseline PID simulation (`feedback_controller.py`), block diagram generator (`plot_pid.py`), and notebook scaffold (`evolve_controller.ipynb`). Committed as "Initial commit: PID feedback controller simulation and block diagram".
