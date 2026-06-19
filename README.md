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

Runs CBS and independent A* baseline on 20×20 open grid for multiple agent counts.
Generates success rate and runtime plots.

```bash
python main.py --mode reproduce --n-instances 25 --time-limit 60
```

Options:
- `--n-instances N`       : instances per agent count (default: 25)
- `--agent-counts 4 6 8 10 12 15 18 20 25 30` : agent counts to test
- `--obstacle-pct 0.1`    : fraction of grid cells that are obstacles

Output files:
- `results/reproduce_open.csv`
- `results/fig1_success_rate.png`
- `results/fig2_runtime.png`
- `results/fig3_ct_nodes.png`

### 4. Run extension — map topology study

Compares CBS on open grid vs warehouse-style grid.

```bash
python main.py --mode extension --n-instances 25 --time-limit 60
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
python main.py --mode reproduce --n-instances 25 --time-limit 60 --agent-counts 4 6 8 10 12 15 18 20 25 30
python main.py --mode extension --n-instances 25 --time-limit 60 --agent-counts 4 6 8 10 12 15 18 20
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

---

## Reproducibility Statement

- Results reproduced: success rate vs agents (Figure 1), runtime comparison (Figure 2)
- Implementation: written independently in Python 3; not based on authors' original code
- Differences from original: Python vs C++, smaller grid sizes, potentially different random seeds
- Agreement: qualitative trends match (CBS scales better than joint A*); absolute numbers differ due to hardware and language
- Raw results: `results/reproduce_open.csv`, `results/extension_open.csv`, `results/extension_warehouse.csv`

---

## AI Tools Disclosure

The following AI tools were used during this project:

- **Claude (Anthropic)**: assisted with code structure, implementation of TSA* and CBS, debugging, report writing guidance, and explaining algorithm concepts from the paper
- All code was reviewed, understood, and validated by the team
- The team takes full responsibility for the correctness, originality, and quality of the submission
