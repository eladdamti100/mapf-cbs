# Presentation Creation Prompt for Gemini

Please create a professional academic presentation (PowerPoint / Google Slides) with exactly 12 slides based on the content below.

**Style instructions:**
- Clean academic style, white or dark navy background
- Times New Roman or similar serif font for body text
- Each slide has a clear title and bullet points (no walls of text)
- Use diagrams/visuals where indicated
- Font size: titles 28-32pt, bullets 18-22pt
- Color accent: blue (#1a4f8a) for highlights

---

## SLIDE 1 - Title Slide

**Title:** Conflict-Based Search for Optimal Multi-Agent Path Finding

**Subtitle:** A Reproduction and Extension Study

**Bottom line:**
- Nimrod Netzer | Elad Damti | Kfir Dahan
- Search in Artificial Intelligence - Bar-Ilan University, 2026
- Based on: Sharon, Stern, Felner & Sturtevant (2015), Artificial Intelligence Journal

**Visual:** Simple robot/warehouse icon or grid with agents moving

---

## SLIDE 2 - What is MAPF?

**Title:** Multi-Agent Path Finding (MAPF)

**Bullets:**
- k agents on a shared graph G = (V, E)
- Each agent has a start position and a goal position
- Agents move one step per timestep, or wait
- No two agents may occupy the same vertex at the same time (vertex conflict)
- No two agents may swap positions in one step (edge conflict)
- Objective: minimize Sum of Costs (SOC) = total steps across all agents

**Visual:** Small 5x5 grid showing 3 agents (colored circles) with arrows toward their goals. Label starts S1, S2, S3 and goals G1, G2, G3.

**Real-world applications (small icons row):**
- Amazon warehouse robots
- Airport ground traffic control
- Railway scheduling
- Video game AI

---

## SLIDE 3 - Why is Optimal MAPF Hard?

**Title:** Joint State Space Explodes Exponentially

**Bullets:**
- Naive approach: search all agents together in one joint state space
- Joint state space size = O(|V|^k)
- Example: k=10 agents, |V|=5 vertices → ~9.7 million states
- For k=30 agents on a realistic map → completely infeasible

**Table (3 rows, 2 cols):**
| Agents (k) | Joint State Space Size |
|---|---|
| 2 | ~25 |
| 10 | ~9,765,625 |
| 30 | astronomical |

**Our experiment result (highlighted box):**
> Joint A* solved only 32% of 6-agent instances and 0% of 8-agent instances within 5 seconds

---

## SLIDE 4 - Conflict Types

**Title:** Types of Conflicts Between Agents

**Two main conflicts we handle (with diagram for each):**

**Vertex Conflict:**
- Two agents at the SAME vertex at the SAME timestep
- Diagram: two arrows pointing to same cell at t=3

**Edge Conflict (Swap):**
- Two agents crossing the SAME edge in OPPOSITE directions
- Diagram: two arrows crossing between two cells between t=2 and t=3

**Other conflict types (smaller, just listed):**
- Following conflict - one agent follows another on same edge
- Cycle conflict - cyclic dependency between agents
- Swapping conflict - agents exchange positions

**Note at bottom:** We implement vertex + edge conflict detection - sufficient for correctness and optimality

---

## SLIDE 5 - CBS: Two-Level Algorithm

**Title:** Conflict-Based Search (CBS) - Overview

**Visual: Two-level diagram**

```
HIGH LEVEL: Constraint Tree (CT)
    - Best-first search by Sum of Costs
    - Each node = set of constraints per agent
    - Branch on detected conflicts

        ↕ (calls)

LOW LEVEL: Time-Space A* (TSA*)
    - Plans ONE agent at a time
    - State = (vertex v, timestep t)
    - Respects agent's constraint set
    - Heuristic = Manhattan distance (admissible)
```

**Key insight (highlighted):**
> Instead of searching all agents jointly, CBS plans agents independently and resolves only the conflicts that actually occur

---

## SLIDE 6 - Time-Space A* (Low Level)

**Title:** Low Level: Time-Space A* (TSA*)

**Bullets:**
- State = (vertex v, timestep t) - time is part of the state
- Vertex constraint (v, t): agent i forbidden at vertex v at time t
- Edge constraint: agent i forbidden from moving along edge (u→v) at time t
- Heuristic h = Manhattan distance to goal (admissible → optimal)
- Future constraint check at goal: before stopping, verify no future constraints exist at goal vertex

**Visual: Small diagram**
- Show a path on a 4x4 grid
- One cell marked with X at t=3 (constraint)
- Agent path curves around it

**Implemented in:** `tsa_star.py`

---

## SLIDE 7 - CBS High Level: CT Branching

**Title:** High Level: Constraint Tree (CT)

**Step-by-step (numbered list):**
1. Root node: plan each agent independently with TSA*
2. Find first conflict between any two agents
3. If no conflict → return solution (OPTIMAL!)
4. Conflict found (agents i, j at vertex v, time t) → create 2 children:
   - Left child: constrain agent i (forbidden at v, t)
   - Right child: constrain agent j (forbidden at v, t)
5. Replan only the constrained agent with TSA*
6. Push both children to min-heap ordered by Sum of Costs
7. Repeat from step 2

**Visual: Small CT tree diagram**
- Root at top (no constraints, SOC=10)
- Two children: left (constrain A1, SOC=11), right (constrain A2, SOC=12)
- Arrow pointing to left child as "expanded next"

**Guarantee:** CBS is complete and optimal [Sharon et al., 2015]

---

## SLIDE 8 - Our Implementation

**Title:** Our Implementation - Python from Scratch

**Module table:**
| File | Role |
|---|---|
| graph.py | 4-connected Grid with obstacles |
| tsa_star.py | Time-Space A* (Nimrod) |
| conflict.py | Vertex + edge conflict detection (Elad) |
| cbs.py | CT node, CBS main loop (Elad) |
| joint_astar.py | Joint A* baseline (Kfir) |
| benchmark.py | Map generators, experiment runner (Kfir) |
| visualize.py | Result plots (Kfir) |

**Key choices:**
- Baseline: Joint-State-Space A* (searches all agents simultaneously - correct baseline)
- Goal model: agents stay at goal indefinitely (paths padded for conflict checking)
- Conflict selection: first conflict by timestep, then agent pair (i < j)
- All experiments deterministic (seed = 42 + n_agents * 1000 + instance_index)

**Hardware:** Intel Core i7-1255U, 16 GB RAM, Python 3.13

---

## SLIDE 9 - Reproduction Results

**Title:** Result 1: CBS Outperforms Joint A* - Success Rate

**Setup:**
- Map: 20x20 open grid, 10% random obstacles
- 25 instances per agent count, agent counts: 4, 6, 8, 10, 12, 15, 18, 20
- CBS time limit: 30s | Joint A* time limit: 5s

**Table:**
| Agents | CBS Success | Joint A* Success | CBS CT Nodes |
|---|---|---|---|
| 4 | 100% | 100% | 1.7 |
| 6 | 92% | 32% | 3.7 |
| 8 | 100% | 0% | 5.4 |
| 10 | 96% | 0% | 12.7 |
| 12 | 96% | 0% | 70.6 |
| 15 | 64% | 0% | 334.3 |
| 18 | 64% | 0% | 251.3 |
| 20 | 60% | 0% | 716.3 |

**Key finding (highlighted box):**
> Joint A* fails completely from 8 agents onward. CBS maintains 60%+ success even at 20 agents.

**Note:** Matches paper's trend - quantitative differences due to Python vs C++ and smaller grid

---

## SLIDE 10 - Extension: Map Topology Study

**Title:** Extension: Does Map Topology Affect CBS?

**Research question:**
> Do warehouse maps with narrow bottleneck corridors reduce CBS performance compared to open grids?

**Two map types:**
- Open Grid: 20x20, ~10% random obstacles
- Warehouse Grid: 20x20, alternating shelf rows with single-cell corridors every 4 columns

**Visual: Two small grid diagrams side by side**
- Left: open grid with scattered black squares
- Right: warehouse grid with rows of black squares and narrow gaps

**Results at 20 agents:**
| Metric | Open Grid | Warehouse | Difference |
|---|---|---|---|
| Success rate | 64% | 28% | -36% |
| Mean CT nodes | 877 | 3,258 | 3.7x more |
| Mean runtime | 1.54s | 3.14s | 2x slower |

**Why?** Narrow corridors force agents onto the same cells → more vertex conflicts → deeper CT tree → cascade of detours → even more conflicts

---

## SLIDE 11 - Key Findings

**Title:** Summary of Results

**Three main findings:**

**Finding 1 - CBS works and scales:**
- CBS finds provably optimal, collision-free solutions
- Succeeds at 100% for 4 agents, 60% for 20 agents
- Joint A* fails completely from 8 agents onward

**Finding 2 - Map topology matters:**
- Warehouse maps reduce CBS success from 64% to 28% at 20 agents
- CT nodes expand 3.7x more on warehouse maps
- Direct practical implication for warehouse robotics

**Finding 3 - Correct reproduction:**
- Qualitative trends match Sharon et al. (2015) exactly
- Quantitative differences explained by Python vs C++ (~10-50x slower) and smaller grid size

**Limitation:** Basic CBS only - paper's improvements (Prioritizing Conflicts, CBS with Heuristics) would extend scalable range

---

## SLIDE 12 - Conclusion

**Title:** Conclusion

**What we did:**
- Implemented CBS from scratch in Python (7 modules, ~800 lines)
- Reproduced 2 central results from Sharon et al. (2015)
- Extended the study with a warehouse map topology comparison

**Main takeaways:**
- CBS elegantly avoids exponential joint state space by planning agents separately and resolving only actual conflicts
- Warehouse bottlenecks create cascading conflicts that dramatically amplify CBS difficulty
- CBS improvements (Conflict Prioritization, High-Level Heuristics) are especially needed in structured environments

**Future work:**
- Apply CBS improvements to warehouse maps where gap is largest
- Test on standard Moving AI benchmark maps
- Compare Disjoint Splitting variant

**Bottom line (large, centered):**
> CBS: optimal, complete, and practically scalable - but map topology is critical

**Team line:** Nimrod Netzer | Elad Damti | Kfir Dahan - Ready for the defense!

---

## DESIGN NOTES FOR GEMINI

- Slides 1, 12: full visual layout, centered
- Slides 2, 4, 8, 11: bullet-heavy, clean layout
- Slides 3, 9, 10: include tables prominently
- Slides 5, 6, 7: include diagrams/visuals (described above)
- Slide 5: two-box diagram (HIGH LEVEL / LOW LEVEL with arrow between)
- Slide 7: small tree diagram with 3 nodes (root + 2 children)
- Consistent color scheme throughout: white background, blue headers (#1a4f8a), black body text
- Page numbers bottom right on every slide
- University logo top right if available
