"""
Main entry point for CBS MAPF experiments.

Usage examples:
  # Quick sanity check (3 agents, small grid)
  python main.py --mode demo

  # Reproduce paper results (success rate + runtime on open grid)
  python main.py --mode reproduce

  # Extension: map topology study (open vs warehouse)
  python main.py --mode extension

  # Single instance solve
  python main.py --mode solve --agents 5 --width 10 --height 10

Run python main.py --help for all options.
"""

import argparse
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
MAPS_DIR = os.path.join(BASE_DIR, 'maps')
INSTANCES_DIR = os.path.join(BASE_DIR, 'instances')

from graph import Grid
from cbs import cbs
from benchmark import (
    make_open_grid, make_warehouse_grid,
    generate_instance, run_experiment, save_results, save_map,
)
from visualize import (
    plot_success_rate, plot_runtime, plot_ct_nodes,
    plot_topology_comparison, animate_solution,
)


def mode_demo(args):
    """Quick demo: solve a small hand-crafted instance and print solution."""
    print("=== CBS Demo: 3 agents on 5x5 grid ===")
    grid = Grid(5, 5, obstacles=[(2, 2)])
    starts = [(0, 0), (4, 0), (0, 4)]
    goals  = [(4, 4), (0, 4), (4, 0)]

    print(f"Grid: {grid}")
    print(f"Starts: {starts}")
    print(f"Goals:  {goals}")
    print()

    result = cbs(grid, starts, goals, time_limit=30.0)

    if result['paths']:
        print(f"Solution found!")
        print(f"  Cost (SOC):        {result['cost']}")
        print(f"  CT nodes expanded: {result['ct_nodes']}")
        print(f"  Low-level calls:   {result['low_level_calls']}")
        print(f"  Time:              {result['time']:.4f}s")
        print()
        for i, path in enumerate(result['paths']):
            print(f"  Agent {i}: {path}")
    else:
        print("No solution found within time limit.")

    # Animate if matplotlib available
    try:
        if result['paths']:
            animate_solution(grid, result['paths'], starts, goals,
                             title="CBS Demo — 3 agents")
    except Exception as e:
        print(f"(Animation skipped: {e})")


def mode_solve(args):
    """Solve a single random instance and print result."""
    import random
    grid = make_open_grid(args.width, args.height, obstacle_pct=0.1, seed=args.seed)
    
    # generate_instance returns a dict now, we extract starts and goals
    inst = generate_instance(grid, args.agents, seed_base=args.seed)
    starts, goals = inst['starts'], inst['goals']

    print(f"Solving: {args.agents} agents on {args.width}x{args.height} open grid")
    result = cbs(grid, starts, goals, time_limit=args.time_limit)

    if result['paths']:
        print(f"SUCCESS | cost={result['cost']} | CT_nodes={result['ct_nodes']} "
              f"| time={result['time']:.3f}s")
        for i, p in enumerate(result['paths']):
            print(f"  Agent {i}: {p}")
    else:
        print(f"TIMEOUT/FAIL after {result['time']:.1f}s | CT_nodes={result.get('ct_nodes', 0)}")


def mode_reproduce(args):
    """
    Reproduce the two central results from Sharon et al. 2015:
      1. Success rate vs number of agents (CBS vs joint A* baseline)
      2. Runtime comparison on solved instances
    """
    print("=== Reproducing Sharon et al. 2015 Results ===")
    print(f"Map: {args.width}x{args.height} open grid, {args.obstacle_pct*100:.0f}% obstacles")
    print(f"Instances per agent count: {args.n_instances}")
    print(f"Time limit: {args.time_limit}s")
    print(f"Agent counts: {args.agent_counts}")
    print()

    grid = make_open_grid(args.width, args.height, obstacle_pct=args.obstacle_pct, seed=1)
    save_map(grid, os.path.join(MAPS_DIR, 'open_grid.map'))

    results = []
    for n_agents in args.agent_counts:
        instances = []
        for i in range(args.n_instances):
            inst = generate_instance(grid, n_agents, seed_base=args.seed + n_agents * 100 + i)
            inst['id'] = i
            instances.append(inst)
            
        res = run_experiment(grid, instances, time_limit=args.time_limit, run_baseline=True)
        results.extend(res)

    out_path = os.path.join(RESULTS_DIR, 'reproduce_open.csv')
    save_results(results, out_path)

    # Generate plots
    try:
        plot_success_rate(
            results,
            title='Success Rate vs Number of Agents (Open Grid)',
            out_path=os.path.join(RESULTS_DIR, 'fig1_success_rate.png'),
        )
        plot_runtime(
            results,
            title='Runtime vs Number of Agents (Open Grid)',
            out_path=os.path.join(RESULTS_DIR, 'fig2_runtime.png'),
        )
        plot_ct_nodes(
            results,
            title='CT Nodes Expanded vs Number of Agents (Open Grid)',
            out_path=os.path.join(RESULTS_DIR, 'fig3_ct_nodes.png'),
        )
        print("Plots saved to results/")
    except Exception as e:
        print(f"Plot error: {e}")


