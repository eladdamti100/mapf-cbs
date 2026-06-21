# CBS MAPF — Implementation & Experiments

Implementation of **Conflict-Based Search (CBS)** for optimal Multi-Agent Path Finding.

Based on: Sharon, G., Stern, R., Felner, A., & Sturtevant, N. R. (2015).
*Conflict-Based Search for Optimal Multi-Agent Pathfinding.*
Artificial Intelligence, 219, 40–66.

Team: Nimrod Netzer, Elad Damti, Kfir Dahan — Bar-Ilan University, Search in AI, 2026.

---

## Requirements

- Python 3.8+
- matplotlib (for plots and animation)

Install dependencies:
```bash
pip install matplotlib
```

---

## Project Structure

```
mapf_cbs/
├── graph.py        # Grid representation
├── tsa_star.py     # Time-Space A* (low-level CBS search)
├── conflict.py     # Conflict detection (vertex + edge)
├── cbs.py          # CBS high-level constraint tree
├── joint_astar.py  # Joint-State-Space A* baseline (true paper baseline)
├── benchmark.py    # Map generators, instance generator, experiment runner
├── main.py         # CLI entry point
├── visualize.py    # Plots and animation
├── maps/           # Generated map files
├── instances/      # Generated instance files
└── results/        # Output CSV files and figures
```

---

## How to Run

All commands are run from inside the `mapf_cbs/` directory.

### 1. Demo — solve a small 3-agent instance and visualize

```bash
python main.py --mode demo
```

### 2. Solve a single random instance

```bash
python main.py --mode solve --agents 8 --width 15 --height 15
```

Options:
- `--agents N`       : number of agents (default: 5)
- `--width W`        : grid width (default: 20)
- `--height H`       : grid height (default: 20)
- `--time-limit T`   : time limit in seconds (default: 60)
- `--seed S`         : random seed (default: 42)

### 3. Reproduce paper results (Result 1 + Result 2)

Runs CBS and the Joint-State-Space A* baseline (the paper's intended baseline,
not an independent-planning baseline) on a 20×20 open grid for multiple agent
counts. Generates success rate, runtime, and CT-node plots.

```bash
python main.py --mode reproduce --n-instances 25 --time-limit 30 --baseline-time-limit 5 --agent-counts 4 6 8 10 12 15 18 20
```

Options:
- `--n-instances N`            : instances per agent count (default: 25)
- `--agent-counts 4 6 8 10 12 15 18 20` : agent counts to test
- `--obstacle-pct 0.1`         : fraction of grid cells that are obstacles
- `--time-limit T`             : CBS time limit in seconds (default: 60; paper reproduction uses 30)
- `--baseline-time-limit T`    : Joint A* baseline time limit in seconds (default: same as `--time-limit`; paper reproduction uses 5 since Joint A*'s state space blows up combinatorially)

Output files:
- `results/reproduce_open.csv`
- `results/fig1_success_rate.png`
- `results/fig2_runtime.png`
- `results/fig3_ct_nodes.png`

### 4. Run extension — map topology study

Compares CBS on open grid vs warehouse-style grid (CBS only, no baseline).

```bash
python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12 15 18 20
```

Output files:
- `results/extension_open.csv`
- `results/extension_warehouse.csv`
- `results/fig4_topology_success.png`

---

## Reproducing All Experiments (Full Pipeline)

Run these commands in order:

```bash
cd mapf_cbs
python main.py --mode demo
python main.py --mode reproduce --n-instances 25 --time-limit 30 --baseline-time-limit 5 --agent-counts 4 6 8 10 12 15 18 20
python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12 15 18 20
```

All results will be in the `results/` directory.

---

## Algorithm Overview

**CBS operates in two levels:**

**High level — Constraint Tree (CT):**
- Root: each agent plans independently with TSA*
- Find first conflict (vertex or edge) among all paths
- If no conflict: return solution
- Otherwise: create two child CT nodes, each adding one constraint (one per conflicting agent)
- Search CT with best-first (min sum-of-costs)

**Low level — Time-Space A* (TSA*):**
- State: (vertex, timestep)
- Heuristic: Manhattan distance (admissible)
- Skips states blocked by agent's constraint set
- Returns shortest path for one agent respecting its constraints

**Conflict types detected:**
- Vertex conflict: two agents at same vertex at same timestep
- Edge conflict: two agents swap positions between consecutive timesteps

**Baseline — Joint-State-Space A\*:**
- Searches the full joint configuration space of all agents simultaneously (`joint_astar.py`)
- This is the paper's intended baseline, not an independent-per-agent planner — it always produces conflict-free paths but suffers from exponential state-space blowup
- In our experiments it fails completely (0% success) from 8 agents onward within its 5s time limit

---

## Reproducibility Statement

- Results reproduced: (1) success rate of CBS vs. the Joint-State-Space A* baseline as a function of agent count (Figure 1); (2) CT node expansion and runtime growth (Figures 2-3)
- Implementation: written independently in Python 3.13; not based on the authors' original code
- Differences from original: Python vs C++, smaller 20×20 grid instead of Moving AI benchmark maps, shorter time limits (30s CBS / 5s Joint A* for reproduction, 15s for the extension)
- Agreement: qualitative trends match (CBS scales far better than joint search, success rate degrades with agent count, CT nodes grow exponentially); absolute numbers differ due to hardware, grid size, and time limits
- Raw results: `results/reproduce_open.csv`, `results/extension_open.csv`, `results/extension_warehouse.csv`

---

## AI Tools Disclosure

Claude (Anthropic): used as a technical assistant for code optimization, syntax debugging, and editorial review of the documentation. All core algorithms (including TSA* and CBS) were conceptualized and implemented directly by the team. The team has thoroughly validated all project components and takes full responsibility for the integrity, originality, and performance of the final output.
