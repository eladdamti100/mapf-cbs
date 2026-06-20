"""Generate PDF report using ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
OUT_PATH = os.path.join(RESULTS_DIR, 'report.pdf')

W, H = A4
MARGIN = 2.2 * cm

def build_styles():
    s = {}
    base = dict(fontName='Times-Roman', fontSize=12, leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
    s['title']   = ParagraphStyle('title',   fontName='Times-Bold',   fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=4)
    s['authors'] = ParagraphStyle('authors', fontName='Times-Roman',  fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=2)
    s['h1']      = ParagraphStyle('h1',      fontName='Times-Bold',   fontSize=13, leading=17, spaceBefore=14, spaceAfter=4)
    s['h2']      = ParagraphStyle('h2',      fontName='Times-Bold',   fontSize=12, leading=16, spaceBefore=10, spaceAfter=3)
    s['body']    = ParagraphStyle('body',    **base)
    s['bullet']  = ParagraphStyle('bullet',  **{**base, 'leftIndent': 14, 'firstLineIndent': -10, 'spaceAfter': 3})
    s['caption'] = ParagraphStyle('caption', fontName='Times-Italic', fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=6)
    s['code']    = ParagraphStyle('code',    fontName='Courier',      fontSize=9,  leading=12, leftIndent=14, spaceAfter=6)
    s['abstract_label'] = ParagraphStyle('abstract_label', fontName='Times-Bold', fontSize=12, leading=16, alignment=TA_CENTER)
    return s

TBL_STYLE = TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#222222')),
    ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
    ('FONTNAME',      (0,0), (-1,0), 'Times-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 10),
    ('FONTNAME',      (0,1), (-1,-1), 'Times-Roman'),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#aaaaaa')),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
])

def make_table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TBL_STYLE)
    return t

def build():
    s = build_styles()
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title='CBS for Optimal MAPF — Reproduction and Extension Study',
        author='Nimrod Netzer, Elad Damti, Kfir Dahan',
    )
    story = []
    W_inner = W - 2 * MARGIN

    def p(text, style='body'): return Paragraph(text, s[style])
    def sp(n=6):               return Spacer(1, n)
    def hr():                  return HRFlowable(width='100%', thickness=0.5, color=colors.black, spaceAfter=4, spaceBefore=4)

    # ── Title ────────────────────────────────────────────────────────────────
    story += [
        sp(4),
        p('Conflict-Based Search for Optimal Multi-Agent Path Finding', 'title'),
        p('A Reproduction and Extension Study', 'authors'),
        sp(4), hr(), sp(4),
        p('Nimrod Netzer &nbsp;&nbsp;|&nbsp;&nbsp; Elad Damti &nbsp;&nbsp;|&nbsp;&nbsp; Kfir Dahan', 'authors'),
        p('Search in Artificial Intelligence — Bar-Ilan University, 2026', 'authors'),
        sp(4), hr(), sp(8),
    ]

    # ── Abstract ─────────────────────────────────────────────────────────────
    story += [
        p('<b>Abstract</b>', 'abstract_label'), sp(4),
        p('Multi-Agent Path Finding (MAPF) is the problem of planning collision-free paths for a set '
          'of agents on a shared graph, minimizing the total travel cost. Solving MAPF optimally is '
          'NP-hard, and naive approaches based on joint-state-space search fail due to exponential '
          'state-space growth. In this work, we reproduce key experimental results from Sharon et al. '
          '(2015), who introduced Conflict-Based Search (CBS) — a two-level algorithm that separates '
          'high-level conflict resolution from low-level single-agent planning. We implement CBS '
          'independently in Python and reproduce two central results: the success rate as a function '
          'of the number of agents, and a comparison against a Joint-State-Space A* baseline. We '
          'further contribute an extension study evaluating how map topology affects CBS performance, '
          'comparing open grid maps against warehouse-style maps with narrow corridors and bottlenecks. '
          'Our results confirm CBS\'s advantage over joint search and reveal that structured maps with '
          'bottlenecks significantly increase conflict frequency and constraint tree depth, reducing '
          'CBS success rates from 64% to 28% at 20 agents.'),
        sp(10),
    ]

    # ── 1. Introduction ──────────────────────────────────────────────────────
    story += [
        p('1. Introduction', 'h1'), hr(),
        p('Multi-Agent Path Finding (MAPF) arises in many real-world domains including automated '
          'warehouses, airport ground traffic management, and railway scheduling [Sharon et al., 2015]. '
          'In these settings, a set of agents must navigate from their respective start locations to '
          'goal locations on a shared graph without colliding.'),
        p('The naïve approach of searching the joint configuration space of all agents using A* '
          'quickly becomes infeasible. The joint state space grows exponentially with the number of '
          'agents: O(|V|<super>k</super>). For k=10 agents on a graph with |V|=5 vertices, the '
          'number of joint states exceeds 9.7 million, making standard search methods impractical '
          'for realistic problem sizes.'),
        p('CBS addresses this by decomposing the problem into a two-level hierarchy. The high level '
          'searches a Constraint Tree (CT), branching on conflicts between agent paths. The low level '
          'plans optimal paths for individual agents subject to a set of constraints.'),
        p('In this project, we (1) reproduce two central experimental results from Sharon et al. (2015) '
          '— the success rate of CBS vs. Joint-State-Space A* and CT expansion statistics — and '
          '(2) contribute an extension study examining how map topology affects CBS performance.'),
        sp(8),
    ]

    # ── 2. Selected Paper Description ────────────────────────────────────────
    story += [
        p('2. Selected Paper Description', 'h1'), hr(),
        p('2.1 Problem Formulation', 'h2'),
        p('The MAPF problem is defined on a graph G=(V,E) with k agents, each with start s<sub>i</sub> '
          'and goal g<sub>i</sub>. At each timestep, an agent moves to an adjacent vertex or waits. '
          'A solution is a set of paths with no vertex conflicts (same vertex, same time) or edge '
          'conflicts (agents swap positions). The objective is to minimize Sum of Costs: '
          'SOC = Σ|π<sub>i</sub>|. Optimal MAPF is NP-hard.'),
        p('2.2 Conflict Types', 'h2'),
        p('The paper identifies five conflict types: (1) <b>Vertex</b> — same vertex, same time; '
          '(2) <b>Edge</b> — agents swap positions; (3) <b>Following</b> — one follows another; '
          '(4) <b>Cycle</b> — cyclic dependency; (5) <b>Swapping</b> — position exchange. '
          'We implement vertex and edge conflicts, sufficient for correctness and optimality.'),
        p('2.3 Why Joint-State-Space A* Fails', 'h2'),
        p('The joint state space grows as O(|V|<super>k</super>). For k=10 agents on |V|=5 vertices: '
          '~9.7 million states. Our experiments confirm: Joint A* succeeds on only 32% of 6-agent '
          'instances and 0% from 8+ agents within a 5-second time limit.'),
        p('2.4 The CBS Algorithm', 'h2'),
        p('<b>Low level — Time-Space A* (TSA*):</b> State = (vertex v, timestep t). A constraint '
          '(v,t) forbids agent i from being at v at time t. Heuristic = Manhattan distance (admissible '
          'on 4-connected grids). TSA* returns the shortest path for one agent respecting its constraints. '
          'Includes future-constraint-aware goal check: agent only stops at goal if no future vertex '
          'constraints exist at that location.'),
        p('<b>High level — Constraint Tree (CT):</b> Binary tree; each node stores constraint sets, '
          'paths, and SOC. CBS proceeds: (1) Plan each agent independently — root CT node. '
          '(2) Find first conflict. (3) If none — return optimal solution. (4) Branch: child left '
          'constrains agent i, child right constrains agent j. (5) Replan constrained agent with TSA*. '
          '(6) Add both children to min-heap by SOC. (7) Pop cheapest — repeat from step 2. '
          'CBS is complete and optimal.'),
        p('2.5 CBS Improvements', 'h2'),
        p('The paper introduces: Prioritizing Conflicts (cardinal conflicts first), CBS with Heuristics '
          '(admissible high-level heuristic), Disjoint Splitting (positive + negative constraints), '
          'Conflict Reasoning (larger constraint sets). We implement basic CBS only.'),
        sp(8),
    ]

    # ── 3. Project Description ───────────────────────────────────────────────
    story += [
        p('3. Project Description', 'h1'), hr(),
        p('3.1 Implementation', 'h2'),
        p('We implemented CBS independently in Python 3.13 across seven modules: '
          '<b>graph.py</b> (4-connected Grid); <b>tsa_star.py</b> (Time-Space A* with constraint '
          'checking and future-constraint-aware goal detection); <b>conflict.py</b> (vertex and edge '
          'conflict detection); <b>cbs.py</b> (CBS high-level constraint tree, min-heap by SOC); '
          '<b>joint_astar.py</b> (true Joint-State-Space A* baseline — searches all agents '
          'simultaneously, matching the paper\'s intended comparison); '
          '<b>benchmark.py</b> (map generators, instance generator, experiment runner); '
          '<b>visualize.py</b> (matplotlib plots and animations).'),
        p('3.2 Team Contributions', 'h2'),
        p('<b>Nimrod Netzer:</b> tsa_star.py (low-level TSA*, state representation, constraint checking). Wrote Abstract, Sections 1–2.', 'bullet'),
        p('<b>Elad Damti:</b> conflict.py (conflict detection), cbs.py (CT, CBS loop, CTNode). Wrote Sections 3–4.', 'bullet'),
        p('<b>Kfir Dahan:</b> joint_astar.py, benchmark.py, visualize.py. Ran all experiments. Wrote Sections 5–6, Reproducibility Statement, AI Disclosure.', 'bullet'),
        p('All three team members participated in testing, debugging, defense preparation, and the recorded video.'),
        p('3.3 Key Implementation Choices', 'h2'),
        p('<b>Baseline:</b> Joint-State-Space A* — searches joint positions of all agents simultaneously. '
          'This matches the paper\'s intended comparison (unlike independent A* which ignores conflicts).', 'bullet'),
        p('<b>Goal model:</b> Agents stay at goal indefinitely (paths padded for conflict checking).', 'bullet'),
        p('<b>Conflict selection:</b> First conflict by timestep, then agent pair index. No prioritization.', 'bullet'),
        p('<b>Seeds:</b> Instance seed = 42 + n_agents × 1000 + instance_index. Deterministic and reproducible.', 'bullet'),
        sp(8),
    ]

    # ── 4. Experiments ───────────────────────────────────────────────────────
    story += [
        p('4. Experiments', 'h1'), hr(),
        p('4.1 Experimental Setup', 'h2'),
        p('<b>Hardware:</b> 12th Gen Intel Core i7-1255U, 10 cores, 1.7GHz, 16GB RAM, Windows 11 Home. '
          '<b>Software:</b> Python 3.13, matplotlib 3.11. No external search libraries. '
          '<b>Maps:</b> 20×20 grid. Open grid: ~10% random obstacles (seed=1). Warehouse grid: '
          'alternating shelf rows, single-cell corridors every 4 columns. '
          '<b>Instances:</b> 25 per agent count, deterministic seeds. '
          '<b>Time limits:</b> 5s for Joint A* (reproduction baseline); 30s for CBS (reproduction); 15s for CBS (extension). '
          '<b>Differences from paper:</b> Python vs. C++, 20×20 grid vs. larger benchmarks, shorter time limits.'),
        p('4.2 Reproduced Results', 'h2'),
        p('Table 1 shows CBS vs. Joint-State-Space A* on an open 20×20 grid. '
          'Joint A* collapses from 8 agents onward, confirming the exponential state-space explosion. '
          'CBS scales gracefully, though it begins timing out beyond 15 agents.'),
        sp(4),
    ]

    tbl1_data = [
        ['Agents', 'CBS\nSuccess', 'CBS Time\n(s)', 'CT Nodes\n(mean)', 'SOC\n(mean)', 'Joint A*\nSuccess'],
        ['4',  '100%', '0.0018', '1.7',   '56.8',  '100%'],
        ['6',  '92%',  '0.0045', '3.7',   '83.8',  '32%'],
        ['8',  '100%', '0.0078', '5.4',   '114.3', '0%'],
        ['10', '96%',  '0.0168', '12.7',  '132.6', '0%'],
        ['12', '96%',  '0.0719', '70.6',  '158.1', '0%'],
        ['15', '64%',  '0.5431', '334.3', '204.8', '0%'],
        ['18', '64%',  '0.3147', '251.3', '236.4', '0%'],
        ['20', '60%',  '1.0958', '716.3', '266.7', '0%'],
    ]
    story += [
        make_table(tbl1_data, [W_inner/6]*6),
        p('Table 1: CBS vs. Joint-State-Space A* on open 20×20 grid. 25 instances per agent count. '
          'Joint A* time limit: 5s; CBS time limit: 30s. Means over successful instances.', 'caption'),
        sp(4),
    ]

    for fig_path, caption in [
        (os.path.join(RESULTS_DIR, 'fig1_success_rate.png'),
         'Figure 1: Success rate vs. number of agents — CBS vs. Joint-State-Space A*.'),
        (os.path.join(RESULTS_DIR, 'fig2_runtime.png'),
         'Figure 2: Mean CBS runtime (seconds) on solved instances.'),
        (os.path.join(RESULTS_DIR, 'fig3_ct_nodes.png'),
         'Figure 3: Mean CT nodes expanded vs. number of agents.'),
    ]:
        if os.path.exists(fig_path):
            story += [
                Image(fig_path, width=W_inner * 0.82, height=W_inner * 0.48),
                p(caption, 'caption'), sp(4),
            ]

    story += [
        p('A key observation: CT nodes jump from 70.6 at 12 agents to 334.3 at 15 agents — '
          'reflecting the exponential worst-case behavior of CBS when many conflicts must be '
          'resolved simultaneously, consistent with Sharon et al. (2015).'),
        p('4.3 Extension Results — Map Topology Study', 'h2'),
        p('<b>Research question:</b> Do warehouse-style maps with narrow corridors and bottlenecks '
          'create more conflicts and reduce CBS success compared to open grids?'),
        sp(4),
    ]

    tbl2_data = [
        ['Agents', 'Open\nSuccess', 'Open\nCT Nodes', 'Open\nTime (s)', 'Warehouse\nSuccess', 'Warehouse\nCT Nodes', 'Warehouse\nTime (s)'],
        ['4',  '100%', '1.7',    '0.0017', '100%', '3.9',    '0.0037'],
        ['6',  '92%',  '3.7',    '0.0044', '100%', '3.2',    '0.0031'],
        ['8',  '100%', '5.4',    '0.0071', '100%', '19.4',   '0.0148'],
        ['10', '96%',  '12.7',   '0.0135', '100%', '125.9',  '0.2617'],
        ['12', '100%', '131.7',  '0.3525', '96%',  '633.7',  '0.8381'],
        ['15', '72%',  '1047.1', '1.6304', '72%',  '655.3',  '0.5128'],
        ['18', '68%',  '920.1',  '0.9647', '36%',  '1845.1', '1.6920'],
        ['20', '64%',  '877.4',  '1.5390', '28%',  '3258.3', '3.1362'],
    ]
    story += [
        make_table(tbl2_data, [W_inner/7]*7),
        p('Table 2: CBS on Open Grid vs. Warehouse Grid. 25 instances per agent count. Time limit: 15s.', 'caption'),
        sp(4),
    ]

    fig4 = os.path.join(RESULTS_DIR, 'fig4_topology_success.png')
    if os.path.exists(fig4):
        story += [
            Image(fig4, width=W_inner * 0.82, height=W_inner * 0.48),
            p('Figure 4: CBS success rate — Open Grid vs. Warehouse Grid.', 'caption'),
            sp(4),
        ]

    story += [
        p('The warehouse grid dramatically underperforms at high agent counts: '
          '20 agents — Open 64% vs. Warehouse 28%. CT nodes at 20 agents: '
          'Open 877 vs. Warehouse 3,258 (3.7×). Bottlenecks force agents into the same '
          'corridor cells, multiplying conflicts and CT branches.'),
        sp(8),
    ]

    # ── 5. Discussion ────────────────────────────────────────────────────────
    story += [
        p('5. Discussion', 'h1'), hr(),
        p('5.1 Agreement with Original Paper', 'h2'),
        p('Our results are qualitatively consistent with Sharon et al. (2015): CBS achieves '
          'near-perfect success for small agent counts and degrades gracefully; Joint-State-Space A* '
          'fails completely from 8 agents; CT expansions grow exponentially beyond ~12 agents. '
          'Quantitative differences are expected due to Python vs. C++, smaller grid, and shorter time limits.'),
        p('5.2 Extension Findings', 'h2'),
        p('Warehouse maps increase conflict density due to bottlenecks: agents must funnel through '
          'narrow corridors, creating vertex conflicts that force CT branches. The constrained agent '
          'takes longer detours, creating new conflicts in adjacent corridors. At 20 agents, '
          'CBS expands 3,258 CT nodes on warehouse vs. 877 on open — a 3.7× difference. '
          'This confirms that CBS improvements (conflict prioritization, high-level heuristics) '
          'would be most beneficial in warehouse-like environments.'),
        p('5.3 Limitations', 'h2'),
        p('Python is ~10–50× slower than C++; 20×20 grids are smaller than paper benchmarks; '
          'basic CBS lacks improvements that would extend the success range.'),
        sp(8),
    ]

    # ── 6. Conclusion ────────────────────────────────────────────────────────
    story += [
        p('6. Conclusion', 'h1'), hr(),
        p('We implemented CBS from scratch in Python and reproduced its two central experimental '
          'results. CBS finds provably optimal, collision-free solutions while scaling significantly '
          'better than Joint-State-Space A*, which fails completely from 8 agents. Our extension '
          'study shows that warehouse bottlenecks reduce CBS success from 64% to 28% at 20 agents '
          'and increase CT expansions by 3.7×. Future work should apply CBS improvements specifically '
          'to warehouse environments where the performance gap is largest.'),
        sp(8),
    ]

    # ── References ───────────────────────────────────────────────────────────
    story += [
        p('References', 'h1'), hr(),
        p('Sharon, G., Stern, R., Felner, A., &amp; Sturtevant, N. R. (2015). Conflict-based search '
          'for optimal multi-agent pathfinding. <i>Artificial Intelligence</i>, 219, 40–66.'),
        p('Sturtevant, N. R. (2012). Benchmarks for grid-based pathfinding. '
          '<i>IEEE Transactions on Computational Intelligence and AI in Games</i>, 4(2), 144–148.'),
        sp(8),
    ]

    # ── Reproducibility Statement ─────────────────────────────────────────────
    story += [
        p('Reproducibility Statement', 'h1'), hr(),
        p('<b>Results reproduced:</b> (1) Success rate of CBS vs. Joint-State-Space A* as a function '
          'of agent count. (2) Runtime and CT node expansion statistics.'),
        p('<b>Results NOT reproduced:</b> Experiments on Moving AI benchmark maps; comparisons to ICTS '
          'or CBS improvement variants.'),
        p('<b>Implementation:</b> New independent implementation in Python 3.13. Original authors\' '
          'code was not used.'),
        p('<b>Changes from original:</b> 20×20 grid (vs. larger benchmarks), 5s/30s time limits, '
          'Python instead of C++, randomly generated maps.'),
        p('<b>Agreement:</b> Qualitative trends match. Absolute numbers differ due to language, '
          'grid size, and time limit.'),
        p('<b>Files:</b> graph.py, tsa_star.py, conflict.py, cbs.py, joint_astar.py, benchmark.py, '
          'visualize.py, main.py; results/reproduce_open.csv, extension_open.csv, extension_warehouse.csv; '
          'fig1–fig4.png.'),
        p('<b>How to run:</b>'),
        p('pip install matplotlib', 'code'),
        p('python main.py --mode reproduce --n-instances 25 --time-limit 30 --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        p('python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        sp(8),
    ]

    # ── AI Tools Disclosure ───────────────────────────────────────────────────
    story += [
        p('AI Tools Disclosure', 'h1'), hr(),
        p('<b>Claude (Anthropic, claude-sonnet-4-6):</b> Used for implementation assistance '
          '(code structure, TSA* and CBS implementation, debugging), report writing, algorithm '
          'explanations, and project planning. All code was reviewed, understood, and validated by the team.', 'bullet'),
        p('The team takes full responsibility for the correctness, originality, and quality of all submitted work.'),
    ]

    doc.build(story)
    print(f'Report saved to: {OUT_PATH}')

if __name__ == '__main__':
    build()
