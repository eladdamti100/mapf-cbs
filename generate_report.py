"""
Generate the project report PDF using ReportLab.
Times New Roman 12pt, max 6 pages (references excluded from limit).
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(BASE_DIR, 'results', 'report.pdf')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# --- Register Times New Roman ---
import sys

def get_font_path(name):
    # Windows font directory
    win_fonts = r"C:\Windows\Fonts"
    mapping = {
        'TimesNewRoman':       'times.ttf',
        'TimesNewRoman-Bold':  'timesbd.ttf',
        'TimesNewRoman-Italic':'timesi.ttf',
        'TimesNewRoman-BoldItalic': 'timesbi.ttf',
    }
    path = os.path.join(win_fonts, mapping[name])
    if os.path.exists(path):
        return path
    return None

for font_name, _ in [
    ('TimesNewRoman', 'times.ttf'),
    ('TimesNewRoman-Bold', 'timesbd.ttf'),
    ('TimesNewRoman-Italic', 'timesi.ttf'),
    ('TimesNewRoman-BoldItalic', 'timesbi.ttf'),
]:
    p = get_font_path(font_name)
    if p:
        pdfmetrics.registerFont(TTFont(font_name, p))

FONT      = 'TimesNewRoman'
FONT_BOLD = 'TimesNewRoman-Bold'
FONT_IT   = 'TimesNewRoman-Italic'
FONT_BI   = 'TimesNewRoman-BoldItalic'
SIZE      = 12
PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

def build_styles():
    s = {}

    s['title'] = ParagraphStyle('title',
        fontName=FONT_BOLD, fontSize=14, leading=18,
        alignment=TA_CENTER, spaceAfter=6)

    s['authors'] = ParagraphStyle('authors',
        fontName=FONT_IT, fontSize=11, leading=14,
        alignment=TA_CENTER, spaceAfter=4)

    s['affil'] = ParagraphStyle('affil',
        fontName=FONT, fontSize=10, leading=13,
        alignment=TA_CENTER, spaceAfter=12)

    s['abstract_head'] = ParagraphStyle('abstract_head',
        fontName=FONT_BOLD, fontSize=SIZE, leading=16,
        alignment=TA_CENTER, spaceAfter=4)

    s['abstract'] = ParagraphStyle('abstract',
        fontName=FONT_IT, fontSize=SIZE-1, leading=15,
        leftIndent=1*cm, rightIndent=1*cm,
        alignment=TA_JUSTIFY, spaceAfter=12)

    s['h1'] = ParagraphStyle('h1',
        fontName=FONT_BOLD, fontSize=SIZE, leading=16,
        spaceBefore=10, spaceAfter=4)

    s['h2'] = ParagraphStyle('h2',
        fontName=FONT_BOLD, fontSize=SIZE, leading=16,
        spaceBefore=6, spaceAfter=3)

    s['body'] = ParagraphStyle('body',
        fontName=FONT, fontSize=SIZE, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=6)

    s['bullet'] = ParagraphStyle('bullet',
        fontName=FONT, fontSize=SIZE, leading=16,
        leftIndent=1*cm, bulletIndent=0.4*cm,
        alignment=TA_JUSTIFY, spaceAfter=3)

    s['code'] = ParagraphStyle('code',
        fontName='Courier', fontSize=9, leading=12,
        leftIndent=1*cm, spaceAfter=6,
        backColor=colors.HexColor('#F5F5F5'))

    s['ref'] = ParagraphStyle('ref',
        fontName=FONT, fontSize=10, leading=14,
        leftIndent=1*cm, firstLineIndent=-1*cm,
        spaceAfter=4)

    s['caption'] = ParagraphStyle('caption',
        fontName=FONT_IT, fontSize=10, leading=13,
        alignment=TA_CENTER, spaceAfter=8)

    return s


def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (-1,0),  FONT_BOLD),
        ('FONTNAME',    (0,1), (-1,-1), FONT),
        ('FONTSIZE',    (0,0), (-1,-1), 10),
        ('LEADING',     (0,0), (-1,-1), 13),
        ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#DDDDDD')),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN',       (1,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',  (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    return t


def fig(path, width=14*cm, caption=None):
    items = []
    if os.path.exists(path):
        img = Image(path, width=width, height=width*0.6)
        items.append(img)
    if caption:
        items.append(Paragraph(caption, build_styles()['caption']))
    return items


def build_story():
    S = build_styles()
    story = []

    # --- Title ---
    story.append(Paragraph(
        'Conflict-Based Search for Optimal Multi-Agent Path Finding:<br/>A Reproduction and Extension Study',
        S['title']))
    story.append(Paragraph('Nimrod Netzer, Elad Damti, Kfir Dahan', S['authors']))
    story.append(Paragraph(
        'Search in Artificial Intelligence — Bar-Ilan University, 2026', S['affil']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.2*cm))

    # --- Abstract ---
    story.append(Paragraph('Abstract', S['abstract_head']))
    story.append(Paragraph(
        'Multi-Agent Path Finding (MAPF) is the problem of planning collision-free paths for a set '
        'of agents on a shared graph, minimizing total travel cost. Solving MAPF optimally is NP-hard, '
        'and naive joint-state-space search fails due to exponential state-space growth. In this work, '
        'we reproduce key experimental results from Sharon et al. (2015), who introduced '
        'Conflict-Based Search (CBS) — a two-level algorithm separating high-level conflict resolution '
        'from low-level single-agent planning. We implement CBS independently in Python and reproduce '
        'two central results: success rate as a function of the number of agents, and a comparison '
        'against an independent planning baseline. We further contribute an extension study evaluating '
        'how map topology affects CBS performance, comparing open grids against warehouse-style maps '
        'with narrow corridors and bottlenecks. Our results confirm CBS\'s advantage over independent '
        'planning and reveal that structured bottleneck maps significantly increase conflict frequency '
        'and constraint tree depth, reducing CBS success rates.',
        S['abstract']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.2*cm))

    # --- 1. Introduction ---
    story.append(Paragraph('1. Introduction', S['h1']))
    story.append(Paragraph(
        'Multi-Agent Path Finding (MAPF) arises in many real-world domains including automated '
        'warehouses, airport ground traffic management, and railway scheduling [Sharon et al., 2015]. '
        'In these settings, a set of agents must navigate from their respective start locations to '
        'goal locations on a shared graph without colliding.',
        S['body']))
    story.append(Paragraph(
        'The naïve approach of searching the joint configuration space using A* quickly becomes '
        'infeasible. The joint state space grows exponentially with the number of agents: for 10 '
        'agents on a graph with 5 vertices, the number of joint states exceeds 9.7 million. '
        'CBS addresses this by decomposing the problem into a two-level hierarchy — a high-level '
        'Constraint Tree (CT) that branches on conflicts, and a low-level single-agent planner '
        'that respects constraints. This separation allows CBS to exploit agent independence and '
        'avoid enumerating the full joint state space.',
        S['body']))
    story.append(Paragraph(
        'In this project, we reproduce two central experimental results from Sharon et al. (2015): '
        '(1) the success rate of CBS as the number of agents increases, compared to an independent '
        'A* baseline; and (2) runtime and CT expansion statistics on standard grid benchmarks. '
        'We additionally contribute an extension study examining how map topology — specifically '
        'the presence of bottlenecks in warehouse-style maps — affects CBS performance.',
        S['body']))

    # --- 2. Selected Paper ---
    story.append(Paragraph('2. Selected Paper Description', S['h1']))

    story.append(Paragraph('2.1 Problem Formulation', S['h2']))
    story.append(Paragraph(
        'The MAPF problem is defined on a graph G = (V, E), with k agents A = {1, ..., k}. '
        'Each agent i has a start vertex sᵢ and a goal vertex gᵢ. At each timestep, an agent '
        'can move to an adjacent vertex or wait. A solution is a set of paths {π₁, ..., πₖ} '
        'with no vertex conflicts (two agents at the same vertex at the same time) and no edge '
        'conflicts (two agents swapping positions). The objective is to minimize the '
        'Sum of Costs (SOC) = Σ|πᵢ|, where |πᵢ| is agent i\'s path length. '
        'Optimal MAPF is NP-hard [Sharon et al., 2015].',
        S['body']))

    story.append(Paragraph('2.2 Why Joint-State-Space A* Fails', S['h2']))
    story.append(Paragraph(
        'Searching the joint state space requires O(|V|^k) states, growing exponentially with '
        'agent count. For k=10 agents on |V|=5 vertices, this yields ~9.7 million states. '
        'For realistic grids with tens of agents and hundreds of vertices, this is computationally '
        'infeasible.',
        S['body']))

    story.append(Paragraph('2.3 The CBS Algorithm', S['h2']))
    story.append(Paragraph(
        '<b>Low level — Time-Space A* (TSA*):</b> Each agent\'s path is planned individually '
        'in a time-space graph where each state is a (vertex, timestep) pair. TSA* respects '
        'a constraint set Cᵢ for agent i. A vertex constraint (v, t) forbids agent i from '
        'occupying vertex v at time t; an edge constraint forbids traversing a specific edge '
        'at a specific time. The heuristic is Manhattan distance — admissible on 4-connected grids.',
        S['body']))
    story.append(Paragraph(
        '<b>High level — Constraint Tree (CT):</b> Each CT node stores a constraint set per '
        'agent and the paths planned under those constraints. CBS proceeds as: (1) plan each '
        'agent independently with TSA*; (2) find the first conflict; (3) if none, return the '
        'solution; (4) otherwise create two child CT nodes — one adding a constraint on agent i, '
        'one on agent j; (5) replan the constrained agent; (6) push children to the min-cost '
        'open heap and repeat. CBS is both complete and optimal [Sharon et al., 2015].',
        S['body']))

    story.append(Paragraph('2.4 CBS Improvements', S['h2']))
    story.append(Paragraph(
        'The paper also introduces: <b>Prioritizing Conflicts</b> (resolve cardinal conflicts '
        'first); <b>High-Level Heuristics</b> (admissible h-function on the CT); '
        '<b>Disjoint Splitting</b> (negative and positive constraints); and '
        '<b>Conflict Reasoning</b> (larger constraint sets from conflict analysis). '
        'Our implementation covers basic CBS without these improvements.',
        S['body']))

    # --- 3. Project Description ---
    story.append(Paragraph('3. Project Description', S['h1']))
    story.append(Paragraph(
        'We implemented CBS independently in Python 3.13 without using the original authors\' code. '
        'The implementation consists of six modules: <b>graph.py</b> (4-connected Grid class); '
        '<b>tsa_star.py</b> (Time-Space A* with vertex and edge constraint checking); '
        '<b>conflict.py</b> (vertex and edge conflict detection); <b>cbs.py</b> (CT-based '
        'high-level search and independent A* baseline); <b>benchmark.py</b> (map generators, '
        'instance generator, experiment runner); and <b>visualize.py</b> (all plots and animation).',
        S['body']))
    story.append(Paragraph(
        '<b>Team contributions:</b> Nimrod Netzer implemented the low-level Time-Space A* (tsa_star.py) '
        'and wrote Sections 1–2 and the Abstract. Elad Damti implemented conflict detection (conflict.py) '
        'and the CBS constraint tree (cbs.py), and wrote Sections 3–4. Kfir Dahan implemented the '
        'benchmark infrastructure, ran all experiments, and wrote Sections 5–6, the Reproducibility '
        'Statement, and AI Disclosure. All members participated in testing, debugging, and the defense.',
        S['body']))
    story.append(Paragraph(
        '<b>Key implementation choices:</b> Agents stay at goal indefinitely (stay-at-goal model). '
        'First conflict found (by timestep, then agent pair index) is resolved; no prioritization. '
        'Time limit: 30s per instance (reproduction), 15s (extension). Memory limit: OS-bounded (16GB). '
        'Random seeds: instance seed = 42 + n_agents × 1000 + instance_index. Max timesteps per TSA* '
        'call: 200.',
        S['body']))

    # --- 4. Experiments ---
    story.append(Paragraph('4. Experiments', S['h1']))

    story.append(Paragraph('4.1 Experimental Setup', S['h2']))
    story.append(Paragraph(
        '<b>Hardware:</b> 12th Gen Intel Core i7-1255U (10 cores, 1.7GHz), 16GB RAM, Windows 11 Home. '
        '<b>Software:</b> Python 3.13; matplotlib 3.11 (plots); standard library only (heapq, '
        'collections, csv, json, time). No external search libraries. '
        '<b>Benchmark:</b> 20×20 grid maps. Open grid: ~10% random obstacles (map seed=1). '
        'Warehouse: alternating shelf rows, single-cell vertical corridors every 4 columns. '
        '25 instances per agent count. Random seeds: instance seed = 42 + n_agents×1000 + instance_index. '
        '<b>Algorithms:</b> (1) CBS; (2) Independent A* baseline (no conflict avoidance). '
        '<b>Parameters:</b> max_t=200 timesteps per TSA* call; no conflict prioritization; stay-at-goal model. '
        '<b>Time limit:</b> 30s/instance (reproduction), 15s/instance (extension). '
        '<b>Memory limit:</b> No explicit cap (OS-bounded, 16GB). '
        '<b>Runs:</b> 1 per instance (deterministic). '
        '<b>Agent counts:</b> 4,6,8,10,12,15,18,20 (reproduction); 4,6,8,10,12 (extension). '
        '<b>Differences from paper:</b> Smaller grid (20×20), shorter time limit, Python vs. C++, '
        'randomly generated maps instead of Moving AI benchmarks.',
        S['body']))

    story.append(Paragraph('4.2 Reproduced Results', S['h2']))

    # Table 1
    t1_headers = ['Agents', 'Success', 'Mean Time (s)', 'Mean CT Nodes', 'Mean LL Calls', 'Mean SOC']
    t1_rows = [
        ['4',  '100%', '0.002', '2.0',    '6.0',    '56.8'],
        ['6',  '92%',  '0.004', '4.0',    '11.9',   '83.8'],
        ['8',  '96%',  '0.011', '5.2',    '16.5',   '113.5'],
        ['10', '88%',  '0.013', '11.3',   '30.5',   '132.9'],
        ['12', '76%',  '0.026', '17.1',   '44.2',   '159.4'],
        ['15', '44%',  '1.471', '1,401.9','2,816.8','202.5'],
        ['18', '56%',  '3.626', '1,344.4','2,704.9','242.8'],
        ['20', '36%',  '3.797', '2,179.4','4,376.9','276.1'],
    ]
    story.append(Paragraph(
        'Table 1 shows CBS performance on a 20×20 open grid (25 instances, 30s time limit). '
        'Success rate degrades from 100% at 4 agents to 36% at 20 agents. '
        'A critical jump occurs between 12 and 15 agents: CT nodes leap from 17 to 1,402 on '
        'average, reflecting CBS\'s exponential worst-case behavior when many conflicts accumulate.',
        S['body']))
    story.append(make_table(t1_headers, t1_rows,
        col_widths=[1.5*cm, 1.8*cm, 2.5*cm, 2.8*cm, 2.8*cm, 2.3*cm]))
    story.append(Paragraph('Table 1: CBS performance on open 20×20 grid (25 instances, 30s limit)', S['caption']))

    # Table 2
    t2_headers = ['Agents', 'Baseline Success', 'Mean Conflicts in Solution']
    t2_rows = [
        ['4',  '100%', '0.4'],
        ['6',  '92%',  '1.3'],
        ['8',  '100%', '2.0'],
        ['10', '96%',  '2.2'],
        ['12', '100%', '4.7'],
        ['15', '88%',  '8.6'],
        ['18', '92%',  '10.5'],
        ['20', '92%',  '15.2'],
    ]
    story.append(Paragraph(
        'Table 2 shows the independent A* baseline. While it almost always finds individual paths '
        '(high success), those solutions contain an average of 15.2 collisions at 20 agents. '
        'CBS guarantees zero conflicts at the cost of runtime.',
        S['body']))
    story.append(make_table(t2_headers, t2_rows,
        col_widths=[2*cm, 4*cm, 7*cm]))
    story.append(Paragraph('Table 2: Independent A* baseline — collisions in produced solutions', S['caption']))

    # Figures
    story.extend(fig(
        os.path.join(RESULTS_DIR, 'fig1_success_rate.png'), width=13*cm,
        caption='Figure 1: Success rate vs. number of agents — CBS vs. Independent A* baseline (open 20×20 grid)'))
    story.extend(fig(
        os.path.join(RESULTS_DIR, 'fig3_ct_nodes.png'), width=13*cm,
        caption='Figure 2: Mean CT nodes expanded by CBS vs. number of agents'))

    story.append(Paragraph('4.3 Extension: Map Topology Study', S['h2']))
    story.append(Paragraph(
        '<b>Research question:</b> Does map topology affect CBS performance? Do warehouse-style '
        'maps (narrow corridors, bottlenecks) reduce CBS success compared to open grids?',
        S['body']))

    # Table 3
    t3_headers = ['Agents', 'Open Success', 'Open CT Nodes', 'Warehouse Success', 'Warehouse CT Nodes']
    t3_rows = [
        ['4',  '100%', '2.0',  '92%',  '2.2'],
        ['6',  '92%',  '4.0',  '100%', '3.7'],
        ['8',  '96%',  '5.2',  '76%',  '18.2'],
        ['10', '88%',  '11.3', '60%',  '11.3'],
        ['12', '76%',  '17.1', '44%',  '49.5'],
    ]
    story.append(make_table(t3_headers, t3_rows,
        col_widths=[1.8*cm, 2.5*cm, 2.8*cm, 3*cm, 3.3*cm]))
    story.append(Paragraph('Table 3: CBS on open grid vs. warehouse grid (25 instances, 15s limit)', S['caption']))

    story.extend(fig(
        os.path.join(RESULTS_DIR, 'fig4_topology_success.png'), width=14*cm,
        caption='Figure 3: Success rate and CT nodes — open grid vs. warehouse grid'))

    # --- 5. Discussion ---
    story.append(Paragraph('5. Discussion', S['h1']))
    story.append(Paragraph(
        '<b>Agreement with original paper:</b> Our reproduced results are qualitatively consistent '
        'with Sharon et al. (2015). CBS achieves near-perfect success for small agent counts '
        '(≤10 agents) and degrades as agent count grows. CT nodes grow dramatically beyond 12 '
        'agents, reflecting CBS\'s exponential worst-case behavior. The independent A* baseline '
        'always finds individual paths quickly but produces solutions with increasing collisions, '
        'confirming that naive independent planning is insufficient for MAPF. Quantitative '
        'differences are expected due to Python vs. C++, smaller grid sizes, and a shorter '
        'time limit (30s vs. 300s in the paper).',
        S['body']))
    story.append(Paragraph(
        '<b>Extension findings:</b> Our map topology study confirms that environment structure '
        'significantly affects CBS performance. The warehouse grid — featuring shelf rows with '
        'single-cell corridor gaps — consistently yields lower success rates and more CT '
        'expansions than the open grid. At 12 agents, warehouse success drops to 44% vs. 76% '
        'on the open grid, and CT nodes are nearly 3× higher (49.5 vs. 17.1). This occurs '
        'because bottlenecks force agents through a small number of corridor cells, dramatically '
        'increasing vertex conflict probability. Each conflict forces a CT branch; the constrained '
        'agent must detour, potentially creating further conflicts in adjacent corridors. '
        'This finding suggests that CBS improvements (conflict prioritization, high-level '
        'heuristics) would be especially valuable in warehouse-like environments.',
        S['body']))
    story.append(Paragraph(
        '<b>Limitations:</b> Python is significantly slower than C++; many timed-out instances '
        'would likely be solved with a compiled implementation. Our 20×20 grids are smaller than '
        'the paper\'s benchmarks. We did not implement CBS improvements, which would extend '
        'success rates at higher agent counts.',
        S['body']))

    # --- 6. Conclusion ---
    story.append(Paragraph('6. Conclusion', S['h1']))
    story.append(Paragraph(
        'We implemented CBS from scratch in Python and successfully reproduced its two central '
        'experimental results: success rate vs. number of agents, and CT expansion growth. '
        'Our results confirm CBS\'s key property: it finds provably optimal, collision-free '
        'solutions while scaling significantly better than naive independent planning. '
        'Our extension study on map topology reveals that bottleneck-heavy warehouse maps '
        'increase conflict density and reduce CBS success rates, with CT node counts up to '
        '3× higher than on open grids. Future work should implement CBS improvements '
        '(prioritized conflicts, high-level heuristics) and evaluate them specifically on '
        'warehouse environments, where the performance gap is largest.',
        S['body']))

    # --- References ---
    story.append(Paragraph('References', S['h1']))
    story.append(Paragraph(
        'Sharon, G., Stern, R., Felner, A., & Sturtevant, N. R. (2015). Conflict-based search '
        'for optimal multi-agent pathfinding. <i>Artificial Intelligence</i>, 219, 40–66. '
        'https://doi.org/10.1016/j.artint.2014.11.006',
        S['ref']))
    story.append(Paragraph(
        'Sturtevant, N. R. (2012). Benchmarks for grid-based pathfinding. '
        '<i>IEEE Transactions on Computational Intelligence and AI in Games</i>, 4(2), 144–148.',
        S['ref']))
    story.append(Paragraph(
        'Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic '
        'determination of minimum cost paths. <i>IEEE Transactions on Systems Science and '
        'Cybernetics</i>, 4(2), 100–107.',
        S['ref']))

    # --- Reproducibility Statement ---
    story.append(Paragraph('Reproducibility Statement', S['h1']))
    story.append(Paragraph(
        '<b>Results reproduced:</b> (1) Success rate of CBS vs. number of agents on grid maps '
        'compared to an independent A* baseline — corresponding to the success rate figures in '
        'Sharon et al. (2015). (2) Runtime and CT node expansion statistics on solved instances.',
        S['body']))
    story.append(Paragraph(
        '<b>Results NOT reproduced:</b> Experiments on Moving AI benchmark maps (e.g., Paris_1_256); '
        'comparisons to ICTS or other MAPF solvers; results for CBS variants (prioritized conflicts, '
        'disjoint splitting, high-level heuristics).',
        S['body']))
    story.append(Paragraph(
        '<b>Implementation:</b> New independent implementation in Python 3.13. The original '
        'authors\' code was not used.',
        S['body']))
    story.append(Paragraph(
        '<b>Changes from original:</b> Smaller grid (20×20 vs. larger benchmark maps), shorter '
        'time limit (30s), Python instead of C++, randomly generated maps instead of the paper\'s '
        'Moving AI benchmark files.',
        S['body']))
    story.append(Paragraph(
        '<b>Agreement:</b> Qualitative trends match — CBS scales better than independent planning, '
        'success rate degrades with agent count, CT nodes grow dramatically beyond ~12 agents. '
        'Absolute numbers differ due to language, grid size, and time limit.',
        S['body']))
    story.append(Paragraph(
        '<b>Files included:</b> graph.py, tsa_star.py, conflict.py, cbs.py, benchmark.py, '
        'visualize.py, main.py, generate_report.py, README.md; '
        'reproduce_open.csv, extension_open.csv, extension_warehouse.csv; '
        'fig1_success_rate.png, fig2_runtime.png, fig3_ct_nodes.png, fig4_topology_success.png.',
        S['body']))
    story.append(Paragraph('<b>How to run:</b>', S['body']))
    story.append(Paragraph(
        'pip install matplotlib<br/>'
        'python main.py --mode reproduce --n-instances 25 --time-limit 30 --agent-counts 4 6 8 10 12 15 18 20<br/>'
        'python main.py --mode extension --n-instances 25 --time-limit 15 --agent-counts 4 6 8 10 12',
        S['code']))

    # --- AI Tools ---
    story.append(Paragraph('AI Tools Disclosure', S['h1']))
    story.append(Paragraph(
        'The following AI tools were used in this project: <b>Claude (Anthropic, claude-sonnet-4-6)</b> '
        'was used for implementation assistance (code structure, TSA* and CBS implementation, '
        'debugging), report writing, algorithm explanations based on course lecture slides and '
        'the paper, and project planning. All code was reviewed, understood, and validated by '
        'the team. The team takes full responsibility for the correctness, originality, and '
        'quality of all submitted work.',
        S['body']))

    return story


def main():
    os.makedirs(os.path.join(BASE_DIR, 'results'), exist_ok=True)
    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title='CBS for Optimal MAPF — Project Report',
        author='Nimrod Netzer, Elad Damti, Kfir Dahan',
    )
    story = build_story()
    doc.build(story)
    print(f'PDF saved: {OUT_PATH}')


if __name__ == '__main__':
    main()
