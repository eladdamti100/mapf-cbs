"""
Visualization utilities for CBS MAPF experiments.

Produces:
  - Success rate vs number of agents (CBS vs baseline)
  - Runtime comparison
  - CT nodes expanded
  - Map topology comparison (open vs warehouse)
  - Grid animation of agent paths
"""

import os
import collections


def _agg_by_agents(results, key_success, key_metric=None):
    """
    Aggregate results by n_agents.
    Returns:
      agent_counts  : sorted list of agent counts
      success_rates : % success per agent count
      metric_means  : mean of key_metric for successful runs (or None)
    """
    from collections import defaultdict
    buckets = defaultdict(list)
    for row in results:
        buckets[int(row['n_agents'])].append(row)

    agent_counts = sorted(buckets.keys())
    success_rates = []
    metric_means = [] if key_metric else None

    for n in agent_counts:
        rows = buckets[n]
        successes = [r for r in rows if r[key_success] is True or r[key_success] == 'True']
        success_rates.append(100.0 * len(successes) / len(rows) if rows else 0.0)
        if key_metric and successes:
            vals = [float(r[key_metric]) for r in successes
                    if r[key_metric] not in (None, '', 'None')]
            metric_means.append(sum(vals) / len(vals) if vals else 0.0)
        elif key_metric:
            metric_means.append(0.0)

    return agent_counts, success_rates, metric_means


def plot_success_rate(results, title='Success Rate', out_path=None):
    import matplotlib.pyplot as plt

    cbs_counts, cbs_sr, _ = _agg_by_agents(results, 'cbs_success')

    has_baseline = any('baseline_success' in r for r in results)
    if has_baseline:
        bl_counts, bl_sr, _ = _agg_by_agents(results, 'baseline_success')

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(cbs_counts, cbs_sr, 'b-o', label='CBS', linewidth=2, markersize=6)
    if has_baseline:
        ax.plot(bl_counts, bl_sr, 'r--s', label='Independent A* (baseline)', linewidth=2, markersize=6)

    ax.set_xlabel('Number of Agents', fontsize=12)
    ax.set_ylabel('Success Rate (%)', fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.set_ylim(0, 105)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=150)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close()


def plot_runtime(results, title='Runtime Comparison', out_path=None):
    import matplotlib.pyplot as plt

    cbs_counts, _, cbs_rt = _agg_by_agents(results, 'cbs_success', 'cbs_time')

    has_baseline = any('baseline_success' in r for r in results)
    if has_baseline:
        bl_counts, _, bl_rt = _agg_by_agents(results, 'baseline_success', 'baseline_time')

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(cbs_counts, cbs_rt, 'b-o', label='CBS', linewidth=2, markersize=6)
    if has_baseline:
        ax.plot(bl_counts, bl_rt, 'r--s', label='Independent A* (baseline)', linewidth=2, markersize=6)

    ax.set_xlabel('Number of Agents', fontsize=12)
    ax.set_ylabel('Mean Runtime (s) on Solved Instances', fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=150)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close()


def plot_ct_nodes(results, title='CT Nodes Expanded', out_path=None):
    import matplotlib.pyplot as plt

    counts, _, ct_means = _agg_by_agents(results, 'cbs_success', 'cbs_ct_nodes')

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(counts, ct_means, 'g-^', label='CBS CT nodes expanded', linewidth=2, markersize=6)
    ax.set_xlabel('Number of Agents', fontsize=12)
    ax.set_ylabel('Mean CT Nodes Expanded', fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=150)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close()


def plot_topology_comparison(results_open, results_ware, out_path=None):
    import matplotlib.pyplot as plt

    open_counts, open_sr, open_ct = _agg_by_agents(results_open, 'cbs_success', 'cbs_ct_nodes')
    ware_counts, ware_sr, ware_ct = _agg_by_agents(results_ware, 'cbs_success', 'cbs_ct_nodes')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Success rate comparison
    axes[0].plot(open_counts, open_sr, 'b-o', label='Open Grid', linewidth=2, markersize=6)
    axes[0].plot(ware_counts, ware_sr, 'r--s', label='Warehouse Grid', linewidth=2, markersize=6)
    axes[0].set_xlabel('Number of Agents', fontsize=12)
    axes[0].set_ylabel('Success Rate (%)', fontsize=12)
    axes[0].set_title('Success Rate: Open vs Warehouse', fontsize=13)
    axes[0].set_ylim(0, 105)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)

    # CT nodes comparison
    axes[1].plot(open_counts, open_ct, 'b-o', label='Open Grid', linewidth=2, markersize=6)
    axes[1].plot(ware_counts, ware_ct, 'r--s', label='Warehouse Grid', linewidth=2, markersize=6)
    axes[1].set_xlabel('Number of Agents', fontsize=12)
    axes[1].set_ylabel('Mean CT Nodes Expanded', fontsize=12)
    axes[1].set_title('CT Nodes Expanded: Open vs Warehouse', fontsize=13)
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=150)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close()


def animate_solution(grid, paths, starts, goals, title='CBS Solution', out_path=None):
    """
    Animate agent paths on the grid using matplotlib.
    Each agent gets a distinct color.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation

    max_t = max(len(p) for p in paths)
    n_agents = len(paths)
    colors = plt.cm.tab10.colors

    fig, ax = plt.subplots(figsize=(7, 7))

    def draw_grid():
        ax.set_xlim(-0.5, grid.width - 0.5)
        ax.set_ylim(-0.5, grid.height - 0.5)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=12)
        ax.invert_yaxis()

        for (ox, oy) in grid.obstacles:
            rect = patches.Rectangle(
                (ox - 0.5, oy - 0.5), 1, 1,
                linewidth=0, facecolor='black', alpha=0.8,
            )
            ax.add_patch(rect)

        for i, (gx, gy) in enumerate(goals):
            ax.text(gx, gy, f'G{i}', ha='center', va='center',
                    fontsize=7, color=colors[i % len(colors)], fontweight='bold')

    draw_grid()
    agent_circles = []
    for i in range(n_agents):
        sx, sy = starts[i]
        circle = plt.Circle((sx, sy), 0.35, color=colors[i % len(colors)], zorder=3)
        ax.add_patch(circle)
        agent_circles.append(circle)

    time_text = ax.text(0.01, 0.99, 't=0', transform=ax.transAxes,
                        va='top', fontsize=10)

    def update(frame):
        t = frame
        for i, circle in enumerate(agent_circles):
            pos = paths[i][t] if t < len(paths[i]) else paths[i][-1]
            circle.center = (pos[0], pos[1])
        time_text.set_text(f't={t}')
        return agent_circles + [time_text]

    anim = FuncAnimation(fig, update, frames=max_t, interval=400, blit=True)

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        anim.save(out_path, writer='pillow', fps=2)
        print(f"Animation saved: {out_path}")
    else:
        plt.show()
    plt.close()


def print_grid(grid, paths=None, t=0):
    """Print a text snapshot of the grid at timestep t."""
    from conflict import get_pos

    agent_pos = {}
    if paths:
        for i, p in enumerate(paths):
            pos = get_pos(p, t)
            agent_pos[pos] = i

    for y in range(grid.height):
        row = ''
        for x in range(grid.width):
            v = (x, y)
            if v in grid.obstacles:
                row += '█'
            elif v in agent_pos:
                row += str(agent_pos[v])
            else:
                row += '.'
        print(row)
    print()
