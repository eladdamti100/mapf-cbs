# Presentation Fix Instructions - Fix Only These 4 Slides

The presentation is mostly good. Please fix ONLY these specific slides. Keep all other slides exactly as they are.

---

## FIX SLIDE 2 - MAPF Grid Diagram

**Problem:** A3 and G1 are overlapping in the same cell (bottom-right area).

**Fix the 5x5 grid positions:**

Place agents and goals in DIFFERENT cells - no overlapping:

| Label | Color | Row | Column |
|---|---|---|---|
| A1 (agent start) | Blue circle | Row 1 | Col 1 (top-left) |
| A2 (agent start) | Green circle | Row 1 | Col 5 (top-right) |
| A3 (agent start) | Red circle | Row 5 | Col 1 (bottom-left) |
| G1 (goal) | Blue star | Row 5 | Col 5 (bottom-right) |
| G2 (goal) | Green star | Row 3 | Col 1 (middle-left) |
| G3 (goal) | Red star | Row 1 | Col 3 (top-middle) |

Make sure each cell has ONLY ONE label. No two labels in the same cell.

Draw simple arrows:
- Blue arrow from A1 (1,1) going right and down toward G1 (5,5)
- Green arrow from A2 (1,5) going down toward G2 (3,1)
- Red arrow from A3 (5,1) going up toward G3 (1,3)

---

## FIX SLIDE 5 - CBS Overview - Text Cut Off

**Problem:** The last bullet in the HIGH LEVEL box is cut off ("Searches only conflicts that actually")

**Fix:** Replace the 4 bullets in the HIGH LEVEL (navy) box with these SHORTER bullets that fit:

HIGH LEVEL: Constraint Tree (CT):
- Best-first search by Sum of Costs (SOC)
- Each CT node = constraints + paths + SOC
- Branches only on actual conflicts
- Avoids exponential joint search

LOW LEVEL box stays the same.

Also make the two boxes slightly shorter in height so the Key Insight box at the bottom is fully visible and not cut off.

---

## FIX SLIDE 8 - Implementation - Content Cut Off

**Problem:** The bottom section (Key Implementation Choices + Hardware) is partially cut off.

**Fix:** Make the table rows slightly smaller font (10pt instead of 12pt) so there is more space below. Then show the two boxes fully:

Key Implementation Choices (left box):
- Baseline: Joint A* searches all agents simultaneously
- Goal model: agents stay at goal, paths padded for conflict checking
- Conflict selection: first by timestep then agent pair (i < j)
- Seeds: 42 + n_agents x 1000 + instance_index (deterministic)

Hardware and Software (right box):
- Intel Core i7-1255U, 10 cores, 1.70 GHz
- 16 GB RAM, Windows 11 Home
- Python 3.13, matplotlib 3.11
- No external MAPF libraries used

Make sure both boxes are fully visible within the slide boundaries.

---

## FIX SLIDE 10 - Extension - Warehouse Grid Cut Off

**Problem:** The Warehouse Grid diagram at the bottom-left is cut off - the bottom part is not visible.

**Fix two things:**

1. Make BOTH grid diagrams (Open Grid and Warehouse Grid) SMALLER - reduce each grid to fit in the left half of the slide without going out of bounds. Each grid should be about 200x200 pixels maximum.

2. Place them side by side (Open Grid LEFT, Warehouse Grid RIGHT) in the left half of the slide, instead of stacking them vertically. This way both fit without being cut off.

Layout after fix:
- LEFT HALF of slide: two small grids side by side
  - Top-left small grid: Open Grid (6x6, ~8 scattered gray cells)
  - Top-right small grid: Warehouse Grid (6x6, alternating full rows with one gap)
- RIGHT HALF of slide: Results table + arrow chain (stays the same)

Both grids must be FULLY visible within the slide. Label each grid above it.

---

## DO NOT CHANGE

- Slide 1: keep exactly as is
- Slide 3: keep exactly as is
- Slide 4: keep exactly as is
- Slide 6: keep exactly as is
- Slide 7: keep exactly as is
- Slide 9: keep exactly as is
- Slide 11: keep exactly as is
- Slide 12: keep exactly as is
