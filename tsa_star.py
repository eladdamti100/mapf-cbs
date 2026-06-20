"""
Time-Space A* (TSA*) — low-level search for CBS.

State: (vertex, timestep)
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
    constraints : set of constraints.
                  Format: ('vertex', vertex, t) OR ('edge', from_v, to_v, t)
    max_t       : hard cap on timesteps to prevent infinite loops

    Returns
    -------
    List of vertices [(x,y), ...] from start to goal, or None if no path found.
    """
    vertex_constraints = set()   
    edge_constraints = set()     

    for c in constraints:
        kind = c[0]
        if kind == 'vertex':
            _, v, t = c
            vertex_constraints.add((v, t))
        elif kind == 'edge':
            _, u, v, t = c
            edge_constraints.add((u, v, t))

    # Trivial case: already at goal and no constraints force us to leave
    if start == goal and (start, 0) not in vertex_constraints:
        return [start]

    # open heap: (f, g, vertex, timestep)
    h0 = heuristic(start, goal)
    open_heap = [(h0, 0, start, 0)]
    came_from = {}
    g_score = {(start, 0): 0}
    closed = set()

    while open_heap:
        f, g, v, t = heapq.heappop(open_heap)

        if (v, t) in closed:
            continue
        closed.add((v, t))

        if v == goal:
            # FIX: Only stop at the goal if there are NO future constraints forcing us to move.
            future_constraints = [c_time for (c_vertex, c_time) in vertex_constraints 
                                  if c_vertex == goal and c_time > t]
            
            if not future_constraints:
                # Safe to rest here forever. Reconstruct path.
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

            # Check directional edge constraint
            if (v, nb, t) in edge_constraints:
                continue

            new_g = g + 1
            if (nb, nt) not in g_score or new_g < g_score[(nb, nt)]:
                g_score[(nb, nt)] = new_g
                came_from[(nb, nt)] = (v, t)
                f_new = new_g + heuristic(nb, goal)
                heapq.heappush(open_heap, (f_new, new_g, nb, nt))

    return None