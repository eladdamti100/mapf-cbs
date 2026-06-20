"""Generate PDF report - exactly 6 pages + page 7 references only."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
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
    """Canvas that adds page numbers at the bottom of each page."""
    def __init__(self, *args, **kwargs):
        pdfcanvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont('Times-Roman', 10)
        self.setFillColor(colors.HexColor('#555555'))
        self.drawCentredString(W / 2, 0.8 * cm, f'{self._pageNumber}')

def S():
    s = {}
    s['title']  = ParagraphStyle('title',  fontName='Times-Bold',   fontSize=13, leading=17, alignment=TA_CENTER, spaceAfter=2)
    s['sub']    = ParagraphStyle('sub',    fontName='Times-Roman',  fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=1)
    s['h1']     = ParagraphStyle('h1',     fontName='Times-Bold',   fontSize=12, leading=15, spaceBefore=7, spaceAfter=2, alignment=TA_LEFT)
    s['h2']     = ParagraphStyle('h2',     fontName='Times-Bold',   fontSize=12, leading=15, spaceBefore=5, spaceAfter=1, alignment=TA_LEFT)
    s['body']   = ParagraphStyle('body',   fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=4, alignment=TA_JUSTIFY)
    s['bul']    = ParagraphStyle('bul',    fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=2, alignment=TA_JUSTIFY, leftIndent=12, firstLineIndent=-10)
    s['cap']    = ParagraphStyle('cap',    fontName='Times-Italic', fontSize=9,  leading=12, alignment=TA_CENTER, spaceAfter=3)
    s['code']   = ParagraphStyle('code',   fontName='Courier',      fontSize=8,  leading=11, leftIndent=10, spaceAfter=2)
    s['abl']    = ParagraphStyle('abl',    fontName='Times-Bold',   fontSize=12, leading=15, alignment=TA_CENTER, spaceAfter=2)
    s['ref']    = ParagraphStyle('ref',    fontName='Times-Roman',  fontSize=12, leading=15, spaceAfter=4, alignment=TA_JUSTIFY, leftIndent=16, firstLineIndent=-16)
    return s

TS = TableStyle([
    ('BACKGROUND',    (0,0),(-1,0), colors.HexColor('#1a1a1a')),
    ('TEXTCOLOR',     (0,0),(-1,0), colors.white),
    ('FONTNAME',      (0,0),(-1,0), 'Times-Bold'),
    ('FONTSIZE',      (0,0),(-1,-1), 9),
    ('FONTNAME',      (0,1),(-1,-1), 'Times-Roman'),
    ('GRID',          (0,0),(-1,-1), 0.4, colors.HexColor('#999')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, colors.HexColor('#f2f2f2')]),
    ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 2),
    ('BOTTOMPADDING', (0,0),(-1,-1), 2),
    ('LEFTPADDING',   (0,0),(-1,-1), 3),
    ('RIGHTPADDING',  (0,0),(-1,-1), 3),
])

def mktbl(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TS)
    return t

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=colors.black, spaceAfter=2, spaceBefore=2)

def build():
    s = S()
    doc = SimpleDocTemplate(
        OUT_PATH, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title='CBS for Optimal MAPF',
        author='Nimrod Netzer, Elad Damti, Kfir Dahan',
    )
    story = []
    def p(t, st='body'): return Paragraph(t, s[st])
    def sp(n=3):         return Spacer(1, n)

    # =========================================================
    # PAGE 1 - Title + Abstract + Intro + Paper Description start
    # =========================================================
    story += [
        sp(2),
        p('Conflict-Based Search for Optimal Multi-Agent Path Finding', 'title'),
        p('A Reproduction and Extension Study', 'sub'),
        sp(2), hr(),
        p('Nimrod Netzer | Elad Damti | Kfir Dahan', 'sub'),
        p('Search in Artificial Intelligence, Bar-Ilan University, 2026', 'sub'),
        hr(), sp(4),
        p('Abstract', 'abl'), sp(2),
        p('Multi-Agent Path Finding (MAPF) is the problem of planning collision-free paths for '
          'k agents on a shared graph while minimizing total travel cost. Solving MAPF optimally '
          'is NP-hard, and joint-state-space A* fails due to exponential state-space growth. We '
          'reproduce key results from Sharon et al. (2015), who introduced Conflict-Based Search '
          '(CBS), a two-level algorithm separating high-level conflict resolution from low-level '
          'single-agent planning. We implement CBS independently in Python, reproduce two central '
          'results (success rate vs. agent count and runtime vs. Joint-State-Space A*), and '
          'contribute an extension comparing open grids against warehouse maps with bottlenecks. '
          'CBS success drops from 100% at 4 agents to 60% at 20 agents while Joint A* fails '
          'completely from 8 agents onward. Warehouse maps reduce CBS success further, from 64% '
          'to 28% at 20 agents, with 3.7x more CT node expansions.'),
        sp(5),
        p('1. Introduction', 'h1'), hr(),
        p('MAPF arises in automated warehouses, airport traffic, and railway scheduling '
          '[Sharon et al., 2015]. The naive approach of joint-state-space A* is infeasible: '
          'state space grows as O(|V|<super>k</super>), reaching ~9.7 million states for '
          'k=10 agents on |V|=5 vertices. Our experiments confirm this: Joint A* succeeds '
          'on only 32% of 6-agent instances and 0% of 8-agent instances within 5 seconds. '
          'CBS solves this via a Constraint Tree (CT) that branches on conflicts and a '
          'low-level Time-Space A* (TSA*) that plans paths per agent subject to constraints. '
          'We reproduce two results from Sharon et al. (2015) and study how map topology '
          'affects CBS performance.'),
        sp(5),
        p('2. Selected Paper Description', 'h1'), hr(),
        p('2.1 Problem Formulation', 'h2'),
        p('MAPF is defined on graph G=(V,E) with k agents, each with start s<sub>i</sub> and '
          'goal g<sub>i</sub>. Agents move or wait each timestep. A valid solution has no '
          'vertex conflicts (same vertex, same time) or edge conflicts (agents swap positions). '
          'Objective: minimize SOC = sum of |pi<sub>i</sub>| for all agents.'),
        p('2.2 Conflict Types', 'h2'),
        p('Sharon et al. (2015) identify five conflict types: (1) Vertex: same vertex, same '
          'time. (2) Edge: agents swap positions. (3) Following: one agent follows another '
          'on the same edge. (4) Cycle: cyclic dependency. (5) Swapping: position exchange. '
          'We detect and resolve vertex and edge conflicts, sufficient for correctness and optimality.'),
        p('2.3 Why Joint A* Fails', 'h2'),
        p('The joint state space is O(|V|<super>k</super>). For k=30 agents on a realistic '
          'map, exhaustive joint search is infeasible. CBS avoids this by planning agents '
          'independently and resolving only actual conflicts.'),
        p('2.4 CBS Algorithm', 'h2'),
        p('<b>Low level - TSA*:</b> State = (vertex v, timestep t). Vertex constraint (v,t) '
          'forbids occupying v at t. Edge constraint forbids a directional move at t. '
          'Heuristic = Manhattan distance (admissible on 4-connected grids). '
          'TSA* checks future constraints at the goal before terminating.'),
        p('<b>High level - CT:</b> Binary tree; each node stores constraints per agent, TSA* '
          'paths, and SOC. CBS: (1) Root: plan each agent independently. (2) Find first '
          'conflict. (3) If none, return optimal solution. (4) Branch: left child constrains '
          'agent i, right child constrains agent j. (5) Replan constrained agent. (6) Push '
          'both children to min-heap by SOC. Repeat. CBS is complete and optimal [Sharon et al., 2015].'),
        p('2.5 CBS Improvements', 'h2'),
        p('The paper introduces: Prioritizing Conflicts (cardinal conflicts first), CBS with '
          'Heuristics (high-level admissible heuristic), Disjoint Splitting (positive and '
          'negative constraints), and Conflict Reasoning. We implement basic CBS only.'),
    ]

    # =========================================================
    # PAGE 2 - Project Description + Experiments Setup
    # =========================================================
    story += [
        sp(5),
        p('3. Project Description', 'h1'), hr(),
        p('3.1 Implementation', 'h2'),
        p('We implemented CBS independently in Python 3.13 without the original authors\' code, '
          'across seven modules: <b>graph.py</b> (4-connected Grid with obstacles); '
          '<b>tsa_star.py</b> (TSA* with constraint checking and future-constraint-aware goal '
          'detection); <b>conflict.py</b> (vertex and edge conflict detection); '
          '<b>cbs.py</b> (CT, CTNode structure, CBS main loop, min-heap by SOC); '
          '<b>joint_astar.py</b> (true Joint-State-Space A* baseline matching the paper\'s '
          'intended comparison); <b>benchmark.py</b> (map generators, instance generator, '
          'experiment runner); <b>visualize.py</b> (matplotlib plots).'),
        p('3.2 Team Contributions', 'h2'),
        p('<b>Nimrod Netzer:</b> tsa_star.py (TSA*, constraint checking, goal detection). Abstract, Sections 1-2.', 'bul'),
        p('<b>Elad Damti:</b> conflict.py and cbs.py (CTNode, CBS loop). Sections 3-4.', 'bul'),
        p('<b>Kfir Dahan:</b> joint_astar.py, benchmark.py, visualize.py. All experiments. Sections 5-6, Reproducibility, AI Disclosure.', 'bul'),
        p('All three members participated in testing, debugging, defense preparation, and the video.'),
        p('3.3 Key Implementation Choices', 'h2'),
        p('<b>Baseline:</b> Joint-State-Space A* (joint_astar.py) searches all agent positions '
          'simultaneously, matching the paper\'s intended comparison. Unlike independent A*, it '
          'guarantees conflict-free solutions.', 'bul'),
        p('<b>Goal model:</b> Agents stay at goal indefinitely; paths padded for conflict checking.', 'bul'),
        p('<b>Conflict selection:</b> First conflict found by timestep then agent pair index.', 'bul'),
        p('<b>Seeds:</b> Instance seed = 42 + n_agents x 1000 + instance_index. Deterministic.', 'bul'),
        sp(5),
        p('4. Experiments', 'h1'), hr(),
        p('4.1 Experimental Setup', 'h2'),
        p('<b>Hardware:</b> 12th Gen Intel Core i7-1255U, 10 cores, 1.70 GHz, 16 GB RAM, Windows 11 Home.'),
        p('<b>Software:</b> Python 3.13; matplotlib 3.11; standard library only (heapq, collections, csv, json, time). No external MAPF libraries.'),
        p('<b>Benchmark instances:</b> 20x20 grid maps generated randomly. Open grid: ~10% obstacle density (seed=1). Warehouse grid: alternating shelf rows with single-cell corridors every 4 columns. 25 random instances per agent count.'),
        p('<b>Algorithms:</b> (1) CBS as described in Section 3. '
          '(2) Joint-State-Space A* as the paper\'s baseline.'),
        p('<b>Parameter settings:</b> CBS: first-found conflict, stay-at-goal model, max_t=200. '
          'Joint A*: admissible heuristic = sum of Manhattan distances.'),
        p('<b>Time limits:</b> 5s for Joint A* (reproduction); 30s for CBS (reproduction); 15s for CBS (extension). Exceeded instances counted as failures.'),
        p('<b>Memory limits:</b> No explicit cap; bounded by OS (16 GB).'),
        p('<b>Number of runs:</b> 1 per instance (deterministic algorithm).'),
        p('<b>Random seeds:</b> Instance seed = 42 + n_agents x 1000 + instance_index. Map seed = 1.'),
        p('<b>Differences from paper:</b> 20x20 grid (smaller than paper benchmarks); Python instead of C++ (~10-50x slower); shorter time limits. These explain earlier success rate drops.'),
    ]

    # =========================================================
    # PAGE 3 - Table 1 + Figures 1-2
    # =========================================================
    story += [
        sp(4),
        p('4.2 Reproduced Results', 'h2'),
        p('Table 1 shows CBS vs. Joint A* on the open 20x20 grid. Joint A* collapses from '
          '8 agents onward, confirming exponential state-space explosion. CBS scales '
          'significantly better but begins timing out beyond 15 agents.'),
        sp(3),
        mktbl([
            ['Agents','CBS Success','CBS Time (s)','CT Nodes','SOC','Joint A* Success'],
            ['4','100%','0.0018','1.7','56.8','100%'],
            ['6','92%','0.0045','3.7','83.8','32%'],
            ['8','100%','0.0078','5.4','114.3','0%'],
            ['10','96%','0.0168','12.7','132.6','0%'],
            ['12','96%','0.0719','70.6','158.1','0%'],
            ['15','64%','0.5431','334.3','204.8','0%'],
            ['18','64%','0.3147','251.3','236.4','0%'],
            ['20','60%','1.0958','716.3','266.7','0%'],
        ], [W_INNER/6]*6),
        p('Table 1: CBS vs. Joint-State-Space A* on open 20x20 grid. 25 instances per count. '
          'Joint A* limit: 5s. CBS limit: 30s. Means over successful instances.', 'cap'),
        sp(3),
    ]

    # Figures 1 and 2 side by side
    fig1 = os.path.join(RESULTS_DIR, 'fig1_success_rate.png')
    fig2 = os.path.join(RESULTS_DIR, 'fig2_runtime.png')
    if os.path.exists(fig1) and os.path.exists(fig2):
        img_w = W_INNER * 0.485
        img_h = img_w * 0.62
        row = [[Image(fig1, width=img_w, height=img_h),
                Image(fig2, width=img_w, height=img_h)]]
        t = Table(row, colWidths=[img_w, img_w])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                ('LEFTPADDING',(0,0),(-1,-1),2),
                                ('RIGHTPADDING',(0,0),(-1,-1),2)]))
        story.append(t)
        story.append(p('Figure 1 (left): Success rate vs. agents. Figure 2 (right): Mean CBS runtime on solved instances.', 'cap'))
        story.append(sp(3))

    fig3 = os.path.join(RESULTS_DIR, 'fig3_ct_nodes.png')
    if os.path.exists(fig3):
        story.append(Image(fig3, width=W_INNER * 0.62, height=W_INNER * 0.38))
        story.append(p('Figure 3: Mean CT nodes expanded vs. number of agents.', 'cap'))
        story.append(sp(3))

    story += [
        p('CT nodes jump from 70.6 at 12 agents to 334.3 at 15 agents, reflecting CBS\'s '
          'exponential worst-case behavior consistent with Sharon et al. (2015).'),
    ]

    # =========================================================
    # PAGE 4 - Extension results
    # =========================================================
    story += [
        sp(5),
        p('4.3 Extension Results - Map Topology Study', 'h2'),
        p('Research question: Do warehouse maps with narrow corridors create more conflicts '
          'and reduce CBS success compared to open grids?'),
        sp(3),
        mktbl([
            ['Agents','Open Success','Open CT Nodes','Open Time (s)','WH Success','WH CT Nodes','WH Time (s)'],
            ['4','100%','1.7','0.0017','100%','3.9','0.0037'],
            ['6','92%','3.7','0.0044','100%','3.2','0.0031'],
            ['8','100%','5.4','0.0071','100%','19.4','0.0148'],
            ['10','96%','12.7','0.0135','100%','125.9','0.2617'],
            ['12','100%','131.7','0.3525','96%','633.7','0.8381'],
            ['15','72%','1047.1','1.6304','72%','655.3','0.5128'],
            ['18','68%','920.1','0.9647','36%','1845.1','1.6920'],
            ['20','64%','877.4','1.5390','28%','3258.3','3.1362'],
        ], [W_INNER/7]*7),
        p('Table 2: CBS on Open vs. Warehouse Grid (WH). 25 instances per count. Time limit: 15s.', 'cap'),
        sp(3),
    ]

    fig4 = os.path.join(RESULTS_DIR, 'fig4_topology_success.png')
    if os.path.exists(fig4):
        story.append(Image(fig4, width=W_INNER * 0.80, height=W_INNER * 0.44))
        story.append(p('Figure 4: CBS success rate - Open Grid vs. Warehouse Grid.', 'cap'))
        story.append(sp(3))

    story += [
        p('Warehouse maps dramatically underperform at high agent counts: 20 agents - '
          'Open 64% vs. Warehouse 28%. CT nodes at 20 agents: 877 (open) vs. 3,258 (warehouse, 3.7x). '
          'Bottlenecks force agents into the same corridor cells, multiplying conflicts and CT branches.'),
    ]

    # =========================================================
    # PAGE 5 - Discussion + Conclusion
    # =========================================================
    story += [
        sp(5),
        p('5. Discussion', 'h1'), hr(),
        p('5.1 Agreement with Original Paper', 'h2'),
        p('Results are qualitatively consistent with Sharon et al. (2015): CBS achieves '
          'near-perfect success for small agent counts and degrades as agents increase; '
          'Joint A* fails completely from 8 agents; CT nodes grow exponentially beyond 12 agents. '
          'Quantitative differences are expected due to Python vs. C++, smaller 20x20 grid, '
          'and shorter time limits.'),
        p('5.2 Extension Findings', 'h2'),
        p('Warehouse maps confirm that bottleneck structure severely impacts CBS. Agents must '
          'share narrow corridor cells, creating vertex conflicts that cascade: each CT branch '
          'forces a longer detour, generating new conflicts in adjacent corridors. At 20 agents, '
          'CBS expands 3,258 CT nodes on warehouse maps vs. 877 on open grids (3.7x). '
          'This confirms that CBS improvements - conflict prioritization and high-level heuristics '
          '- are especially needed in warehouse environments.'),
        p('5.3 Limitations', 'h2'),
        p('Python is ~10-50x slower than C++, causing earlier timeouts. The 20x20 grid is '
          'smaller than the paper\'s benchmarks. We implemented basic CBS only, without the '
          'improvements that would extend the solvable agent range.'),
        sp(5),
        p('6. Conclusion', 'h1'), hr(),
        p('We implemented CBS from scratch in Python and reproduced its two central results. '
          'CBS finds provably optimal, collision-free solutions while scaling far better than '
          'Joint A*, which fails completely from 8 agents. Our extension shows warehouse '
          'bottlenecks reduce CBS success from 64% to 28% at 20 agents, with 3.7x more CT '
          'expansions. Future work should apply CBS improvements specifically to warehouse '
          'environments where the performance gap is largest.'),
    ]

    # =========================================================
    # PAGE 6 - Reproducibility Statement + AI Tools Disclosure
    # =========================================================
    story += [
        sp(5),
        p('Reproducibility Statement', 'h1'), hr(),
        p('<b>Results reproduced:</b> (1) Success rate of CBS vs. Joint-State-Space A* as a '
          'function of agent count on grid maps, corresponding to the success rate figures in '
          'Sharon et al. (2015). (2) Runtime and CT node expansion statistics on solved instances.'),
        p('<b>Results not reproduced:</b> Experiments on Moving AI benchmark maps (e.g., '
          'Paris_1_256); comparisons to ICTS or other MAPF algorithms; CBS improvement variants '
          '(prioritized conflicts, disjoint splitting, high-level heuristics).'),
        p('<b>Implementation basis:</b> New independent implementation in Python 3.13. The '
          'original authors\' code was not used at any stage.'),
        p('<b>Changes from original paper:</b> 20x20 grid vs. larger benchmarks; Python instead '
          'of C++; time limits of 5s (Joint A*) and 30s (CBS) vs. the paper\'s longer limits; '
          'randomly generated maps instead of paper benchmark files.'),
        p('<b>Agreement with original:</b> Qualitative trends match: CBS scales better than '
          'joint search, success degrades with agent count, CT nodes grow exponentially beyond '
          '~12 agents. Absolute numbers differ due to language, grid size, and time limits.'),
        p('<b>Files included:</b> graph.py, tsa_star.py, conflict.py, cbs.py, joint_astar.py, '
          'benchmark.py, visualize.py, main.py, generate_report.py; '
          'results/reproduce_open.csv, results/extension_open.csv, '
          'results/extension_warehouse.csv; results/fig1-fig4.png; results/report.pdf.'),
        p('<b>How to run:</b>'),
        p('pip install matplotlib', 'code'),
        p('python main.py --mode reproduce --n-instances 25 --time-limit 30 --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        p('python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12 15 18 20', 'code'),
        sp(5),
        p('AI Tools Disclosure', 'h1'), hr(),
        p('<b>Claude (Anthropic):</b> Used as a technical assistant for code optimization, '
          'syntax debugging, and editorial review of the documentation.'),
        sp(3),
        p('All core algorithms (including TSA* and CBS) were conceptualized and implemented '
          'directly by the team. The team has thoroughly validated all project components and '
          'takes full responsibility for the integrity, originality, and performance of the '
          'final output.'),
    ]

    # =========================================================
    # PAGE 7 - References ONLY (not counted in 6-page limit)
    # =========================================================
    story.append(PageBreak())
    story += [
        p('References', 'h1'), hr(), sp(4),
        p('Sharon, G., Stern, R., Felner, A., and Sturtevant, N. R. (2015). Conflict-based '
          'search for optimal multi-agent pathfinding. <i>Artificial Intelligence</i>, 219, '
          '40-66. https://doi.org/10.1016/j.artint.2014.11.006', 'ref'),
        p('Sturtevant, N. R. (2012). Benchmarks for grid-based pathfinding. '
          '<i>IEEE Transactions on Computational Intelligence and AI in Games</i>, '
          '4(2), 144-148.', 'ref'),
    ]

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'Report saved: {OUT_PATH}')

if __name__ == '__main__':
    build()
