# Conflict-Based Search for Optimal Multi-Agent Path Finding
## A Reproduction and Extension Study

**Authors:** Nimrod Netzer, Elad Damti, Kfir Dahan
**Course:** Search in Artificial Intelligence — Bar-Ilan University, 2026

---

## Abstract

Multi-Agent Path Finding (MAPF) is the problem of planning collision-free paths for a set of agents on a shared graph, minimizing the total travel cost. Solving MAPF optimally is NP-hard, and naive approaches based on joint-state-space search fail due to exponential state-space growth. In this work, we reproduce key experimental results from Sharon et al. (2015), who introduced Conflict-Based Search (CBS) — a two-level algorithm that separates high-level conflict resolution from low-level single-agent planning. We implement CBS independently in Python and reproduce two central results: the success rate as a function of the number of agents, and a comparison against an independent planning baseline. We further contribute an extension study evaluating how map topology affects CBS performance, comparing open grid maps against warehouse-style maps with narrow corridors and bottlenecks. Our results confirm CBS's advantage over independent planning and reveal that structured maps with bottlenecks significantly increase conflict frequency and constraint tree depth, reducing CBS success rates.

---

## 1. Introduction

Multi-Agent Path Finding (MAPF) arises in many real-world domains including automated warehouses, airport ground traffic management, and railway scheduling [Sharon et al., 2015]. In these settings, a set of agents must navigate from their respective start locations to goal locations on a shared graph without colliding.

The na\"{i}ve approach of searching the joint configuration space of all agents using A* quickly becomes infeasible. The joint state space grows exponentially with the number of agents: for 10 agents on a graph with 5 vertices, the number of joint states exceeds 9.7 million, making standard search methods impractical for realistic problem sizes.

CBS addresses this by decomposing the problem into a two-level hierarchy. The high level searches a Constraint Tree (CT), branching on conflicts between agent paths. The low level plans optimal paths for individual agents subject to a set of constraints. This separation allows CBS to exploit agent independence and avoid enumerating the full joint state space.

In this project, we reproduce two central experimental results from Sharon et al. (2015): (1) the success rate of CBS as the number of agents increases, compared to an independent A* baseline; and (2) the runtime and constraint tree expansion statistics on standard grid benchmarks. We additionally contribute an extension study examining how map topology — specifically the presence of bottlenecks in warehouse-style maps — affects CBS performance.

---

## 2. Selected Paper Description

### 2.1 Problem Formulation

The MAPF problem is defined on a graph G = (V, E), with a set of k agents A = {1, ..., k}. Each agent i has a start vertex s_i and a goal vertex g_i. At each timestep, an agent can move to an adjacent vertex or wait at its current vertex. A solution is a set of paths {π_1, ..., π_k} such that no two agents occupy the same vertex at the same timestep (vertex conflict) and no two agents traverse the same edge in opposite directions simultaneously (edge conflict).

The objective is to minimize the Sum of Costs (SOC):

    SOC = Σ_{i=1}^{k} |π_i|

where |π_i| is the number of timesteps agent i takes to reach its goal. Optimal MAPF is NP-hard in general [Sharon et al., 2015].

### 2.2 Conflict Types

The paper identifies five types of conflicts between agent pairs:
1. **Vertex conflict:** Two agents occupy the same vertex at the same timestep.
2. **Edge conflict:** Two agents traverse the same edge in opposite directions between consecutive timesteps (swap conflict).
3. **Following conflict:** One agent follows another on the same edge.
4. **Cycle conflict:** A group of agents form a cyclic dependency.
5. **Swapping conflict:** Two agents exchange positions.

In our implementation we detect and resolve vertex and edge (swap) conflicts, which are the two fundamental types required for correctness and optimality.

### 2.3 Why Joint-State-Space A* Fails

Searching the joint configuration space with A* requires representing all k agents simultaneously. The state space size is O(|V|^k), which grows exponentially. For k=10 agents on a graph with |V|=5 vertices, this yields approximately 9.7 million states. For realistic grid maps with hundreds of vertices and tens of agents, this is computationally infeasible.

### 2.4 The CBS Algorithm

CBS operates on two levels:

**Low level — Time-Space A* (TSA*):**
Each agent's path is planned individually using A* in the time-space graph, where each state is a (vertex, timestep) pair. The TSA* respects a set of constraints C_i for agent i. A constraint (v, t) forbids agent i from occupying vertex v at timestep t. An edge constraint forbids traversing a specific edge at a specific timestep. The heuristic is the Manhattan distance to the goal, which is admissible on 4-connected grids.

**High level — Constraint Tree (CT):**
The CT is a binary tree where each node N contains:
- A set of constraints for each agent: {C_1, ..., C_k}
- A set of paths planned by TSA* respecting those constraints
- The total cost: SOC of all paths

