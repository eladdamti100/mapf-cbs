import time
import heapq
import itertools

class JointNode:
    def __init__(self, positions, g, h, parent=None):
        self.positions = positions
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def run_joint_astar(graph, starts, goals, time_limit=60.0):
    """
    True Joint-State A* Baseline.
    Moves all agents simultaneously to guarantee 0 collisions, 
    but suffers from exponential state space explosion.
    """
    t_start = time.time()
    k = len(starts)
    start_pos = tuple(starts)
    goal_pos = tuple(goals)

    def compute_h(positions):
        return sum(abs(positions[i][0] - goal_pos[i][0]) + abs(positions[i][1] - goal_pos[i][1]) for i in range(k))

    start_node = JointNode(start_pos, 0, compute_h(start_pos))
    open_list = [start_node]
    closed_set = set()

    while open_list:
        # Check timeout 
        if time.time() - t_start > time_limit:
            return {'success': False, 'time': time.time() - t_start, 'cost': None, 'num_conflicts': None}

        curr = heapq.heappop(open_list)

        if curr.positions == goal_pos:
            paths = [[] for _ in range(k)]
            node = curr
            while node:
                for i in range(k):
                    paths[i].append(node.positions[i])
                node = node.parent
            cost = sum(len(p) - 1 for p in paths)
            return {'success': True, 'time': time.time() - t_start, 'cost': cost, 'num_conflicts': 0}

        if curr.positions in closed_set:
            continue
        closed_set.add(curr.positions)

        agent_moves = [graph.neighbors(curr.positions[i]) for i in range(k)]

        # Generate all possible joint states (Cartesian product)
        for step_idx, joint_move in enumerate(itertools.product(*agent_moves)):
            
            # CRITICAL FIX: Check timeout INSIDE this massive combinatorial loop!
            # For >8 agents, itertools.product generates millions of states.
            # Without this inner check, it will hang for minutes/hours.
            if step_idx % 2000 == 0 and time.time() - t_start > time_limit:
                return {'success': False, 'time': time.time() - t_start, 'cost': None, 'num_conflicts': None}
                
            if len(set(joint_move)) < k:
                continue

            edge_conflict = False
            for a1 in range(k):
                for a2 in range(a1 + 1, k):
                    if joint_move[a1] == curr.positions[a2] and joint_move[a2] == curr.positions[a1]:
                        edge_conflict = True
                        break
                if edge_conflict: break

            if edge_conflict:
                continue

            if joint_move not in closed_set:
                h = compute_h(joint_move)
                heapq.heappush(open_list, JointNode(joint_move, curr.g + 1, h, curr))

    return {'success': False, 'time': time.time() - t_start, 'cost': None, 'num_conflicts': None}