# Presentation Prompt Version 3 - Fix Existing Dark-Theme Presentation

I have an existing dark-theme presentation (12 slides + 1 Image Sources slide). 
Keep the exact same dark navy background style, cyan accent color, speaker time tags.
Fix ONLY the problems listed below.

---

## CRITICAL GLOBAL RULES

- Do NOT use any external images from the internet
- Do NOT add an "Image Sources" slide - delete it entirely
- EXACTLY 12 slides total
- No LaTeX notation - plain text only
- No em-dashes - use hyphens only

---

## SLIDE 1 - Keep exactly as is

Title slide looks great. No changes.

---

## SLIDE 2 - Fix: Replace warehouse photo with drawn grid

**Problem:** Slide has a real warehouse photo from the internet. Replace it with a drawn diagram.

**Keep:** All the text bullets on the left side. Keep the same dark theme.

**Replace the right side photo with this drawn diagram:**

Draw a 5x5 grid (table with thin light borders on dark background).
Place these labels in the cells (each cell has ONLY ONE label):

- Row 1, Col 1: Blue filled circle with text "A1"
- Row 1, Col 5: Green filled circle with text "A2"  
- Row 5, Col 1: Red filled circle with text "A3"
- Row 5, Col 5: Blue star shape with text "G1"
- Row 3, Col 3: Green star shape with text "G2"
- Row 1, Col 3: Red star shape with text "G3"

Draw 3 arrows (thin, colored):
- Blue arrow: diagonal from A1 to G1
- Green arrow: from A2 going left and down to G2
- Red arrow: from A3 going up to G3

Label below grid: "Example: 3 agents, 5x5 grid"

---

## SLIDE 3 - Keep exactly as is

The ">10M nodes" visual looks great. No changes.

---

## SLIDE 4 - Fix: Remove math formulas, add third conflict type box

**Problem:** The formula boxes show broken math notation ("a1 = a2 at vertexvat timet" and "a1 swaps witha2 on edgeeatt -> t+1"). Also missing "Other Types" column.

**Fix the formula boxes - replace with plain text:**

Vertex Conflict box formula:
Replace with: "Agent A1 and A2 at the same cell at time t"

Edge Conflict box formula:
Replace with: "Agent A1 moves right, Agent A2 moves left, crossing same edge between t and t+1"

**Add a third card on the right:**
Title: Other Conflict Types
- Following Conflict
- Cycle Conflict  
- Swapping Conflict

Note (italic, bottom center): We implement Vertex + Edge detection - sufficient for optimality

---

## SLIDE 5 - Keep exactly as is

CBS Overview with High-Level / Low-Level boxes looks great. No changes.

---

## SLIDE 6 - Fix: Replace wrong image with drawn TSA* grid

**Problem:** Slide shows a "Hyper graph built after clustering" image from the internet - completely wrong topic. Replace with a drawn grid.

**Keep:** All the text on the left side exactly as is.

**Replace the right side image with this drawn diagram:**

Draw a 4x4 grid (table with light borders on dark background).

Color the cells:
- Row 1, Col 1: Dark teal circle labeled "A" (agent start)
- Row 1, Col 2: Light blue - label "t=1"
- Row 2, Col 2: Light blue - label "t=2"
- Row 2, Col 3: RED cell - label "X" with small text below "Constraint t=3"
- Row 3, Col 3: Light blue - label "t=4"  
- Row 4, Col 4: Green cell or circle - label "G"
- Row 3, Col 4: Light blue - label "t=5"

Draw a blue dotted line connecting: A -> t=1 -> t=2 -> (skips X, goes around) -> t=4 -> t=5 -> G

Label below: "Agent avoids constrained cell, finds alternate path"

---

## SLIDE 7 - Keep exactly as is

High-Level Branching timeline looks great. No changes.

---

## SLIDE 8 - Fix: Show all 7 modules, not 3 categories

**Problem:** Slide groups files into 3 category boxes (Algorithmic Engine, Data & Conflict, Validation) - missing joint_astar.py and visualize.py.

**Replace the 3 category boxes with a full table showing all 7 files:**

Title stays: "Our Python Implementation"
Subtitle stays: "We developed a highly cohesive modular implementation in Python 3."

Table (dark header row, alternating dark rows, cyan text for filenames):
| File | Role | Lead |
|---|---|---|
| graph.py | 4-connected grid with obstacles | Team |
| tsa_star.py | Time-Space A* low-level solver | Nimrod |
| conflict.py | Vertex + Edge conflict detection | Elad |
| cbs.py | Constraint Tree high-level loop | Elad |
| joint_astar.py | Joint-State-Space A* baseline | Kfir |
| benchmark.py | Map generators + experiment runner | Kfir |
| visualize.py | Result plots and graphs | Kfir |