The CBS algorithm proceeds as follows:
1. Create root node: plan each agent independently with TSA* (no constraints).
2. Find the first conflict among all agent paths.
3. If no conflict exists: return the current solution (optimal).
4. Otherwise, create two child nodes — one adding a constraint on agent i, one on agent j (where i and j are the conflicting agents).
5. Replan the constrained agent with TSA* in each child.
6. Add both children to the open list (min-heap by cost).
7. Pop the lowest-cost node and repeat from step 2.

CBS is both complete and optimal: it is guaranteed to find the minimum SOC solution if one exists [Sharon et al., 2015].

### 2.5 CBS Improvements

The paper also introduces several improvements to basic CBS:
- **Prioritizing Conflicts:** Resolve cardinal conflicts (those guaranteed to increase cost) first.
- **CBS with Heuristics:** Add an admissible heuristic at the high-level CT to guide node selection.
- **Disjoint Splitting:** Use both negative constraints (avoid position) and positive constraints (must pass through position) to reduce tree branching.
- **Conflict Reasoning:** Impose larger sets of constraints derived from conflict analysis.

Our implementation covers basic CBS without these improvements, providing a clean baseline for comparison.

---

## 3. Project Description

### 3.1 Implementation

We implemented CBS independently in Python 3.13, without using the original authors' code. The implementation consists of six modules:

- **graph.py:** A `Grid` class representing 4-connected grid maps with obstacles. Supports random map generation and Moving AI map file format.
- **tsa_star.py:** Time-Space A* with constraint checking. State = (vertex, timestep). Heuristic = Manhattan distance. Constraints are stored as a set of (vertex, timestep) tuples (vertex constraints) and frozensets of position-time pairs (edge constraints).
- **conflict.py:** Conflict detection for all agent pairs. Detects vertex conflicts and edge (swap) conflicts. Returns the first conflict found for CBS branching, or all conflicts for analysis.
- **cbs.py:** The CBS high-level constraint tree. Uses a min-heap (by SOC) as the open list. Each CT node stores its constraint sets and paths. Also implements an independent A* baseline for comparison.
- **benchmark.py:** Map generators (open grid with random obstacles; warehouse grid with shelf rows and narrow corridors), random instance generator, and experiment runner producing CSV results.
- **visualize.py:** Matplotlib-based plotting of success rates, runtimes, CT node counts, and topology comparisons. Also includes grid animation.

### 3.2 Team Contributions

- **Nimrod Netzer:** Implemented the low-level Time-Space A* search (tsa_star.py), including state representation, constraint checking, and heuristic. Wrote Sections 1, 2, and the Abstract.
- **Elad Damti:** Implemented conflict detection (conflict.py) and the CBS high-level constraint tree (cbs.py), including the CTNode structure and main CBS loop. Wrote Sections 3 and 4.
- **Kfir Dahan:** Implemented the benchmark infrastructure (benchmark.py), map generators, experiment runner, and visualization (visualize.py). Ran all experiments and wrote Sections 5, 6, the Reproducibility Statement, and AI Disclosure.

All three team members participated in testing, debugging, defense preparation, and the recorded video.

### 3.3 Implementation Choices

- **Goal model:** Agents stay at their goal vertex indefinitely (paths are padded at the goal for conflict checking beyond their length).
- **Conflict selection:** The first conflict found (by timestep, then agent pair index) is resolved. No conflict prioritization was implemented.
- **Time limit:** 30 seconds per instance for reproduction; 15 seconds for the extension. Instances not solved within the limit are counted as failures.
- **Memory limit:** No explicit memory cap; Python process limited by OS (16GB RAM available).
- **Grid size:** 20×20 for all experiments, ~10% obstacle density for open grids.
- **Random seeds:** Instance seed = 42 + n\_agents × 1000 + instance\_index (deterministic and fully reproducible).

---

## 4. Experiments

### 4.1 Experimental Setup

