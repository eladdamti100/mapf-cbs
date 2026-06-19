# Video Script — CBS for Optimal Multi-Agent Pathfinding
## Bar-Ilan University | Search in AI Course | Team: Nimrod Netzer, Elad Damti, Kfir Dahan
## Total Duration: ~8 minutes

---

## SLIDE 1 — Title Slide
**[Nimrod — 0:00–0:20]**

> "Hello, we are Nimrod Netzer, Elad Damti, and Kfir Dahan from Bar-Ilan University.
> In this video we present our project on Conflict-Based Search for Optimal Multi-Agent Pathfinding,
> based on the 2015 paper by Sharon, Stern, Felner, and Sturtevant, published in the journal Artificial Intelligence."

---

## SLIDE 2 — What is MAPF?
**[Nimrod — 0:20–1:10]**

> "Imagine a warehouse with dozens of robots that all need to move from their starting positions
> to their target positions — without crashing into each other.
>
> This is the Multi-Agent Path Finding problem, or MAPF.
> Formally: we have a graph, k agents, each with a start and a goal.
> Agents move one step per timestep, or they can wait.
> The objective is to minimize the Sum of Costs — the total number of steps taken by all agents.
>
> MAPF is used in real-world applications like Amazon warehouse robots, airport ground traffic,
> railway scheduling, and video game AI."

---

## SLIDE 3 — Why is MAPF Hard?
**[Nimrod — 1:10–1:55]**

> "The obvious approach is to search the joint state space of all agents together.
> But the joint space explodes exponentially.
>
> With just 10 agents on a 5×5 grid, the state space has nearly 10 million nodes.
> For 30 agents on a realistic map — it's completely infeasible.
>
> Joint A-star runs out of memory before it can even find a solution.
> We need a smarter algorithm."

---

## SLIDE 4 — Conflict Types
**[Nimrod — 1:55–2:30]**

> "Before we explain CBS, let's define what a conflict is.
>
> A vertex conflict happens when two agents are at the same location at the same timestep.
> An edge conflict — also called a swap conflict — happens when two agents cross the same
> edge in opposite directions between two consecutive timesteps.
>
> There are also following conflicts, cycle conflicts, and swapping conflicts.
> CBS detects these conflicts and resolves them one at a time."

---

## SLIDE 5 — CBS Overview
**[Elad — 2:30–3:00]**

> "Conflict-Based Search, or CBS, is a two-level algorithm.
>
> At the high level, CBS builds a Constraint Tree — a binary tree where each node
> represents a set of constraints imposed on the agents.
> CBS searches this tree using best-first search, always expanding the node with the lowest total cost.
>
> At the low level, for each CT node, each agent is planned independently using
> Time-Space A-star, respecting its own constraint set."

---

## SLIDE 6 — Time-Space A* (Low Level)
**[Elad — 3:00–3:40]**

> "Time-Space A-star is the low-level solver.
> Unlike regular A-star, the state includes both the vertex AND the timestep.
> So the state is the pair (vertex v, time t).
>
> A constraint says: agent i cannot be at vertex v at time t.
> Before expanding any state, we check if it violates any constraint.
> The heuristic is Manhattan distance to the goal — which is admissible, so TSA-star is optimal.
>
> This means each agent gets the shortest possible path that doesn't break its constraints."

---

## SLIDE 7 — CBS High Level (CT Branching)
**[Elad — 3:40–4:30]**

> "Here's how the high level works, step by step.
>
> First, CBS plans each agent independently — this is the root of the Constraint Tree.
> Then it scans all agent pairs for the first conflict.
> If there's no conflict, we're done — we found an optimal solution.
>
> If there is a conflict — say agents i and j both visit vertex v at time t —
> CBS creates two child nodes.
> In the left child, agent i is forbidden from vertex v at time t.
> In the right child, agent j is forbidden.
> Both children replan the constrained agent with TSA-star.
>
> CBS picks the cheapest child and repeats.
> Because it searches best-first by total cost, and TSA-star is optimal,
> the first complete solution CBS finds is guaranteed to be globally optimal."

---

## SLIDE 8 — Our Implementation
**[Elad — 4:30–5:00]**