Below table - one line in smaller text:
"No external MAPF libraries. Python 3.13, Intel i7-1255U, 16 GB RAM."

---

## SLIDE 9 - Fix: Correct numbers and show all 8 agent counts

**Problem 1:** Says "Baseline (Independent A*)" - must be "Joint A*" (not Independent)
**Problem 2:** Only shows 5 agent counts (4, 8, 12, 16, 20) with wrong percentages
**Problem 3:** Numbers are wrong (shows 88%, 68%, 52%, 36% - these are not our results)

**Replace entire slide content:**

Title: Reproduction Results
Subtitle: Success Rate vs. Agent Count

Setup line (small text): 20x20 open grid | 25 instances per agent count | CBS limit: 30s | Joint A* limit: 5s

**Replace the bar chart with a table (ALL 8 rows - do not skip any):**

| Agents | CBS Success | Joint A* Success | Mean CT Nodes |
|---|---|---|---|
| 4 | 100% | 100% | 1.7 |
| 6 | 92% | 32% | 3.7 |
| 8 | 100% | 0% | 5.4 |
| 10 | 96% | 0% | 12.7 |
| 12 | 96% | 0% | 70.6 |
| 15 | 64% | 0% | 334.3 |
| 18 | 64% | 0% | 251.3 |
| 20 | 60% | 0% | 716.3 |

On the right side, two highlight boxes:
Box 1 (dark accent):
"Joint A* fails completely from 8 agents onward (0%)"

Box 2 (lighter accent):
"CBS maintains 60%+ success even at 20 agents"

Small note at bottom: Matches Sharon et al. (2015) qualitative trends. Differences due to Python vs C++ speed.

---

## SLIDE 10 - Fix: Add actual numbers and results table

**Problem:** Slide describes the two map types well but has NO numbers/results.

**Keep:** The research question and the two cards describing Open Grid and Warehouse Grid.

**Add below the two cards - a results table:**

Title for table: "Results at 20 Agents:"

| Metric | Open Grid | Warehouse Grid |
|---|---|---|
| Success Rate | 64% | 28% |
| Mean CT Nodes | 877 | 3,258 (3.7x more) |
| Mean Runtime | 1.54s | 3.14s (2x slower) |

Below table, one-line explanation:
"Narrow corridors force agents onto same cells -> more vertex conflicts -> deeper CT tree -> 3.7x more expansions"

---

## SLIDE 11 - Fix: Add specific numbers to bullets

**Problem:** Bullets are vague - no actual numbers.

**Keep the same layout and style.**

**Replace bullet text with these numbered versions:**

Bullet 1 - "CBS Delivers Optimality: CBS achieves 100% success at 4 agents and 60% at 20 agents. Joint A* fails completely from 8 agents onward (0% success rate)."

Bullet 2 - "Corridors are Bottlenecks: Warehouse grids reduce CBS success from 64% to 28% at 20 agents, with 3.7x more CT node expansions (877 vs 3,258)."

Bullet 3 - "High Efficiency: CBS plans 4 agents in ~2ms. At 10 agents on warehouse grid: ~0.26s mean runtime."

Bullet 4 - "Limitations: Beyond 20 agents, CBS times out more often - motivating CBS improvements (Prioritizing Conflicts, High-Level Heuristics)."

---

## SLIDE 12 - Fix: Remove "ready for defense" phrase

**Keep:** The "Questions & Defense" title. Keep the thank you text and names.

**Change:** Remove "Our optimal Multi-Agent Pathfinding suite is ready for experimental defense."

**Replace with:** "CBS elegantly resolves conflicts lazily - planning independently and branching only on actual collisions. Warehouse map topology is a critical factor for real deployments."

Keep the 3 names at the bottom: NIMROD NETZER - ELAD DAMTI - KFIR DAHAN

---

## DELETE SLIDE 13 - Image Sources

Delete the "Image Sources" slide entirely. The final presentation must have exactly 12 slides.

---

## SUMMARY OF WHAT TO CHANGE

| Slide | Action |
|---|---|
| 1 | Keep as is |
| 2 | Replace warehouse photo with drawn 5x5 grid |
| 3 | Keep as is |
| 4 | Fix broken formulas, add third "Other Types" card |
| 5 | Keep as is |
| 6 | Replace wrong "Hyper graph" image with drawn 4x4 TSA* grid |
| 7 | Keep as is |
| 8 | Replace 3 category boxes with full 7-file table |
| 9 | Fix baseline name to "Joint A*", replace bar chart with correct 8-row table |
| 10 | Add results table with numbers below the two map description cards |
| 11 | Add specific numbers to all 4 bullets |
| 12 | Remove "ready for defense" phrase |
| 13 | DELETE this slide entirely |
