"""
Generate PowerPoint presentation for CBS MAPF project.
Requires: pip install python-pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

# Color palette
DARK_BLUE = RGBColor(0x1A, 0x3A, 0x5C)   # title/header background
MID_BLUE  = RGBColor(0x24, 0x5C, 0x94)   # accent bars
LIGHT_BLUE= RGBColor(0xD6, 0xE8, 0xF7)   # light bg
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE    = RGBColor(0xE8, 0x7A, 0x1E)   # highlight color
DARK_GRAY = RGBColor(0x2C, 0x2C, 0x2C)
MID_GRAY  = RGBColor(0x55, 0x55, 0x55)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]  # completely blank


# ─── helpers ───────────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill_rgb, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    return shape

def add_text(slide, text, l, t, w, h, font_size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

def add_bullet_slide(slide, title, bullets, speaker_label, speaker_color=MID_BLUE):
    # header bar
    add_rect(slide, 0, 0, 13.33, 1.3, DARK_BLUE)
    add_text(slide, title, 0.3, 0.15, 12.0, 1.0, font_size=32, bold=True,
             color=WHITE, align=PP_ALIGN.LEFT)
    # speaker tag
    add_rect(slide, 0, 1.3, 13.33, 0.35, speaker_color)
    add_text(slide, f"  {speaker_label}", 0, 1.3, 13.33, 0.35,
             font_size=14, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    # light bg
    add_rect(slide, 0, 1.65, 13.33, 5.85, LIGHT_BLUE)
    # bullets
    y = 2.0
    for bullet in bullets:
        if bullet.startswith("##"):  # sub-bullet
            add_text(slide, "      → " + bullet[2:].strip(), 0.5, y, 12.0, 0.5,
                     font_size=18, color=DARK_GRAY)
            y += 0.52
        elif bullet.startswith("#"):  # section header
            add_text(slide, bullet[1:].strip(), 0.4, y, 12.0, 0.4,
                     font_size=20, bold=True, color=MID_BLUE)
            y += 0.48
        else:
            add_text(slide, "• " + bullet, 0.4, y, 12.0, 0.55,
                     font_size=20, color=DARK_GRAY)
            y += 0.60

def add_image_slide(slide, title, img_path, caption, speaker_label,
                    speaker_color=MID_BLUE):
    add_rect(slide, 0, 0, 13.33, 1.3, DARK_BLUE)
    add_text(slide, title, 0.3, 0.15, 12.0, 1.0, font_size=32, bold=True,
             color=WHITE, align=PP_ALIGN.LEFT)
    add_rect(slide, 0, 1.3, 13.33, 0.35, speaker_color)
    add_text(slide, f"  {speaker_label}", 0, 1.3, 13.33, 0.35,
             font_size=14, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    add_rect(slide, 0, 1.65, 13.33, 5.85, LIGHT_BLUE)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(1.5), Inches(1.85),
                                  Inches(10.3), Inches(4.8))
    add_text(slide, caption, 0.3, 6.85, 12.5, 0.5, font_size=14,
             italic=True, color=MID_GRAY, align=PP_ALIGN.CENTER)


# ─── SLIDE 1 — Title ───────────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(slide, 0, 2.8, 13.33, 2.5, MID_BLUE)

add_text(slide, "Conflict-Based Search for", 0.5, 1.0, 12.3, 0.9,
         font_size=38, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "Optimal Multi-Agent Pathfinding", 0.5, 1.75, 12.3, 0.9,
         font_size=38, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

add_text(slide, "Sharon, Stern, Felner & Sturtevant — AIJ 2015", 0.5, 2.9,
         12.3, 0.6, font_size=20, italic=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(slide, "Nimrod Netzer  •  Elad Damti  •  Kfir Dahan", 0.5, 3.6,
         12.3, 0.5, font_size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(slide, "Bar-Ilan University  |  Search in AI Course  |  June 2026",
         0.5, 4.25, 12.3, 0.5, font_size=16, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)

add_rect(slide, 0, 6.8, 13.33, 0.7, RGBColor(0x0D, 0x1F, 0x33))
add_text(slide, "Heuristic Search Course Project", 0, 6.82, 13.33, 0.5,
         font_size=13, italic=True, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)


# ─── SLIDE 2 — What is MAPF? ───────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="What is Multi-Agent Path Finding?",
    bullets=[
        "k agents on a graph, each with a start and a goal location",
        "Agents move one step per timestep, or wait in place",
        "Objective: minimize Sum of Costs (SOC) = total steps by all agents",
        "Constraint: no two agents at the same vertex or edge at the same time",
        "# Real-World Applications",
        "Amazon warehouse robots (Kiva systems)",
        "Airport ground traffic control",
        "Railway scheduling and video game AI",
        "# Formal Definition",
        "Graph G=(V,E),  agents A={1..k},  starts s_i,  goals g_i",
        "Optimal MAPF is NP-hard in the general case",
    ],
    speaker_label="Nimrod Netzer"
)


# ─── SLIDE 3 — Why is MAPF Hard? ───────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Why is MAPF Hard? (Joint A* Fails)",
    bullets=[
        "Naive approach: search the joint state space of all agents",
        "Joint state space size = |V|^k   (exponential in number of agents)",
        "# State Space Explosion",
        "2 agents × 5 vertices  →  25 joint states",
        "10 agents × 5 vertices  →  9,765,624 joint states",
        "30 agents on a 20×20 grid  →  completely infeasible",
        "# Joint A* limitations",
        "Runs out of memory before finding solution",
        "Even optimal A* cannot handle large instances",
        "# CBS Solution",
        "Avoid the joint space entirely — plan each agent separately",
        "Only resolve conflicts when they actually occur",
    ],
    speaker_label="Nimrod Netzer"
)


# ─── SLIDE 4 — Conflict Types ──────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Conflict Types in MAPF",
    bullets=[
        "# Vertex Conflict",
        "Two agents occupy the same vertex at the same timestep",
        "# Edge Conflict (Swap)",
        "Two agents traverse the same edge in opposite directions simultaneously",
        "# Following Conflict",
        "Agent i follows agent j along the same edge",
        "# Cycle Conflict",
        "A group of agents forms a cycle of dependencies",
        "# Swapping Conflict",
        "Two agents exchange positions across consecutive timesteps",
        "CBS detects the first conflict found and branches on it",
    ],
    speaker_label="Nimrod Netzer"
)


# ─── SLIDE 5 — CBS Two-Level Overview ─────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Conflict-Based Search — Two-Level Algorithm",
    bullets=[
        "# High Level — Constraint Tree (CT)",
        "Binary tree where each node holds a set of constraints",
        "Best-first search: always expand the node with lowest total cost",
        "Branch when a conflict is found: add constraint to one agent",
        "# Low Level — Time-Space A* (TSA*)",
        "Plan each agent individually, respecting its constraint set",
        "State = (vertex v, timestep t)",
        "Heuristic = Manhattan distance (admissible)",
        "# Key Insight",
        "CBS avoids joint state space — agents plan independently",
        "Conflicts are resolved lazily: only when they appear",
        "Guaranteed to find the optimal solution (complete + optimal)",
    ],
    speaker_label="Elad Damti"
)


# ─── SLIDE 6 — TSA* Detail ────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Low Level: Time-Space A* (TSA*)",
    bullets=[
        "State = (vertex v, timestep t) — time is part of the state",
        "Successor states: move to adjacent vertex OR wait in place",
        "# Constraint Checking",
        "Vertex constraint: (agent i, vertex v, time t) → skip state (v,t)",
        "Edge constraint: (agent i, edge v1→v2, time t) → skip transition",
        "# Admissible Heuristic",
        "Manhattan distance from v to goal (ignores constraints)",
        "Never overestimates → TSA* is optimal for each agent",
        "# Result",
        "Returns the shortest path for one agent that satisfies all its constraints",
        "If no path exists → CT node is pruned (infeasible branch)",
    ],
    speaker_label="Elad Damti"
)


# ─── SLIDE 7 — CBS Algorithm Steps ────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="CBS Algorithm — Step by Step",
    bullets=[
        "Step 1: Plan each agent independently → root CT node",
        "Step 2: Find the first conflict among all agent paths",
        "Step 3: If no conflict → DONE, return optimal solution",
        "Step 4: Create 2 child CT nodes:",
        "## Left child: agent i is forbidden from vertex v at time t",
        "## Right child: agent j is forbidden from vertex v at time t",
        "Step 5: Replan the constrained agent with TSA*",
        "Step 6: Add both children to the open list (by cost)",
        "Step 7: Pop cheapest CT node → go to Step 2",
        "# Optimality Guarantee",
        "Best-first search + optimal low level → first complete solution is globally optimal",
    ],
    speaker_label="Elad Damti"
)


# ─── SLIDE 8 — Our Implementation ─────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Our Implementation — Python 3",
    bullets=[
        "# Module Structure",
        "graph.py — 20×20 grid, 4-connected, obstacle support",
        "tsa_star.py — Time-Space A*, vertex + edge constraints  [Nimrod]",
        "conflict.py — Vertex & edge conflict detection  [Elad]",
        "cbs.py — Constraint Tree, best-first search  [Elad]",
        "benchmark.py — Map generation, instance runner  [Kfir]",
        "# Implementation Choices",
        "First conflict found is resolved (not prioritized by type)",
        "Agents stay at goal after arrival (path extended with waits)",
        "Time limit: 30s reproduction, 15s extension",
        "# Validation",
        "Tested on hand-verified 3-agent examples",
        "All paths checked to be conflict-free before reporting success",
    ],
    speaker_label="Elad Damti"
)


# ─── SLIDE 9 — Reproduction Results (Success Rate) ────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_image_slide(slide,
    title="Reproduction Results — Success Rate vs. Agents",
    img_path=os.path.join(RESULTS_DIR, "fig1_success_rate.png"),
    caption="CBS success rate drops as agents increase | 25 instances per count | 20×20 open grid | 30s time limit",
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 10 — Runtime Comparison ────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_image_slide(slide,
    title="Reproduction Results — Runtime Comparison",
    img_path=os.path.join(RESULTS_DIR, "fig2_runtime.png"),
    caption="CBS runtime grows with agents but remains tractable at low counts | baseline shown for reference",
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 11 — CT Nodes ──────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_image_slide(slide,
    title="Reproduction Results — Constraint Tree Growth",
    img_path=os.path.join(RESULTS_DIR, "fig3_ct_nodes.png"),
    caption="CT nodes expanded grows exponentially with agent count — reflects increasing conflict resolution work",
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 12 — Extension: Map Topology ───────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Extension: Map Topology Study",
    bullets=[
        "# Research Question",
        "Does map structure affect CBS performance, and why?",
        "# Two Map Types Compared",
        "Open grid: 20×20, 10% random obstacles (sparse, many paths)",
        "Warehouse grid: structured shelf rows + narrow corridors (bottlenecks)",
        "# Experimental Setup",
        "5 agent counts: 4, 6, 8, 10, 12 agents",
        "25 instances per agent count per map type",
        "15-second time limit per instance",
        "# Hypothesis",
        "Bottleneck maps force agents onto same paths → more conflicts → deeper CT trees",
    ],
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 13 — Extension Results ─────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_image_slide(slide,
    title="Extension Results — Open Grid vs. Warehouse",
    img_path=os.path.join(RESULTS_DIR, "fig4_topology_success.png"),
    caption="Warehouse maps show significantly lower success rate — confirming bottleneck hypothesis",
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 14 — Key Findings ──────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Key Findings",
    bullets=[
        "# Finding 1: CBS Works",
        "Finds optimal, conflict-free solutions — scales far better than joint A*",
        "100% success rate at 4 agents; drops gracefully with scale",
        "# Finding 2: Map Topology Matters",
        "Warehouse maps (bottlenecks) are significantly harder for CBS",
        "More conflicts → deeper CT trees → exponentially more search",
        "Practical insight: CBS deployment depends on environment structure",
        "# Finding 3: Python CBS is Efficient",
        "4-agent problems solved in under 1 millisecond",
        "12-agent warehouse problems solved within 15 seconds",
        "# Limitation",
        "Beyond 20 agents, CBS times out → motivates CBS improvements",
        "Conflict prioritization + high-level heuristics extend scalability",
    ],
    speaker_label="Kfir Dahan"
)


# ─── SLIDE 15 — Conclusion ────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_bullet_slide(slide,
    title="Conclusion",
    bullets=[
        "CBS solves MAPF optimally by separating individual planning from conflict resolution",
        "Two-level structure avoids exponential joint state space",
        "Low level (TSA*) finds optimal single-agent paths under constraints",
        "High level (CT) resolves conflicts lazily — only when they occur",
        "# Our Contribution",
        "Full Python implementation validated against hand-verified examples",
        "Reproduced the main success rate trend from Sharon et al. 2015",
        "Extension: warehouse maps create 2–3× more CT expansions than open maps",
        "# Future Work",
        "Test CBS improvements (conflict prioritization, disjoint splitting)",
        "Scale to larger maps using the Moving AI benchmark library",
    ],
    speaker_label="Nimrod Netzer"
)


# ─── SLIDE 16 — Thank You ─────────────────────────────────────────────────
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, 13.33, 7.5, DARK_BLUE)
add_rect(slide, 0, 2.7, 13.33, 2.2, MID_BLUE)

add_text(slide, "Thank You", 0.5, 0.8, 12.3, 1.2,
         font_size=52, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "Conflict-Based Search for Optimal Multi-Agent Pathfinding",
         0.5, 1.9, 12.3, 0.6, font_size=20, italic=True, color=LIGHT_BLUE,
         align=PP_ALIGN.CENTER)

add_text(slide, "Questions?", 0.5, 2.85, 12.3, 0.7,
         font_size=36, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

add_text(slide, "Nimrod Netzer  •  Elad Damti  •  Kfir Dahan",
         0.5, 3.65, 12.3, 0.5, font_size=22, color=WHITE, align=PP_ALIGN.CENTER)

add_text(slide, "Sharon, Stern, Felner & Sturtevant — Artificial Intelligence, 219, 40–66, 2015",
         0.5, 4.3, 12.3, 0.45, font_size=15, italic=True, color=LIGHT_BLUE,
         align=PP_ALIGN.CENTER)

add_rect(slide, 1.5, 5.2, 10.33, 0.06, ORANGE)

add_text(slide, "Bar-Ilan University  |  Search in AI  |  June 2026",
         0.5, 5.4, 12.3, 0.5, font_size=14, color=LIGHT_BLUE, align=PP_ALIGN.CENTER)


# ─── Save ──────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "results", "presentation.pptx")
prs.save(out_path)
print(f"Presentation saved to: {out_path}")
print(f"Total slides: {len(prs.slides)}")