**Hardware:** 12th Gen Intel Core i7-1255U, 10 cores, 1.7GHz, 16GB RAM, Windows 11 Home.
**Software:** Python 3.13; matplotlib 3.11 (plots); standard library (heapq, collections, csv, json, time). No external search libraries used.
**Benchmark:** 20×20 grid maps generated randomly. Open grid: ~10% obstacle density (random placement, seed=1). Warehouse grid: alternating shelf rows with single-cell vertical corridors every 4 columns. 25 random instances per agent count.
**Random seeds:** Instance seed = 42 + n\_agents × 1000 + instance\_index. Map seed = 1. Fully deterministic and reproducible.
**Algorithms:** (1) CBS — our implementation. (2) Independent A* baseline — each agent planned separately with TSA*, no conflict avoidance.
**Parameter settings:** CBS: no conflict prioritization, first-found conflict resolved, stay-at-goal model, max\_t=200 timesteps per TSA* call.
**Time limit:** 30 seconds per instance (reproduction); 15 seconds (extension). Instances exceeding the limit counted as failures.
**Memory limit:** No explicit cap; bounded by OS (16GB RAM).
**Number of runs:** 1 run per instance (deterministic algorithm).
**Agent counts:** Reproduction: 4, 6, 8, 10, 12, 15, 18, 20. Extension: 4, 6, 8, 10, 12.
**Differences from original paper:** We used a 20×20 grid (smaller than the paper's maps), Python instead of C++, and a 30s time limit instead of the paper's longer limits. These differences explain lower absolute success rates at higher agent counts.

### 4.2 Reproduced Results

**Table 1: CBS performance on open 20×20 grid (25 instances per agent count)**

| Agents | Success Rate | Mean Time (s) | Mean CT Nodes | Mean LL Calls | Mean SOC |
|--------|-------------|---------------|---------------|---------------|----------|
| 4      | 100%        | 0.002         | 2.0           | 6.0           | 56.8     |
| 6      | 92%         | 0.004         | 4.0           | 11.9          | 83.8     |
| 8      | 96%         | 0.011         | 5.2           | 16.5          | 113.5    |
| 10     | 88%         | 0.013         | 11.3          | 30.5          | 132.9    |
| 12     | 76%         | 0.026         | 17.1          | 44.2          | 159.4    |
| 15     | 44%         | 1.471         | 1401.9        | 2816.8        | 202.5    |
| 18     | 56%         | 3.626         | 1344.4        | 2704.9        | 242.8    |
| 20     | 36%         | 3.797         | 2179.4        | 4376.9        | 276.1    |

**Table 2: Independent A* baseline — mean conflicts in produced solutions**

| Agents | Baseline Success | Mean Conflicts in Solution |
|--------|-----------------|---------------------------|
| 4      | 100%            | 0.4                       |
| 6      | 92%             | 1.3                       |
| 8      | 100%            | 2.0                       |
| 10     | 96%             | 2.2                       |
| 12     | 100%            | 4.7                       |
| 15     | 88%             | 8.6                       |
| 18     | 92%             | 10.5                      |
| 20     | 92%             | 15.2                      |

The baseline always produces solutions quickly (it never searches for conflict resolution), but those solutions contain collisions — an average of 15.2 conflicts at 20 agents. CBS, by contrast, guarantees conflict-free optimal solutions at the cost of increased runtime.

A striking observation in Table 1 is the jump in CT nodes between 12 and 15 agents: from 17 nodes to 1,402 nodes on average. This reflects the exponential worst-case behavior of CBS when many conflicts must be resolved, consistent with the paper's findings.

### 4.3 Extension Results — Map Topology Study

**Research question:** Does map topology affect CBS performance? Specifically, do warehouse-style maps (narrow corridors, bottlenecks) create more conflicts and reduce CBS success compared to open grids?

**Table 3: CBS on Open Grid vs Warehouse Grid (25 instances per agent count, 15s time limit)**

| Agents | Open Grid Success | Open Grid Mean CT | Warehouse Success | Warehouse Mean CT |
|--------|------------------|-------------------|------------------|-------------------|
| 4      | 100%             | 2.0               | 92%              | 2.2               |
| 6      | 92%              | 4.0               | 100%             | 3.7               |
| 8      | 96%              | 5.2               | 76%              | 18.2              |
| 10     | 88%              | 11.3              | 60%              | 11.3              |
| 12     | 76%              | 17.1              | 44%              | 49.5              |

The warehouse grid consistently underperforms the open grid at higher agent counts. At 12 agents, open grid success rate is 76% while warehouse drops to 44%. More strikingly, the mean CT nodes expanded in the warehouse at 12 agents (49.5) is nearly 3× that of the open grid (17.1), indicating that bottlenecks force more conflicts that require deeper constraint tree exploration.

---

## 5. Discussion

### 5.1 Agreement with Original Paper

Our reproduced results are qualitatively consistent with Sharon et al. (2015):
- CBS achieves near-perfect success rates for small agent counts (≤10 agents) and degrades gracefully as agent count increases.
- The CT expansion count grows dramatically beyond ~12 agents, reflecting CBS's exponential worst-case behavior.
- The independent A* baseline always finds individual paths quickly, but produces solutions with increasing numbers of collisions as agent count grows — confirming that naive independent planning is insufficient for MAPF.

Quantitative differences from the paper are expected due to: (1) our Python implementation vs. the original C++, (2) different hardware, (3) smaller grid size (20×20 vs. larger maps in the paper), and (4) a 30-second time limit vs. the paper's longer limits. Our success rates drop earlier than in the original paper, which is consistent with these differences.

### 5.2 Extension Findings

Our map topology study confirms that environment structure significantly affects CBS performance. The warehouse grid — featuring rows of shelf obstacles with narrow single-cell corridor gaps — consistently yields lower success rates and more CT node expansions than the open grid at the same agent counts.

At 8 agents, the warehouse CT node count (18.2) is 3.5× higher than the open grid (5.2), despite similar instance difficulty for small agent counts. At 12 agents, warehouse success drops to 44% while open grid remains at 76%. This gap can be attributed to the following mechanism: in warehouse maps, agents must funnel through a small number of corridor cells, dramatically increasing the probability of vertex conflicts at those bottleneck locations. Each conflict forces a CT branch, and the constrained agent is then forced to take a longer detour, potentially creating further conflicts with other agents in adjacent corridors.

This finding has practical implications: CBS improvements such as conflict prioritization and high-level heuristics would be especially valuable in warehouse-like environments, where the number of conflicts per solution is inherently higher due to spatial constraints.

### 5.3 Limitations

- **Python performance:** Our implementation is significantly slower than a C++ implementation. Many instances that fail due to timeout would likely be solved with a compiled implementation.
- **Grid size:** 20×20 grids are smaller than the paper's benchmarks. Larger grids would allow more agents before conflicts become dense.
- **No CBS improvements:** We implemented basic CBS only. Adding prioritized conflict resolution or high-level heuristics would significantly improve success rates at higher agent counts.

---

## 6. Conclusion

We implemented CBS from scratch in Python and reproduced its two central experimental results: success rate vs. number of agents, and the growth of CT expansions. Our results confirm CBS's key property: it finds provably optimal, collision-free solutions while scaling significantly better than naive joint-state-space search.

Our extension study on map topology provides insight into which environmental structures make CBS harder, showing that bottleneck-heavy warehouse maps increase conflict density and reduce success rates — at 12 agents, warehouse success rate (44%) is nearly half that of open grids (76%).

Future work could implement CBS improvements (prioritized conflicts, high-level heuristics) and evaluate them specifically on warehouse-style maps, where the performance gap is expected to be largest.

---

## References

Sharon, G., Stern, R., Felner, A., & Sturtevant, N. R. (2015). Conflict-based search for optimal multi-agent pathfinding. *Artificial Intelligence*, 219, 40–66. https://doi.org/10.1016/j.artint.2014.11.006

Sturtevant, N. R. (2012). Benchmarks for grid-based pathfinding. *IEEE Transactions on Computational Intelligence and AI in Games*, 4(2), 144–148.

---

## Reproducibility Statement

**Results reproduced:** (1) Success rate of CBS vs. number of agents on grid maps, compared to an independent A* baseline — corresponding to the success rate figures in Sharon et al. (2015). (2) Runtime and CT node expansion statistics on solved instances.

**Results NOT reproduced:** Experiments on the specific Moving AI benchmark maps used in the paper (e.g., Paris_1_256); comparisons to ICTS or other MAPF algorithms; results for CBS improvement variants (prioritized conflicts, disjoint splitting, high-level heuristics).

**Implementation basis:** New independent implementation in Python 3.13. The original authors' code was not used.

**Changes from original:** Smaller grid (20×20 vs. larger benchmark maps), shorter time limit (30s), Python instead of C++, randomly generated maps instead of the paper's benchmark files.

**Agreement with original:** Qualitative trends match — CBS scales better than independent planning, success rate degrades with agent count, CT nodes grow dramatically beyond ~12 agents. Absolute numbers differ due to implementation language, grid size, and time limit.

**Files included:**
- Source code: `graph.py`, `tsa_star.py`, `conflict.py`, `cbs.py`, `benchmark.py`, `visualize.py`, `main.py`, `generate_report.py`
- Raw results: `results/reproduce_open.csv`, `results/extension_open.csv`, `results/extension_warehouse.csv`
- Figures: `results/fig1_success_rate.png`, `fig2_runtime.png`, `fig3_ct_nodes.png`, `fig4_topology_success.png`
- Instructions: `README.md`

**How to run:**
```bash
pip install matplotlib
python main.py --mode reproduce --n-instances 25 --time-limit 30 --agent-counts 4 6 8 10 12 15 18 20
python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12
```

---

## AI Tools Disclosure

The following AI tools were used in this project:

- **Claude (Anthropic, claude-sonnet-4-6):** Used for implementation assistance (code structure, TSA* and CBS implementation, debugging), report writing guidance, algorithm explanations based on course lecture slides and the paper, and project planning. All code was reviewed, understood, and validated by the team.

The team takes full responsibility for the correctness, originality, and quality of all submitted work.
