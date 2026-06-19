"""
Benchmark utilities for MAPF experiments.

Provides:
  - Map generators: open grid, warehouse grid
  - Instance generator: random start/goal pairs
  - Experiment runner: run CBS and baseline over many instances
  - Result saver: write CSV results
"""

import random
import csv
import os
import json
import time

from graph import Grid
from cbs import cbs, independent_astar


# ---------------------------------------------------------------------------
# Map generators
# ---------------------------------------------------------------------------

def make_open_grid(width=20, height=20, obstacle_pct=0.1, seed=None):
    """Random open grid with roughly obstacle_pct fraction of cells blocked."""
    rng = random.Random(seed)
    all_cells = [(x, y) for x in range(width) for y in range(height)]
    n_obs = int(len(all_cells) * obstacle_pct)
    obstacles = set(rng.sample(all_cells, n_obs))
    return Grid(width, height, obstacles)


def make_warehouse_grid(width=20, height=20, corridor_width=1, seed=None):
    """
    Warehouse-style grid: horizontal shelves (rows of obstacles) with
    narrow vertical corridors every few columns.

    Layout:
      - Shelves occupy alternating rows (rows 2,3, 6,7, 10,11, ...)
      - Corridors: every (corridor_width + shelf_width) columns, one column is free
    """
    obstacles = set()
    shelf_rows = []
    r = 2
    while r + 1 < height - 1:
        shelf_rows.extend([r, r + 1])
        r += 4  # gap of 2 free rows between shelves

    corridor_spacing = 4  # one free column every 4
    for y in shelf_rows:
        for x in range(width):
            # Leave a corridor every `corridor_spacing` columns
            if x % corridor_spacing != 0:
                obstacles.add((x, y))

    return Grid(width, height, obstacles)


def save_map(grid, path):
    """Save a grid to a simple text file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f"type octile\n")
        f.write(f"height {grid.height}\n")
        f.write(f"width {grid.width}\n")
        f.write("map\n")
        for y in range(grid.height):
            row = ''
            for x in range(grid.width):
                row += '@' if (x, y) in grid.obstacles else '.'
            f.write(row + '\n')


# ---------------------------------------------------------------------------
# Instance generator
# ---------------------------------------------------------------------------

def generate_instance(grid, n_agents, seed=None):
    """
    Generate random start/goal pairs for n_agents on the given grid.
    Starts and goals are all distinct vertices.
    Returns (starts, goals) or raises ValueError if not enough free cells.
    """
    rng = random.Random(seed)
    free = grid.vertices()
    if len(free) < 2 * n_agents:
        raise ValueError(
            f"Not enough free cells ({len(free)}) for {n_agents} agents "
            f"(need {2 * n_agents})"
        )
    chosen = rng.sample(free, 2 * n_agents)
    starts = chosen[:n_agents]
    goals = chosen[n_agents:]
    return starts, goals


def save_instance(starts, goals, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump({'starts': starts, 'goals': goals}, f)


def load_instance(path):
    with open(path, 'r') as f:
        d = json.load(f)
    starts = [tuple(s) for s in d['starts']]
    goals = [tuple(g) for g in d['goals']]
    return starts, goals


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------

def run_experiment(
    grid,
    agent_counts,
    n_instances=25,
    time_limit=60.0,
    seed_base=42,
    run_baseline=True,
    verbose=True,
):
    """
    For each agent count in agent_counts, generate n_instances random instances
    and run CBS (and optionally the independent A* baseline).

    Returns a list of result dicts, one per (agent_count, instance_index).
    """
    results = []

    for n_agents in agent_counts:
        cbs_successes = 0
        baseline_successes = 0

        for inst_idx in range(n_instances):
            seed = seed_base + n_agents * 1000 + inst_idx
            try:
                starts, goals = generate_instance(grid, n_agents, seed=seed)
            except ValueError as e:
                if verbose:
                    print(f"  [skip] n={n_agents} inst={inst_idx}: {e}")
                continue

            # Run CBS
            cbs_result = cbs(graph=grid, starts=starts, goals=goals, time_limit=time_limit)
            if cbs_result['success']:
                cbs_successes += 1

            row = {
                'n_agents': n_agents,
                'instance': inst_idx,
                'cbs_success': cbs_result['success'],
                'cbs_time': cbs_result['time'],
                'cbs_cost': cbs_result['cost'],
                'cbs_ct_nodes': cbs_result['ct_nodes'],
                'cbs_ll_calls': cbs_result['low_level_calls'],
            }

            # Run baseline
            if run_baseline:
                bl_result = independent_astar(
                    graph=grid, starts=starts, goals=goals, time_limit=time_limit
                )
                if bl_result['success']:
                    baseline_successes += 1
                row.update({
                    'baseline_success': bl_result['success'],
                    'baseline_time': bl_result['time'],
                    'baseline_cost': bl_result['cost'],
                    'baseline_conflicts': bl_result['num_conflicts'],
                })

            results.append(row)

        if verbose:
            pct = 100 * cbs_successes / n_instances
            print(f"  n_agents={n_agents:3d} | CBS success: {cbs_successes}/{n_instances} ({pct:.0f}%)")

    return results


def save_results(results, path):
    if not results:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {path}")


def load_results(path):
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Convert numeric fields
    numeric = {
        'n_agents', 'instance', 'cbs_time', 'cbs_cost', 'cbs_ct_nodes',
        'cbs_ll_calls', 'baseline_time', 'baseline_cost', 'baseline_conflicts'
    }
    bool_fields = {'cbs_success', 'baseline_success'}
    for row in rows:
        for k in list(row.keys()):
            if k in numeric and row[k] not in ('', 'None', None):
                try:
                    row[k] = float(row[k])
                except ValueError:
                    pass
            elif k in bool_fields:
                row[k] = row[k] == 'True'
    return rows
