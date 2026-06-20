"""Generate PDF report - at most 6 pages content + page 7 references only."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas as pdfcanvas
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
OUT_PATH = os.path.join(RESULTS_DIR, 'report.pdf')

W, H = A4
MARGIN = 1.8 * cm
W_INNER = W - 2 * MARGIN


class NumberedCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont('Times-Roman', 10)
            self.setFillColor(colors.HexColor('#444444'))
            self.drawCentredString(W / 2, 0.7 * cm, str(self._pageNumber))
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)


def S():
    s = {}
    s['title'] = ParagraphStyle('title', fontName='Times-Bold',   fontSize=14, leading=18, alignment=TA_CENTER, spaceAfter=3)
    s['sub']   = ParagraphStyle('sub',   fontName='Times-Roman',  fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=1)
    s['h1']    = ParagraphStyle('h1',    fontName='Times-Bold',   fontSize=12, leading=15, spaceBefore=6, spaceAfter=2)
    s['h2']    = ParagraphStyle('h2',    fontName='Times-Bold',   fontSize=12, leading=15, spaceBefore=4, spaceAfter=1)
    s['body']  = ParagraphStyle('body',  fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=4, alignment=TA_JUSTIFY)
    s['bul']   = ParagraphStyle('bul',   fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=2, alignment=TA_JUSTIFY, leftIndent=14, firstLineIndent=-10)
    s['cap']   = ParagraphStyle('cap',   fontName='Times-Italic', fontSize=9,  leading=12, alignment=TA_CENTER, spaceAfter=3, spaceBefore=2)
    s['code']  = ParagraphStyle('code',  fontName='Courier',      fontSize=8,  leading=12, leftIndent=12, spaceAfter=3, wordWrap='LTR')
    s['abl']   = ParagraphStyle('abl',   fontName='Times-Bold',   fontSize=12, leading=15, alignment=TA_CENTER, spaceAfter=3)
    s['bodyl'] = ParagraphStyle('bodyl', fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=4, alignment=TA_LEFT)
    s['ref']   = ParagraphStyle('ref',   fontName='Times-Roman',  fontSize=12, leading=16, spaceAfter=6, alignment=TA_LEFT, leftIndent=18, firstLineIndent=-18)
    return s


TABLE_STYLE = TableStyle([
    ('BACKGROUND',    (0, 0), (-1, 0), colors.HexColor('#222222')),
    ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
    ('FONTNAME',      (0, 0), (-1, 0), 'Times-Bold'),
    ('FONTNAME',      (0, 1), (-1, -1), 'Times-Roman'),
    ('FONTSIZE',      (0, 0), (-1, -1), 9),
    ('GRID',          (0, 0), (-1, -1), 0.4, colors.HexColor('#aaaaaa')),
    ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f4f4')]),
    ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING',    (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LEFTPADDING',   (0, 0), (-1, -1), 4),
    ('RIGHTPADDING',  (0, 0), (-1, -1), 4),
])


def mktbl(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TABLE_STYLE)
    return t


def hr():
    return HRFlowable(width='100%', thickness=0.5, color=colors.black, spaceAfter=3, spaceBefore=1)


def side_by_side(path_a, path_b, w_frac=0.49, h_frac=0.65):
    """Two images side by side in a Table."""
    iw = W_INNER * w_frac
    ih = iw * h_frac
    row = [[Image(path_a, width=iw, height=ih), Image(path_b, width=iw, height=ih)]]
    t = Table(row, colWidths=[iw, iw])
    t.setStyle(TableStyle([
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    return t


def build():
    s = S()
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title='CBS for Optimal MAPF',
        author='Nimrod Netzer, Elad Damti, Kfir Dahan',
    )

    def p(t, st='body'): return Paragraph(t, s[st])
    def sp(n=3):         return Spacer(1, n)

    story = []

    # ----------------------------------------------------------
    # TITLE BLOCK
    # ----------------------------------------------------------
    story += [
        p('Conflict-Based Search for Optimal Multi-Agent Path Finding', 'title'),
        p('A Reproduction and Extension Study', 'sub'),
        hr(),
        p('Nimrod Netzer | Elad Damti | Kfir Dahan', 'sub'),
        p('Search in Artificial Intelligence, Bar-Ilan University, 2026', 'sub'),
        hr(),
        sp(4),
    ]

    # ----------------------------------------------------------
    # ABSTRACT
    # ----------------------------------------------------------
    story += [
        p('Abstract', 'abl'),
        p('Multi-Agent Path Finding (MAPF) is the problem of planning collision-free paths for '
          'k agents on a shared graph while minimizing the Sum of Costs (SOC). Optimal MAPF is '
          'NP-hard; joint-state-space A* becomes infeasible as state space grows '
          'as O(|V|<super>k</super>). We reproduce two central results from Sharon et al. (2015), '
          'who introduced Conflict-Based Search (CBS): a two-level algorithm that separates '
          'high-level conflict resolution from low-level single-agent planning via Time-Space A* '
          '(TSA*). We implement CBS independently in Python and reproduce: (1) success rate vs. '
          'agent count compared to Joint-State-Space A*, and (2) CT node expansion growth. '
          'Our extension evaluates CBS on warehouse maps with narrow corridors vs. open grids. '
          'CBS success drops from 100% at 4 agents to 60% at 20 agents; Joint A* fails completely '
          'beyond 6 agents. Warehouse maps reduce CBS success further from 64% to 28% at 20 '
          'agents, with 3.7x more CT node expansions.'),
        sp(4),
    ]

    # ----------------------------------------------------------
    # 1. INTRODUCTION
    # ----------------------------------------------------------
    story += [
        p('1. Introduction', 'h1'), hr(),
        p('MAPF arises in automated warehouses, airport traffic, and railway scheduling '
          '[Sharon et al., 2015]. The naive approach of searching the joint state space is '
          'infeasible: with k=10 agents and |V|=5 vertices, the state space reaches ~9.7 million '
          'nodes. Our experiments confirm this: Joint A* solves only 32% of 6-agent instances '
          'and 0% of 8-agent instances within 5 seconds. CBS avoids this explosion by maintaining '
          'a Constraint Tree (CT) that branches only on detected conflicts, replanning a single '
          'agent at each CT node using TSA*. We reproduce the two central results of Sharon et al. '
          '(2015) and extend the study by comparing open vs. warehouse map topology.'),
        sp(4),
    ]

    # ----------------------------------------------------------
    # 2. SELECTED PAPER DESCRIPTION
    # ----------------------------------------------------------
    story += [
        p('2. Selected Paper Description', 'h1'), hr(),
        p('2.1 Problem Formulation', 'h2'),
        p('MAPF is defined on graph G=(V,E) with k agents, each with start s<sub>i</sub> and '
          'goal g<sub>i</sub>. Agents move to an adjacent vertex or wait each timestep. A valid '
          'solution has no vertex conflicts (two agents at the same vertex at the same time) and '
          'no edge conflicts (agents swapping positions between two consecutive timesteps). '
          'Objective: minimize SOC = sum of individual path lengths |pi<sub>i</sub>|.'),
        p('2.2 Conflict Types', 'h2'),
        p('Sharon et al. (2015) identify five conflict types: (1) Vertex - same vertex, same '
          'time; (2) Edge - agents swap positions; (3) Following - agent follows another on the '
          'same edge; (4) Cycle - cyclic dependency; (5) Swapping - position exchange. We detect '
          'and resolve vertex and edge conflicts, which is sufficient for correctness and '
          'optimality on 4-connected grids.'),
        p('2.3 Why Joint A* Fails', 'h2'),
        p('The joint state space is O(|V|<super>k</super>). Even for k=10 agents on a small grid '
          'this is computationally infeasible. CBS avoids this by planning agents independently '
          'and resolving only conflicts that actually arise.'),
        p('2.4 CBS Algorithm', 'h2'),
        p('<b>Low level - TSA*:</b> State = (vertex v, timestep t). A vertex constraint (v, t) '
          'forbids agent i from being at vertex v at time t. An edge constraint forbids a '
          'directional move at time t. Heuristic = Manhattan distance (admissible on 4-connected '
          'grids). TSA* checks all future constraints at the goal before terminating to avoid '
          'premature stopping.'),
        p('<b>High level - CT:</b> Each CT node stores a constraint set per agent, TSA* paths, '
          'and total SOC. CBS proceeds as: (1) Root node - plan each agent independently with '
          'TSA*. (2) Find the first conflict among all agent pairs. (3) If no conflict, return '
          'the current paths as the optimal solution. (4) Branch - create two child CT nodes, '
          'one forbidding agent i from the conflict vertex/edge, the other forbidding agent j. '
          '(5) Replan the constrained agent with TSA*. (6) Push both children onto a min-heap '
          'ordered by SOC. Repeat from step 2. CBS is complete and optimal [Sharon et al., 2015].'),
        p('2.5 CBS Improvements (not implemented)', 'h2'),
        p('The paper also introduces Prioritizing Conflicts (cardinal conflicts first), CBS with '
          'Heuristics (admissible high-level heuristic), Disjoint Splitting (positive and '
          'negative constraints), and Conflict Reasoning. We implement basic CBS only; these '
          'improvements are acknowledged as future work.'),
        sp(4),
    ]

    # ----------------------------------------------------------
    # 3. PROJECT DESCRIPTION
    # ----------------------------------------------------------
    story += [
        p('3. Project Description', 'h1'), hr(),
        p('3.1 Implementation', 'h2'),
        p('We implemented CBS independently in Python 3.13 without using the original authors\' '
          'code. The implementation is organized in seven modules: <b>graph.py</b> - 4-connected '
          'Grid class with obstacle support; <b>tsa_star.py</b> - TSA* with constraint checking '
          'and future-constraint-aware goal detection; <b>conflict.py</b> - vertex and edge '
          'conflict detection and constraint generation; <b>cbs.py</b> - CTNode class, CBS main '
          'loop, and min-heap by SOC; <b>joint_astar.py</b> - true Joint-State-Space A* baseline '
          'matching the paper\'s intended comparison (not independent A*, which does not check '
          'conflicts); <b>benchmark.py</b> - map generators, random instance generator, and '
          'experiment runner with CSV output; <b>visualize.py</b> - matplotlib plots.'),
        p('3.2 Team Contributions', 'h2'),
        p('<b>Nimrod Netzer:</b> tsa_star.py (TSA* with constraint checking and future-constraint-'
          'aware goal detection). Wrote Abstract and Sections 1-2.', 'bul'),
        p('<b>Elad Damti:</b> conflict.py (conflict detection, constraint generation) and cbs.py '
          '(CTNode structure, CBS main loop). Wrote Sections 3-4.', 'bul'),
        p('<b>Kfir Dahan:</b> joint_astar.py, benchmark.py, visualize.py, all experiments. '
          'Wrote Sections 5-6, Reproducibility Statement, and AI Tools Disclosure.', 'bul'),
        p('All three members participated in integration testing, debugging, defense preparation, '
          'and the recorded video.'),
        p('3.3 Key Implementation Choices', 'h2'),
        p('<b>Baseline choice:</b> Joint-State-Space A* searches all agent positions '
          'simultaneously, matching the paper\'s intended baseline. Unlike independent A*, it '
          'produces conflict-free paths and correctly demonstrates the exponential blowup.', 'bul'),
        p('<b>Goal model:</b> Agents remain at their goal indefinitely; paths are padded to '
          'the maximum length for correct conflict checking.', 'bul'),
        p('<b>Conflict selection:</b> First conflict encountered when scanning by timestep and '
          'then by agent pair index (i, j) with i < j.', 'bul'),
        p('<b>Reproducibility:</b> Instance seed = 42 + n_agents * 1000 + instance_index. '
          'Map seed = 1. All experiments are deterministic.', 'bul'),
        sp(4),
    ]

    # ----------------------------------------------------------
    # 4. EXPERIMENTS
    # ----------------------------------------------------------
    story += [
        p('4. Experiments', 'h1'), hr(),
        p('4.1 Experimental Setup', 'h2'),
        p('<b>Hardware:</b> 12th Gen Intel Core i7-1255U, 10 cores @ 1.70 GHz, 16 GB RAM, '
          'Windows 11 Home.'),
        p('<b>Software:</b> Python 3.13; matplotlib 3.11; standard library only (heapq, '
          'collections, csv, json, time). No external MAPF libraries used.'),
        p('<b>Benchmark instances:</b> 20x20 grid maps generated procedurally. Open grid: '
          'random obstacles at ~10% density (map seed=1). Warehouse grid: alternating shelf rows '
          'with single-cell-wide corridors every 4 columns, simulating a real warehouse layout. '
          '25 random agent instances per agent count.'),
        p('<b>Algorithms compared:</b> (1) CBS as described in Section 3. (2) Joint-State-Space '
          'A* as the paper\'s baseline, searching the full joint configuration space.'),
        p('<b>Parameter settings:</b> CBS: first-found conflict selection, stay-at-goal model, '
          'max timestep = 200. Joint A*: admissible heuristic = sum of individual Manhattan '
          'distances.'),
        p('<b>Time limits:</b> 5s for Joint A* (reproduction); 30s for CBS (reproduction); 15s '
          'for CBS (extension). Instances exceeding the limit are counted as failures.'),
        p('<b>Memory limits:</b> No explicit cap; bounded by OS (16 GB RAM).'),
        p('<b>Number of runs:</b> 1 per instance (both algorithms are deterministic).'),
        p('<b>Random seeds:</b> Instance seed = 42 + n_agents * 1000 + instance_index. '
          'Map seed = 1.'),
        p('<b>Differences from original paper:</b> We use a smaller 20x20 grid (the paper uses '
          'larger Moving AI benchmarks); Python instead of C++ (~10-50x slower in wall-clock '
          'time); shorter time limits. These factors explain the earlier onset of failures '
          'compared to the paper\'s results.'),
        sp(4),
        p('4.2 Reproduced Results', 'h2'),
        p('Table 1 shows CBS vs. Joint A* on the open 20x20 grid across 8 agent counts. '
          'Joint A* collapses from 8 agents onward, confirming exponential state-space growth. '
          'CBS scales significantly better but begins timing out beyond 15 agents.'),
        sp(3),
    ]

    story.append(KeepTogether([
        mktbl([
            ['Agents', 'CBS Success', 'CBS Time (s)', 'CT Nodes', 'SOC', 'Joint A* Success'],
            ['4',  '100%', '0.0018', '1.7',   '56.8',  '100%'],
            ['6',  '92%',  '0.0045', '3.7',   '83.8',  '32%'],
            ['8',  '100%', '0.0078', '5.4',   '114.3', '0%'],
            ['10', '96%',  '0.0168', '12.7',  '132.6', '0%'],
            ['12', '96%',  '0.0719', '70.6',  '158.1', '0%'],
            ['15', '64%',  '0.5431', '334.3', '204.8', '0%'],
            ['18', '64%',  '0.3147', '251.3', '236.4', '0%'],
            ['20', '60%',  '1.0958', '716.3', '266.7', '0%'],
        ], [W_INNER / 6] * 6),
        Spacer(1, 3),
        p('Table 1: CBS vs. Joint-State-Space A* on open 20x20 grid. 25 instances per agent '
          'count. Joint A* time limit: 5s. CBS time limit: 30s. Means over successful instances.', 'cap'),
    ]))

    sp6 = sp(6)
    story.append(sp6)

    # Figures 1 + 2 side by side
    fig1 = os.path.join(RESULTS_DIR, 'fig1_success_rate.png')
    fig2 = os.path.join(RESULTS_DIR, 'fig2_runtime.png')
    fig3 = os.path.join(RESULTS_DIR, 'fig3_ct_nodes.png')
    fig4 = os.path.join(RESULTS_DIR, 'fig4_topology_success.png')

    if os.path.exists(fig1) and os.path.exists(fig2):
        story.append(KeepTogether([
            side_by_side(fig1, fig2, w_frac=0.49, h_frac=0.72),
            p('Figure 1 (left): CBS vs. Joint A* success rate vs. number of agents. '
              'Figure 2 (right): Mean CBS runtime on successfully solved instances.', 'cap'),
        ]))

    if os.path.exists(fig3):
        story.append(sp(5))
        story.append(KeepTogether([
            Image(fig3, width=W_INNER * 0.75, height=W_INNER * 0.44),
            p('Figure 3: Mean CT nodes expanded by CBS vs. number of agents on the open grid. '
              'CT nodes jump from 70.6 at 12 agents to 334.3 at 15 agents, reflecting CBS\'s '
              'exponential worst-case behavior consistent with Sharon et al. (2015).', 'cap'),
        ]))

    story += [
        sp(5),
        p('4.3 Extension: Map Topology Study', 'h2'),
        p('Research question: do warehouse maps with narrow bottleneck corridors create more '
          'conflicts, expand more CT nodes, and reduce CBS success rate compared to open grids?'),
        sp(3),
    ]

    story.append(KeepTogether([
        mktbl([
            ['Agents', 'Open Success', 'Open CT Nodes', 'Open Time (s)',
             'WH Success', 'WH CT Nodes', 'WH Time (s)'],
            ['4',  '100%', '1.7',    '0.0017', '100%', '3.9',    '0.0037'],
            ['6',  '92%',  '3.7',    '0.0044', '100%', '3.2',    '0.0031'],
            ['8',  '100%', '5.4',    '0.0071', '100%', '19.4',   '0.0148'],
            ['10', '96%',  '12.7',   '0.0135', '100%', '125.9',  '0.2617'],
            ['12', '100%', '131.7',  '0.3525', '96%',  '633.7',  '0.8381'],
            ['15', '72%',  '1047.1', '1.6304', '72%',  '655.3',  '0.5128'],
            ['18', '68%',  '920.1',  '0.9647', '36%',  '1845.1', '1.6920'],
            ['20', '64%',  '877.4',  '1.5390', '28%',  '3258.3', '3.1362'],
        ], [W_INNER / 7] * 7),
        Spacer(1, 3),
        p('Table 2: CBS performance on Open Grid vs. Warehouse Grid (WH). 25 instances per '
          'agent count. Time limit: 15s per instance. Means over successful instances.', 'cap'),
    ]))

    if os.path.exists(fig4):
        story.append(sp(5))
        story.append(KeepTogether([
            Image(fig4, width=W_INNER * 0.98, height=W_INNER * 0.46),
            p('Figure 4: CBS success rate (left) and CT nodes expanded (right) - '
              'Open Grid vs. Warehouse Grid. Warehouse maps create significantly more '
              'conflicts at high agent counts.', 'cap'),
        ]))

    story += [
        sp(4),
        p('At 20 agents, warehouse CBS success drops to 28% vs. 64% on open grids. CT nodes '
          'expand to 3,258 on warehouse maps vs. 877 on open grids (3.7x). Bottleneck corridors '
          'force agents onto the same cells, multiplying vertex conflicts and CT branching depth.'),
        sp(3),
    ]

    # ----------------------------------------------------------
    # 5. DISCUSSION
    # ----------------------------------------------------------
    story += [
        p('5. Discussion', 'h1'), hr(),
        p('5.1 Agreement with Original Paper', 'h2'),
        p('Our results are qualitatively consistent with Sharon et al. (2015): CBS achieves '
          'near-perfect success at low agent counts and degrades as agent count increases; '
          'Joint A* fails completely from 8 agents onward; CT nodes grow exponentially beyond '
          '12 agents. Quantitative differences are expected: our Python implementation is '
          '~10-50x slower than the original C++, we use a smaller 20x20 grid instead of Moving '
          'AI benchmark maps, and our time limits are shorter. These factors cause success rates '
          'to drop at lower agent counts than in the paper.'),
        p('5.2 Extension Findings', 'h2'),
        p('Warehouse maps confirm that bottleneck structure severely amplifies CBS difficulty. '
          'Agents sharing narrow corridor cells create cascading vertex conflicts: each CT branch '
          'forces a longer detour that generates new conflicts in adjacent corridors. At 20 agents, '
          'CBS expands 3,258 CT nodes on warehouse maps vs. 877 on open grids (3.7x increase). '
          'This confirms that CBS improvements - particularly conflict prioritization and '
          'high-level admissible heuristics - are especially valuable in structured warehouse '
          'environments.'),
        p('5.3 Limitations', 'h2'),
        p('Python is ~10-50x slower than C++, causing earlier timeouts than reported in the '
          'original paper. The 20x20 grid is smaller than the paper\'s benchmarks (e.g., '
          'Paris_1_256). We implemented basic CBS only; extensions such as Disjoint Splitting '
          'and CBS with Heuristics would extend the solvable range.'),
        sp(3),
    ]

    # ----------------------------------------------------------
    # 6. CONCLUSION
    # ----------------------------------------------------------
    story += [
        p('6. Conclusion', 'h1'), hr(),
        p('We implemented CBS from scratch in Python and successfully reproduced its two central '
          'results: (1) CBS success rate vs. agent count significantly outperforms Joint A*, '
          'which fails completely from 8 agents; (2) CT nodes grow exponentially beyond 12 agents. '
          'Our extension demonstrates that warehouse map topology reduces CBS success from 64% '
          'to 28% at 20 agents, with 3.7x more CT expansions, motivating the use of CBS '
          'improvements in structured environments. Future work should evaluate Prioritizing '
          'Conflicts and CBS with Heuristics specifically on warehouse-type maps.'),
        sp(3),
    ]

    # ----------------------------------------------------------
    # REPRODUCIBILITY STATEMENT
    # ----------------------------------------------------------
    story += [
        p('Reproducibility Statement', 'h1'), hr(),
        p('<b>Results reproduced:</b> (1) Success rate of CBS vs. Joint-State-Space A* as a '
          'function of agent count on an open grid map, corresponding to the success rate figures '
          'in Sharon et al. (2015). (2) Mean CT node expansion statistics and runtime on '
          'successfully solved instances.'),
        p('<b>Results not reproduced:</b> Experiments on Moving AI standard benchmark maps '
          '(e.g., Paris_1_256, den520d); comparisons to ICTS or other MAPF algorithms; CBS '
          'improvement variants (Prioritizing Conflicts, Disjoint Splitting, high-level '
          'heuristics).'),
        p('<b>Implementation basis:</b> New independent implementation in Python 3.13. The '
          'original authors\' code was not consulted or used at any stage.'),
        p('<b>Changes from original paper:</b> 20x20 procedurally generated grid vs. larger '
          'Moving AI benchmark maps; Python instead of C++ (~10-50x slower); time limits of '
          '5s (Joint A*) and 30s (CBS) vs. the paper\'s longer limits; randomly generated '
          'start/goal pairs instead of pre-defined benchmark instances.'),
        p('<b>Agreement with original:</b> Qualitative trends match: CBS scales far better than '
          'joint search, success rate degrades with agent count, CT nodes grow exponentially. '
          'Absolute numbers differ due to implementation language, grid size, and time limits.'),
        p('<b>Files included:</b> graph.py, tsa_star.py, conflict.py, cbs.py, joint_astar.py, '
          'benchmark.py, visualize.py, main.py; '
          'results/reproduce_open.csv, results/extension_open.csv, '
          'results/extension_warehouse.csv; results/fig1_success_rate.png, '
          'results/fig2_runtime.png, results/fig3_ct_nodes.png, '
          'results/fig4_topology_success.png.', 'bodyl'),
        p('<b>How to run (commands must be typed on one line each):</b>'),
        p('Step 1 - Install dependency:', 'body'),
        p('pip install matplotlib', 'code'),
        p('Step 2 - Run reproduction experiment (CBS vs. Joint A* on open grid):', 'body'),
        p('python main.py --mode reproduce --n-instances 25 --time-limit 30', 'code'),
        p('         --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        p('Step 3 - Run extension experiment (open grid vs. warehouse grid):', 'body'),
        p('python main.py --mode extension --n-instances 25 --time-limit 15', 'code'),
        p('         --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        sp(3),
    ]

    # ----------------------------------------------------------
    # AI TOOLS DISCLOSURE
    # ----------------------------------------------------------
    story += [
        p('AI Tools Disclosure', 'h1'), hr(),
        p('<b>Claude (Anthropic):</b> Used as a technical assistant for code optimization, '
          'syntax debugging, and editorial review of the documentation. All core algorithms '
          '(including TSA* and CBS) were conceptualized and implemented directly by the team. '
          'The team has thoroughly validated all project components and takes full responsibility '
          'for the integrity, originality, and performance of the final output.'),
    ]

    # ----------------------------------------------------------
    # PAGE BREAK - REFERENCES ON THEIR OWN PAGE (not counted)
    # ----------------------------------------------------------
    story.append(PageBreak())
    story += [
        p('References', 'h1'), hr(),
        sp(6),
        p('Sharon, G., Stern, R., Felner, A., and Sturtevant, N. R. (2015). Conflict-based '
          'search for optimal multi-agent pathfinding. <i>Artificial Intelligence</i>, 219, '
          '40-66. https://doi.org/10.1016/j.artint.2014.11.006', 'ref'),
        sp(4),
        p('Sturtevant, N. R. (2012). Benchmarks for grid-based pathfinding. '
          '<i>IEEE Transactions on Computational Intelligence and AI in Games</i>, '
          '4(2), 144-148.', 'ref'),
    ]

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'Report saved: {OUT_PATH}')


if __name__ == '__main__':
    build()
