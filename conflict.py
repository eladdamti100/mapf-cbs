"""
Conflict detection for MAPF.

A conflict is a tuple:
  ('vertex', agent_i, agent_j, vertex, timestep)
  ('edge',   agent_i, agent_j, v1, v2, timestep)   # agents swap: i goes v1->v2, j goes v2->v1

Paths are lists of vertices, indexed by timestep.
The path is padded implicitly: if t >= len(path), the agent stays at path[-1] (goal).
"""


def get_pos(path, t):
    """Return the vertex an agent occupies at timestep t (stays at goal after path ends)."""
    if t < len(path):
        return path[t]
    return path[-1]


def find_first_conflict(paths):
    """
    Scan all agent pairs and return the first conflict found, or None.

    Returns a conflict tuple:
      ('vertex', i, j, vertex, t)
      ('edge',   i, j, v1, v2, t)   where agent i moves v1->v2 and agent j moves v2->v1
    """
    n = len(paths)
    if n == 0:
        return None

    max_t = max(len(p) for p in paths) + 1  # +1 to catch goal conflicts

    for t in range(max_t):
        for i in range(n):
            for j in range(i + 1, n):
                vi = get_pos(paths[i], t)
                vj = get_pos(paths[j], t)

                # Vertex conflict
                if vi == vj:
                    return ('vertex', i, j, vi, t)

                # Edge conflict (swap): agent i: vi->vi_next, agent j: vj->vj_next
                if t + 1 < max_t:
                    vi_next = get_pos(paths[i], t + 1)
                    vj_next = get_pos(paths[j], t + 1)
                    if vi == vj_next and vj == vi_next:
                        return ('edge', i, j, vi, vj, t)

    return None


def find_all_conflicts(paths):
    """Return a list of all conflicts (used for analysis/reporting)."""
    conflicts = []
    n = len(paths)
    if n == 0:
        return conflicts

    max_t = max(len(p) for p in paths) + 1

    for t in range(max_t):
        for i in range(n):
            for j in range(i + 1, n):
                vi = get_pos(paths[i], t)
                vj = get_pos(paths[j], t)

                if vi == vj:
                    conflicts.append(('vertex', i, j, vi, t))

                if t + 1 < max_t:
                    vi_next = get_pos(paths[i], t + 1)
                    vj_next = get_pos(paths[j], t + 1)
                    if vi == vj_next and vj == vi_next:
                        conflicts.append(('edge', i, j, vi, vj, t))

    return conflicts


def make_constraints_from_conflict(conflict):
    """
    Given a conflict, return two constraint sets (one per branch of the CT).

    Returns: (constraints_for_agent_i, constraints_for_agent_j)
    Each constraint set is a set of (agent, constraint_obj) tuples where
    constraint_obj is either (vertex, t) for vertex constraints
    or frozenset({(v1,t),(v2,t+1)}) for edge constraints.
    """
    kind = conflict[0]

    if kind == 'vertex':
        _, i, j, vertex, t = conflict
        c_i = (i, (vertex, t))   # agent i cannot be at vertex at time t
        c_j = (j, (vertex, t))   # agent j cannot be at vertex at time t
        return c_i, c_j

    elif kind == 'edge':
        _, i, j, v1, v2, t = conflict
        # Agent i moves v1->v2 at time t->t+1
        edge_i = frozenset({(v1, t), (v2, t + 1)})
        c_i = (i, edge_i)
        # Agent j moves v2->v1 at time t->t+1
        edge_j = frozenset({(v2, t), (v1, t + 1)})
        c_j = (j, edge_j)
        return c_i, c_j

    raise ValueError(f"Unknown conflict type: {kind}")