def mode_extension(args):
    """
    Extension: compare CBS performance on open grid vs warehouse grid.
    Research question: does map topology (bottlenecks) affect CBS?
    """
    print("=== Extension: Map Topology Study ===")
    print(f"Open grid vs Warehouse grid ({args.width}x{args.height})")
    print(f"Instances per agent count: {args.n_instances}")
    print(f"Time limit: {args.time_limit}s")
    print(f"Agent counts: {args.agent_counts}")
    print()

    open_grid = make_open_grid(args.width, args.height, obstacle_pct=0.1, seed=1)
    ware_grid = make_warehouse_grid(args.width, args.height, seed=1)

    save_map(open_grid, os.path.join(MAPS_DIR, 'open_grid.map'))
    save_map(ware_grid, os.path.join(MAPS_DIR, 'warehouse_grid.map'))

    print("Running on OPEN GRID...")
    results_open = []
    for n_agents in args.agent_counts:
        instances = []
        for i in range(args.n_instances):
            inst = generate_instance(open_grid, n_agents, seed_base=args.seed + n_agents * 100 + i)
            inst['id'] = i
            instances.append(inst)
        res = run_experiment(open_grid, instances, time_limit=args.time_limit, run_baseline=False)
        results_open.extend(res)
    
    save_results(results_open, os.path.join(RESULTS_DIR, 'extension_open.csv'))

    print("\nRunning on WAREHOUSE GRID...")
    results_ware = []
    for n_agents in args.agent_counts:
        instances = []
        for i in range(args.n_instances):
            inst = generate_instance(ware_grid, n_agents, seed_base=args.seed + n_agents * 100 + i)
            inst['id'] = i
            instances.append(inst)
        res = run_experiment(ware_grid, instances, time_limit=args.time_limit, run_baseline=False)
        results_ware.extend(res)
        
    save_results(results_ware, os.path.join(RESULTS_DIR, 'extension_warehouse.csv'))

    try:
        plot_topology_comparison(
            results_open, results_ware,
            out_path=os.path.join(RESULTS_DIR, 'fig4_topology_success.png'),
        )
        print("Topology comparison plot saved.")
    except Exception as e:
        print(f"Plot error: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description='CBS MAPF Experiments')
    parser.add_argument('--mode', choices=['demo', 'solve', 'reproduce', 'extension'],
                        default='demo')
    parser.add_argument('--agents', type=int, default=5)
    parser.add_argument('--width', type=int, default=20)
    parser.add_argument('--height', type=int, default=20)
    parser.add_argument('--obstacle-pct', type=float, default=0.1, dest='obstacle_pct')
    parser.add_argument('--n-instances', type=int, default=25, dest='n_instances')
    parser.add_argument('--time-limit', type=float, default=60.0, dest='time_limit')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument(
        '--agent-counts', type=int, nargs='+',
        default=[4, 6, 8, 10, 12, 15, 18, 20, 25, 30],
        dest='agent_counts',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(MAPS_DIR, exist_ok=True)
    os.makedirs(INSTANCES_DIR, exist_ok=True)

    if args.mode == 'demo':
        mode_demo(args)
    elif args.mode == 'solve':
        mode_solve(args)
    elif args.mode == 'reproduce':
        mode_reproduce(args)
    elif args.mode == 'extension':
        mode_extension(args)


if __name__ == '__main__':
    main()