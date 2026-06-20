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
from cbs import cbs
from joint_astar import run_joint_astar
from tsa_star import tsa_star


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
#IMPORTANT: DONT KNOW IF IT REALLY NEED IT!
def is_instance_solvable(grid, starts, goals):
    """
    Sanity check: Ensures that every individual agent has at least one valid 
    physical path to its goal (ignoring other agents).
    Prevents "0.0s fails" due to agents spawning inside obstacle cages.
    """
    for s, g in zip(starts, goals):
        path = tsa_star(grid, s, g, set(), max_t=200)
        if path is None:
            return False  # Agent is trapped, instance is fundamentally unsolvable
    return True

def generate_instance(grid, n_agents, seed_base=42):
    """
    Generate random start/goal pairs for n_agents on the given grid.
    Will keep trying different random seeds until a physically solvable 
    instance (no trapped agents) is found.
    """
    attempts = 0
    while attempts < 1000:
        current_seed = seed_base + attempts
        rng = random.Random(current_seed)
        free = grid.vertices()
        
        if len(free) < 2 * n_agents:
            raise ValueError("Not enough free cells for agents.")
            
        chosen = rng.sample(free, 2 * n_agents)
        starts = chosen[:n_agents]
        goals = chosen[n_agents:]
        
        # Check if this draw is actually solvable
        if is_instance_solvable(grid, starts, goals):
            return {'starts': starts, 'goals': goals, 'id': current_seed}
            
        attempts += 1
        
    raise RuntimeError("Could not find a solvable instance after 1000 attempts. Map might be too cluttered.")


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

def run_experiment(graph, instances, time_limit=60.0, run_baseline=True):
    """
    Runs experiments for both CBS and Joint A* and prints status to console.
    """
    results = []
    n_instances = len(instances)
    
    cbs_successes = 0
    cbs_total_time = 0.0
    cbs_total_nodes = 0
    
    ja_successes = 0
    ja_total_time = 0.0
    
    for idx, instance in enumerate(instances):
        n_agents = len(instance['starts'])
        
        print(f"  [Instance {idx+1:02d}/{n_instances}] Agents: {n_agents:2d} | CBS: ", end="", flush=True)
        
        # --- Run CBS ---
        cbs_start = time.time()
        cbs_result = cbs(graph=graph, starts=instance['starts'], goals=instance['goals'], time_limit=time_limit)
        cbs_time = time.time() - cbs_start
        cbs_success = cbs_result is not None and cbs_result.get('paths') is not None
        
        cbs_total_time += cbs_time
        if cbs_success:
            cbs_successes += 1
            nodes = cbs_result.get('ct_nodes', 0)
            cbs_total_nodes += nodes
            cbs_status = f"{cbs_successes}/{idx+1}"
        else:
            nodes = cbs_result.get('ct_nodes', 0) if cbs_result else 0
            cbs_status = "FAIL"

        print(f"{cbs_status} ({cbs_time:5.2f}s, {nodes:4d} nodes)", end="", flush=True)
            
        # --- Run Joint A* ---
        ja_success = False
        ja_time = 0.0
        bl_result = None
        
        if run_baseline:
            print(f" | Joint A*: ", end="", flush=True)
            ja_start = time.time()
            bl_result = run_joint_astar(graph, instance['starts'], instance['goals'], time_limit=time_limit)
            ja_time = time.time() - ja_start
            ja_success = bl_result is not None and bl_result.get('success', False)
            
            ja_total_time += ja_time
            if ja_success:
                ja_successes += 1
                ja_status = f"{ja_successes}/{idx+1}"
            else:
                ja_status = "FAIL"
            
            print(f"{ja_status} ({ja_time:5.2f}s)", end="", flush=True)
        
        print() # Newline at the end of the instance

        # Store result row
        row = {
            'n_agents': n_agents,
            'instance': idx,
            'cbs_success': cbs_success,
            'cbs_time': cbs_time,
            'cbs_cost': cbs_result['cost'] if cbs_success else None,
            'cbs_ct_nodes': cbs_result.get('ct_nodes') if cbs_success else None,
            'cbs_ll_calls': cbs_result.get('low_level_calls') if cbs_success else None,
            'baseline_success': ja_success,
            'baseline_time': ja_time,
            'baseline_cost': bl_result['cost'] if run_baseline and ja_success else None,
            'baseline_conflicts': 0 if run_baseline and ja_success else None,
        }
        results.append(row)

    # --- Summary Line ---
    if instances:
        n_agents = len(instances[0]['starts'])
        cbs_pct = (cbs_successes / n_instances) * 100
        
        print(f"  => n_agents= {n_agents:2d} | CBS success: {cbs_successes}/{n_instances} ({cbs_pct:.0f}%), Total Time: {cbs_total_time:.2f}s, Total Nodes: {cbs_total_nodes}")
        
        if run_baseline:
            ja_pct = (ja_successes / n_instances) * 100
            print(f"  => n_agents= {n_agents:2d} | Joint A* success: {ja_successes}/{n_instances} ({ja_pct:.0f}%), Total Time: {ja_total_time:.2f}s")
            
        print() 

    return results

def save_results(results, path):
    if not results:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

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