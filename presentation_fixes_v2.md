# Fix Instructions - Fix Only These 5 Slides

The presentation looks great. Fix ONLY these specific problems. Keep everything else exactly as is.

---

## FIX SLIDE 3 - Why is MAPF Hard?

**Problem:** Title says "Joint State Space Explodes Exponentially" and content is vague. Missing our actual experiment results.

**Change the title to:** Why is Optimal MAPF Hard?

**Keep the ">10M" visual circle on the right exactly as is.**

**Replace the left side text with:**

Text line 1: Naive approach: search all agents jointly in one state space

Formula box (keep the cyan box style): O(|V|^k)

Small text below formula: State space size grows exponentially with agent count

Table below (3 rows, dark style):
| Agents (k) | State Space Size |
|---|---|
| 2 | ~25 states |
| 10 | ~9,765,625 states |
| 30 | Completely infeasible |

**Below the circle on the right - add a cyan highlighted box:**
Title: Our Experiment Confirms This:
- Joint A* solved only 32% of 6-agent instances
- Joint A* solved 0% of 8-agent instances (5s limit)
- CBS succeeds where Joint A* completely fails

---

## FIX SLIDE 5 - CBS Overview

**Problem:** The bullet text in both boxes is AI paraphrasing that is inaccurate and confusing.

**Keep the layout (two boxes side by side, arrow between them, key insight box at bottom).**

**Replace LEFT box (HIGH LEVEL) bullets with exactly:**
Title: HIGH LEVEL: Constraint Tree (CT)
- Best-first search ordered by Sum of Costs (SOC)
- Each CT node stores: constraints per agent + paths + SOC
- Branches on detected conflicts - one node per conflicting agent
- Only replans the constrained agent (not all agents)

**Replace RIGHT box (LOW LEVEL) bullets with exactly:**
Title: LOW LEVEL: Time-Space A* (TSA*)
- Plans ONE agent at a time respecting its constraints
- State = (vertex v, timestep t)
- Checks constraints before expanding each state
- Heuristic = Manhattan distance (admissible - guarantees optimal path)

**Replace the bottom key insight box text with:**
Key Insight: Instead of searching all agents jointly (exponential), CBS plans agents independently and resolves only actual conflicts - achieving optimality with far less computation

---

## FIX SLIDE 7 - CT Branching

**Problem:** Bottom half of slide is completely empty. The "Branch Factor Mechanics" box is small and the slide looks unfinished.

**Keep the top text and the two boxes (Left Branch / Right Branch) exactly as is.**

**Add below the existing content - a CT tree diagram drawn with shapes:**

Draw 3 boxes connected by lines (tree structure):

TOP BOX (outlined in cyan, dark background):
ROOT
No constraints
SOC = 10

LEFT CHILD BOX (outlined in cyan):
Constrain A1
forbidden at (3,2) t=4
SOC = 11
"Expand next - lowest cost"

RIGHT CHILD BOX (outlined in gray, dimmer):
Constrain A2
forbidden at (3,2) t=4
SOC = 12

Draw lines from ROOT down to both children.
Draw a small cyan arrow pointing to the LEFT CHILD with label "expand first (SOC=11 < SOC=12)"

**Add at very bottom of slide:**
CBS is complete and optimal - Sharon et al. (2015)

---

## FIX SLIDE 11 - Summary of Results

**Problem:** Bottom half of slide is completely empty. The 4 bullets are only in the top half.

**Keep the 4 existing bullets exactly as they are.**

**Add below the 4 bullets - a summary table:**

Title for table: Key Numbers at a Glance:

| Metric | Value |
|---|---|
| CBS success at 4 agents | 100% |
| CBS success at 20 agents (open grid) | 60% |
| Joint A* success at 8+ agents | 0% |
| CT nodes open vs warehouse (20 agents) | 877 vs 3,258 (3.7x) |
| CBS runtime at 4 agents | ~2ms |
| CBS runtime at 10 agents (warehouse) | ~0.26s |

**Also add at the very bottom - one line:**
Conclusion: CBS scales practically. Map topology is a critical deployment factor.

---

## FIX SLIDE 1 - Time tags

**Problem:** Slide 1 shows "[TIME: 00:00 - 01:30]" which is wrong - should match the video script.

**Change to:** Nimrod | 0:00 - 0:20

(Same style as the speaker tag in the other version of this presentation - small pill shape top right)

---

## DO NOT CHANGE

- Slide 2: keep exactly as is (grid diagram looks great)
- Slide 4: keep exactly as is (3 conflict type cards look great)
- Slide 6: keep exactly as is (TSA* grid diagram looks great)
- Slide 8: keep exactly as is (7-file table looks great)
- Slide 9: keep exactly as is (8-row results table looks great)
- Slide 10: keep exactly as is (two grids + results table looks great)
- Slide 12: keep exactly as is
