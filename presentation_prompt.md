# Presentation Creation Prompt for Gemini - Version 2

Please create a professional academic presentation with EXACTLY 12 slides. No extra slides (no "Image Sources" slide, no appendix).

**CRITICAL RULES:**
- Do NOT write LaTeX math notation like $O(|V|^k)$ - write it as plain text: O(|V|^k)
- Do NOT use external images that might fail to load - draw diagrams using shapes/text boxes only
- Do NOT add extra slides beyond the 12 listed
- Every table must show ALL rows listed - do not skip any rows
- No "$" signs anywhere in the presentation

**Style:**
- White background with dark navy blue (#1a3a5c) top border bar on every slide
- Title font: bold, dark navy (#1a3a5c), 28-32pt
- Body font: regular, dark gray, 18-20pt
- Accent color for highlights: medium blue (#2d6aa0)
- Page number bottom right corner on every slide

---

## SLIDE 1 - Title

**Layout:** Centered, logo top center

**Content:**
- [Bar-Ilan University logo at top]
- Main title (large, bold, navy): **Conflict-Based Search for Optimal Multi-Agent Path Finding**
- Subtitle (smaller, gray): A Reproduction and Extension Study
- Authors: Nimrod Netzer | Elad Damti | Kfir Dahan
- Course: Search in Artificial Intelligence - Bar-Ilan University, 2026
- Reference: Based on: Sharon, Stern, Felner & Sturtevant (2015), Artificial Intelligence Journal

---

## SLIDE 2 - What is MAPF?

**Layout:** Left side bullets, right side visual

**Left side bullets:**
- k agents on a shared graph G = (V, E)
- Each agent: start position si, goal position gi
- Actions: move to adjacent vertex OR wait
- No two agents at same vertex same time (Vertex Conflict)
- No two agents swap positions (Edge Conflict)
- Objective: minimize Sum of Costs (SOC) = total steps all agents

**Right side visual - draw using shapes (NO external image):**
Draw a 5x5 grid using table or shapes. Place:
- Blue circle labeled "A1" at cell (0,0), green circle "A2" at (4,0), red circle "A3" at (0,4)
- Blue star "G1" at (4,4), green star "G2" at (0,4), red star "G3" at (4,0)
- Draw arrows showing paths

**Bottom row - 4 text boxes with icons:**
Warehouse | Airport | Railway | Video Games

---

## SLIDE 3 - Why is MAPF Hard?

**Layout:** Left side text+table, right side highlighted box

**Title:** Why is Optimal MAPF Hard?

**Left side:**

Text: "Naive approach: search all agents jointly in one state space"

State space size = O(|V|^k)  [write exactly like this, no dollar signs]

Table (show all 3 rows):
| Agents (k) | State Space Size |
|---|---|
| 2 | ~25 |
| 10 | ~9,765,625 |
| 30 | Infeasible |

**Right side - blue highlighted box:**
Title: Our Experiment Confirms This:

"Joint A* solved only 32% of 6-agent instances"
"Joint A* solved 0% of 8-agent instances (within 5 seconds)"

Bottom text: Standard A* cannot scale to realistic agent counts

---

## SLIDE 4 - Conflict Types

**Layout:** Three equal columns with rounded boxes

**Title:** Types of Conflicts Between Agents

**Column 1 - Vertex Conflict (draw with shapes):**
- Draw two small grids side by side showing timestep t
- In each grid, show two colored arrows pointing to the SAME cell
- Label: "Agent A1 and A2 at same cell at time t"
- Definition: Two agents occupy the same vertex at the same timestep

**Column 2 - Edge Conflict (draw with shapes):**
- Draw two cells with arrows going in OPPOSITE directions between them
- Arrow 1: left cell -> right cell (blue)
- Arrow 2: right cell -> left cell (red)
- Label: "Agents cross same edge in opposite directions between t and t+1"
- Definition: Also called Swap Conflict

**Column 3 - Other Types:**
- Following Conflict
- Cycle Conflict
- Swapping Conflict

**Bottom note (italic, centered):**
We implement Vertex + Edge conflict detection - sufficient for correctness and optimality

---

## SLIDE 5 - CBS Overview

**Layout:** Two large boxes side by side, key insight at bottom

**Title:** Conflict-Based Search (CBS) - Two-Level Algorithm

**Left box (navy background, white text) - HIGH LEVEL: Constraint Tree (CT):**
- Best-first search ordered by Sum of Costs
- Each CT node stores: constraints per agent + paths + SOC
- Branches on detected conflicts
- Searches only conflicts that actually occur

**Right box (light blue background, dark text) - LOW LEVEL: Time-Space A* (TSA*):**
- Plans ONE agent at a time
- State = (vertex v, timestep t)
- Checks constraints before expanding each state
- Heuristic = Manhattan distance (admissible -> optimal)

**Arrow between boxes pointing both ways labeled: "calls / returns path"**

**Bottom highlighted box (blue border):**
Key Insight: Instead of searching all agents jointly (exponential), CBS plans independently and resolves only actual conflicts

---

## SLIDE 6 - Time-Space A* (Low Level)

**Layout:** Left side bullets, right side diagram drawn with shapes

**Title:** Low Level: Time-Space A* (TSA*)

**Left side bullets:**
- State = (vertex v, timestep t) - time is part of the state
- Vertex constraint (v, t): agent forbidden at vertex v at time t
- Edge constraint: agent forbidden from move (u -> v) at time t
- Heuristic h = Manhattan distance to goal (admissible -> optimal path guaranteed)
- Future constraint check: before stopping at goal, verify no future constraints at goal vertex

- Implemented in: tsa_star.py

**Right side - draw a 4x4 grid using table/shapes:**
- Show a grid with cells labeled by coordinates
- Mark cell (2,1) with a red X and label "Constraint at t=3"
- Draw a blue path that goes AROUND the constraint cell
- Label the path "Agent path avoiding constraint"
- Put a green star at the goal cell (3,3)

---

## SLIDE 7 - CT Branching (High Level)

**Layout:** Left side numbered steps, right side CT tree diagram drawn with shapes

**Title:** High Level: Constraint Tree (CT) - How CBS Branches

**Left side numbered list:**
1. Root node: plan each agent independently with TSA*
2. Find first conflict (agents Ai, Aj at vertex v, time t)
3. If NO conflict -> return solution (OPTIMAL!)
4. Create 2 child CT nodes:
   - Left child: forbid agent Ai at (v, t)
   - Right child: forbid agent Aj at (v, t)
5. Replan ONLY the constrained agent with TSA*
6. Push both children to min-heap by SOC
7. Repeat from step 2

**Right side - draw CT tree with shapes:**

Draw 3 boxes connected by lines:

TOP BOX (navy border):
"ROOT
No constraints
SOC = 10"

BOTTOM LEFT BOX (blue border):
"Constrain A1
forbidden at (3,2) t=4
SOC = 11
<- Expand next (lowest cost)"

BOTTOM RIGHT BOX (gray border):
"Constrain A2
forbidden at (3,2) t=4
SOC = 12"

Lines connecting root to both children. Arrow pointing to left box labeled "expand next"

**Bottom text:** CBS is complete and optimal [Sharon et al., 2015]

---

## SLIDE 8 - Our Implementation

**Layout:** Full-width table, key choices below

**Title:** Our Implementation - Python 3.13 from Scratch

**Table (show ALL 7 rows):**
| File | Role | Lead |
|---|---|---|
| graph.py | 4-connected Grid with obstacles | Team |
| tsa_star.py | Time-Space A* search | Nimrod |
| conflict.py | Vertex + Edge conflict detection | Elad |
| cbs.py | CT node management and CBS main loop | Elad |
| joint_astar.py | Joint-State-Space A* baseline | Kfir |
| benchmark.py | Map generators and experiment runner | Kfir |
| visualize.py | Result plots and graphs | Kfir |

**Below table - two columns:**

Left - Key Implementation Choices:
- Baseline: Joint A* (not Independent A* - searches all agents simultaneously)
- Goal model: agents stay at goal, paths padded for conflict checking
- Conflict selection: first by timestep, then agent pair (i < j)
- All experiments deterministic (fixed seeds)

Right - Hardware and Software:
- Intel Core i7-1255U, 10 cores, 1.70 GHz
- 16 GB RAM, Windows 11 Home
- Python 3.13, matplotlib 3.11
- No external MAPF libraries

---

## SLIDE 9 - Reproduction Results

**Layout:** Full table on left, highlighted finding on right

**Title:** Result 1: CBS vs Joint A* - Success Rate

**Setup line:** 20x20 open grid | 25 instances per count | CBS limit: 30s | Joint A* limit: 5s

**Table (show ALL 8 rows - do not skip any):**
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

**Right side - two highlighted boxes:**

Box 1 (navy background, white text):
"Joint A* fails completely
from 8 agents onward (0%)"

Box 2 (light blue background):
"CBS maintains 60%+ success
even at 20 agents"

**Bottom note:** Matches Sharon et al. (2015) trends. Quantitative differences due to Python vs C++ and smaller 20x20 grid.

---

## SLIDE 10 - Extension Results

**Layout:** Left side two grid diagrams (drawn with shapes), right side table + explanation

**Title:** Extension: Does Map Topology Affect CBS?

**Research question (italic, top):** Do warehouse bottleneck corridors reduce CBS success vs open grids?

**Left side - draw TWO grid diagrams using shapes/tables:**

Grid 1 - OPEN GRID (label above: "Open Grid - 10% random obstacles"):
- Draw a 6x6 table representing the grid
- Randomly fill ~6 cells with dark gray (obstacles)
- Rest stays white
- Label "20x20 in experiments"

Grid 2 - WAREHOUSE GRID (label above: "Warehouse Grid - shelf rows with narrow corridors"):
- Draw a 6x6 table
- Fill entire rows 1, 3, 5 with dark gray EXCEPT one cell in each row (the corridor)
- Label "20x20 in experiments"

**Right side:**

Results at 20 agents table:
| Metric | Open Grid | Warehouse | Ratio |
|---|---|---|---|
| Success Rate | 64% | 28% | -36% |
| Mean CT Nodes | 877 | 3,258 | 3.7x more |
| Mean Runtime | 1.54s | 3.14s | 2x slower |

**Explanation chain (use arrows between boxes):**
[Narrow corridors] -> [Agents forced to same cells] -> [More vertex conflicts] -> [Deeper CT tree] -> [Cascade of detours] -> [3.7x more CT expansions]

---

## SLIDE 11 - Summary of Results

**Layout:** Three equal boxes at top, limitation at bottom

**Title:** Summary of Results

**Box 1 (navy left border, light background):**
Title: Finding 1 - CBS Scales, Joint A* Does Not
- CBS: 100% success at 4 agents, 60% at 20 agents
- Joint A*: 32% at 6 agents, 0% from 8 agents onward
- CBS finds provably optimal conflict-free paths

**Box 2 (navy left border, light background):**
Title: Finding 2 - Map Topology Matters
- Warehouse maps: 64% -> 28% success at 20 agents
- CT nodes: 877 (open) vs 3,258 (warehouse) = 3.7x more
- Direct practical implication for warehouse robotics

**Box 3 (navy left border, light background):**
Title: Finding 3 - Reproduction Validated
- Qualitative trends match Sharon et al. (2015) exactly
- Quantitative gaps explained by Python vs C++ (~10-50x slower)
- Grid size: 20x20 vs larger Moving AI benchmarks

**Bottom box (orange/yellow background):**
Limitation: We implemented basic CBS only. CBS improvements (Prioritizing Conflicts, High-Level Heuristics) would extend the solvable range beyond 20 agents.

---

## SLIDE 12 - Conclusion

**Layout:** Centered, clean

**Title:** Conclusion

**Three bullets:**
- CBS elegantly avoids exponential joint state space by planning agents separately and resolving only actual conflicts
- Warehouse map bottlenecks create cascading vertex conflicts that dramatically amplify CBS difficulty (3.7x more CT nodes)
- Our Python implementation successfully reproduces Sharon et al. (2015) qualitative trends

**Large centered box (navy border, blue text inside):**
CBS: Optimal, complete, and practically scalable - but map topology is critical

**Future work (small text):**
- Apply CBS improvements to warehouse maps
- Test on Moving AI standard benchmark maps

**Bottom centered, bold navy:**
Nimrod Netzer | Elad Damti | Kfir Dahan - Ready for the Defense!

---

## IMPORTANT NOTES FOR GEMINI

1. EXACTLY 12 slides total - no Image Sources slide, no appendix slide
2. All diagrams in slides 4, 6, 7, 10 must be drawn using PowerPoint/Slides SHAPES only - no external images
3. Slide 9 table must have ALL 8 rows (agents 4, 6, 8, 10, 12, 15, 18, 20)
4. No LaTeX notation ($, ^, \to etc.) - use plain text only
5. Slide 10 grid diagrams must be drawn with table cells colored, not images from the internet
6. The presentation already exists with good styling - keep the same navy/white theme from slides 1-12