> "We implemented CBS from scratch in Python 3.
>
> The code is split into modules: graph.py for the grid, tsa_star.py for the low-level search,
> conflict.py for detecting vertex and edge conflicts, cbs.py for the high-level constraint tree,
> and benchmark.py for running experiments.
>
> The work was split: Nimrod implemented TSA-star, I implemented the conflict detection and CBS tree,
> and Kfir built the experiment runner and the extension."

---

## SLIDE 9 — Reproduction Results
**[Kfir — 5:00–5:50]**

> "For Stage 3, we reproduced the main result from the Sharon et al. paper:
> success rate as a function of the number of agents.
>
> We ran CBS and our independent A-star baseline on a 20 by 20 open grid with 10% random obstacles.
> We tested 8 agent counts from 4 to 20, with 25 random instances each, and a 30-second time limit.
>
> The result matches the paper's trend: CBS succeeds in 100% of 4-agent cases,
> and success drops as agents increase — reaching 36% at 20 agents as the problems get harder.
>
> The baseline always 'succeeds' because it ignores conflicts — but as we show,
> it produces paths with many collisions. CBS produces conflict-free, optimal paths."

---

## SLIDE 10 — Extension: Map Topology
**[Kfir — 5:50–6:50]**

> "For our extension, we asked: does map topology affect CBS performance?
>
> We compared two map types: an open grid with 10% random obstacles,
> and a warehouse grid — a structured map with shelf rows and narrow corridors,
> designed to simulate a real warehouse environment.
>
> We ran CBS on both maps with 5 agent counts from 4 to 12, and 25 instances each.
>
> The results are clear: the warehouse map is significantly harder for CBS.
> Success rate drops faster, runtime is higher, and the Constraint Tree expands more nodes.
>
> Why? Because narrow corridors force agents onto the same paths, creating more conflicts.
> More conflicts means more CT branching, deeper trees, and exponentially more search work."

---

## SLIDE 11 — Key Findings
**[Kfir — 6:50–7:30]**

> "To summarize our findings:
>
> First — CBS works. It finds optimal, conflict-free solutions and scales much better than joint A-star.
>
> Second — map topology matters. Warehouse-style maps create structural bottlenecks that
> dramatically reduce CBS performance — this is a practical insight for real robot deployments.
>
> Third — our implementation is correct and efficient. Even in Python, CBS solves
> 4-agent problems in under 1 millisecond, and handles 12-agent warehouse problems within 15 seconds.
>
> The main limitation is scalability: beyond 20 agents, even CBS starts timing out —
> motivating the CBS improvements described in the paper, like conflict prioritization and heuristics."

---

## SLIDE 12 — Conclusion
**[Nimrod — 7:30–8:00]**

> "In this project we studied, implemented, and extended the Conflict-Based Search algorithm
> for optimal Multi-Agent Path Finding.
>
> CBS elegantly avoids the exponential joint state space by separating planning per agent
> and only resolving actual conflicts when they appear.
>
> Our extension showed that real-world map structure — like warehouse corridors —
> significantly impacts CBS performance, which is a practically important finding
> for warehouse robotics applications.
>
> Thank you for watching. We are Nimrod, Elad, and Kfir — ready for the defense."

---

## TIMING SUMMARY

| Slide | Speaker | Duration | Cumulative |
|-------|---------|----------|------------|
| 1 Title | Nimrod | 0:20 | 0:20 |
| 2 What is MAPF | Nimrod | 0:50 | 1:10 |
| 3 Why Hard | Nimrod | 0:45 | 1:55 |
| 4 Conflict Types | Nimrod | 0:35 | 2:30 |
| 5 CBS Overview | Elad | 0:30 | 3:00 |
| 6 TSA* | Elad | 0:40 | 3:40 |
| 7 CT Branching | Elad | 0:50 | 4:30 |
| 8 Our Implementation | Elad | 0:30 | 5:00 |
| 9 Reproduction Results | Kfir | 0:50 | 5:50 |
| 10 Extension | Kfir | 1:00 | 6:50 |
| 11 Key Findings | Kfir | 0:40 | 7:30 |
| 12 Conclusion | Nimrod | 0:30 | 8:00 |

**Total: 8:00 minutes**
