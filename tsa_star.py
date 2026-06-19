"""
Time-Space A* (TSA*) — low-level search for CBS.

State: (vertex, timestep)
Constraints: set of (vertex, timestep) pairs the agent must avoid,
             plus edge constraints as frozensets {(v1,t), (v2,t+1)}.

Returns the shortest path (list of vertices) for one agent respecting
its constraint set C, or None if no path exists within max_t steps.
"""

import heapq


def heuristic(v, goal):
    """Manhattan distance — admissible on 4-connected grids."""
    return abs(v[0] - goal[0]) + abs(v[1] - goal[1])


def tsa_star(graph, start, goal, constraints, max_t=200):
    """
    Parameters
    ----------
    graph       : Grid instance
    start       : (x, y) start vertex
    goal        : (x, y) goal vertex
    constraints : set of (vertex, timestep) tuples for vertex constraints
                  AND frozenset({(v_from, t), (v_to, t+1)}) for edge constraints
    max_t       : hard cap on timesteps to prevent infinite loops

    Returns
    -------
    List of vertices [(x,y), ...] from start to goal (length = makespan+1),
    or None if no path found.
    """
    # Separate vertex and edge constraints for fast lookup
    vertex_constraints = set()   # (vertex, t)
    edge_constraints = set()     # frozenset({(v1,t1),(v2,t2)})

    for c in constraints:
        if isinstance(c, frozenset):
            edge_constraints.add(c)
        else:
            vertex_constraints.add(c)

    # Handle trivial case: start == goal with no constraint at t=0
    if start == goal and (start, 0) not in vertex_constraints:
        return [start]

    # open heap: (f, g, vertex, timestep)
    h0 = heuristic(start, goal)
    open_heap = [(h0, 0, start, 0)]
    # came_from[(vertex, t)] = (prev_vertex, prev_t)
    came_from = {}
    g_score = {(start, 0): 0}
    # Track expanded states to avoid re-expanding
    closed = set()

    while open_heap:
        f, g, v, t = heapq.heappop(open_heap)

        if (v, t) in closed:
            continue
        closed.add((v, t))

        if v == goal:
            # Reconstruct path (list of vertices)
            path = []
            cur = (v, t)
            while cur in came_from:
                path.append(cur[0])
                cur = came_from[cur]
            path.append(start)
            path.reverse()
            return path

        if t >= max_t:
            continue

        for nb in graph.neighbors(v):
            nt = t + 1

            # Check vertex constraint
            if (nb, nt) in vertex_constraints:
                continue

            # Check edge constraint (swap conflict)
            edge = frozenset({(v, t), (nb, nt)})
            if edge in edge_constraints:
                continue

            new_g = g + 1
            if (nb, nt) not in g_score or new_g < g_score[(nb, nt)]:
                g_score[(nb, nt)] = new_g
                came_from[(nb, nt)] = (v, t)
                f_new = new_g + heuristic(nb, goal)
                heapq.heappush(open_heap, (f_new, new_g, nb, nt))

    return None  # no path found
