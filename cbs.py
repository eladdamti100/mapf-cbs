"""
Conflict-Based Search (CBS) — high-level search.

Implements the CBS algorithm from:
  Sharon et al. (2015). Conflict-Based Search for Optimal Multi-Agent Pathfinding.
  Artificial Intelligence, 219, 40-66.

The high-level search maintains a Constraint Tree (CT).
Each CT node stores:
  - constraints: dict mapping agent_id -> set of constraint objects
  - paths:       dict mapping agent_id -> list of vertices
  - cost:        sum of individual path lengths (SOC)

The CT is searched with best-first search (min cost).
On each expansion, the first conflict is found and the node is split
into two children, each adding one constraint.
"""

import heapq
import time

from conflict import find_first_conflict, make_constraints_from_conflict, find_all_conflicts
from tsa_star import tsa_star


class CTNode:
    """A node in the Constraint Tree."""
    _counter = 0  # tie-breaking counter for heap

    def __init__(self, constraints, paths):
        """
        constraints : dict {agent_id: set of constraint objects}
        paths       : dict {agent_id: list of vertices}
        """
        self.constraints = constraints
        self.paths = paths
        self.cost = sum(len(p) - 1 for p in paths.values())  # SOC
        CTNode._counter += 1
        self._id = CTNode._counter

    def __lt__(self, other):
        return (self.cost, self._id) < (other.cost, other._id)


def cbs(graph, starts, goals, time_limit=60.0):
    """
    Run CBS on the given MAPF instance.

    Parameters
    ----------
    graph      : Grid instance
    starts     : list of (x,y) start positions, one per agent
    goals      : list of (x,y) goal positions, one per agent
    time_limit : max wall-clock seconds before giving up

    Returns
    -------
    dict with keys:
      'paths'         : list of paths (list of vertices) or None if timeout
      'cost'          : SOC of solution, or None
      'ct_nodes'      : number of CT nodes expanded
      'low_level_calls': number of TSA* calls made
      'success'       : bool
      'time'          : elapsed seconds
      'num_conflicts' : total conflicts in final solution (0 if success)
    """
    CTNode._counter = 0
    t_start = time.time()
    n_agents = len(starts)
    ct_nodes_expanded = 0
    low_level_calls = 0

    def get_constraints_for_agent(constraints, agent):
        return constraints.get(agent, set())

    def plan_path(agent, constraints):
        nonlocal low_level_calls
        low_level_calls += 1
        c_set = get_constraints_for_agent(constraints, agent)
        return tsa_star(graph, starts[agent], goals[agent], c_set)

    # --- Root node ---
    root_constraints = {i: set() for i in range(n_agents)}
    root_paths = {}
    for i in range(n_agents):
        p = plan_path(i, root_constraints)
        if p is None:
            return _fail_result(ct_nodes_expanded, low_level_calls, time.time() - t_start)
        root_paths[i] = p

    root = CTNode(root_constraints, root_paths)
    open_heap = [root]

    while open_heap:
        if time.time() - t_start > time_limit:
            return _fail_result(ct_nodes_expanded, low_level_calls, time.time() - t_start)

        node = heapq.heappop(open_heap)
        ct_nodes_expanded += 1

        paths_list = [node.paths[i] for i in range(n_agents)]
        conflict = find_first_conflict(paths_list)

        if conflict is None:
            # Solution found
            elapsed = time.time() - t_start
            all_conflicts = find_all_conflicts(paths_list)
            return {
                'paths': paths_list,
                'cost': node.cost,
                'ct_nodes': ct_nodes_expanded,
                'low_level_calls': low_level_calls,
                'success': True,
                'time': elapsed,
                'num_conflicts': len(all_conflicts),
            }

        # Branch on conflict: create two child CT nodes
        c_i, c_j = make_constraints_from_conflict(conflict)

        for (agent, new_constraint) in [c_i, c_j]:
            # Copy constraints and add the new one
            new_constraints = {a: set(s) for a, s in node.constraints.items()}
            new_constraints[agent].add(new_constraint)

            # Replan only the constrained agent
            new_path = plan_path(agent, new_constraints)
            if new_path is None:
                continue  # This branch is infeasible, skip

            new_paths = dict(node.paths)
            new_paths[agent] = new_path

            child = CTNode(new_constraints, new_paths)
            heapq.heappush(open_heap, child)

    return _fail_result(ct_nodes_expanded, low_level_calls, time.time() - t_start)


def _fail_result(ct_nodes, ll_calls, elapsed):
    return {
        'paths': None,
        'cost': None,
        'ct_nodes': ct_nodes,
        'low_level_calls': ll_calls,
        'success': False,
        'time': elapsed,
        'num_conflicts': None,
    }


def independent_astar(graph, starts, goals, time_limit=60.0):
    """
    Baseline: plan each agent independently with single-agent A* (no time dimension,
    no conflict avoidance). Returns paths and SOC, always succeeds if individual
    paths exist. Used as comparison baseline.
    """
    from tsa_star import tsa_star
    t_start = time.time()
    paths = []
    for i, (s, g) in enumerate(zip(starts, goals)):
        if time.time() - t_start > time_limit:
            return _fail_result(0, i, time.time() - t_start)
        p = tsa_star(graph, s, g, set())
        if p is None:
            return _fail_result(0, i + 1, time.time() - t_start)
        paths.append(p)

    cost = sum(len(p) - 1 for p in paths)
    from conflict import find_all_conflicts
    all_conflicts = find_all_conflicts(paths)
    return {
        'paths': paths,
        'cost': cost,
        'ct_nodes': 0,
        'low_level_calls': len(starts),
        'success': True,
        'time': time.time() - t_start,
        'num_conflicts': len(all_conflicts),
    }
