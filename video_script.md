# Video Script - CBS for Optimal Multi-Agent Pathfinding
## Bar-Ilan University | Search in AI Course | Team: Nimrod Netzer, Elad Damti, Kfir Dahan
## Total Duration: ~8 minutes

---

## SLIDE 1 - Title Slide
**[Nimrod - 0:00-0:20]**

> "Hello, we are Nimrod Netzer, Elad Damti, and Kfir Dahan from Bar-Ilan University.
> In this video we present our project on Conflict-Based Search for Optimal Multi-Agent Pathfinding,
> based on the 2015 paper by Sharon, Stern, Felner, and Sturtevant, published in the journal Artificial Intelligence."

---

## SLIDE 2 - What is MAPF?
**[Nimrod - 0:20-1:10]**

> "Imagine a warehouse with dozens of robots that all need to move from their starting positions
> to their target positions - without crashing into each other.
>
> This is the Multi-Agent Path Finding problem, or MAPF.
> Formally: we have a graph, k agents, each with a start and a goal.
> Agents move one step per timestep, or they can wait.
> The objective is to minimize the Sum of Costs - the total number of steps taken by all agents.
>
> MAPF is used in real-world applications like Amazon warehouse robots, airport ground traffic,
> railway scheduling, and video game AI."

---

## SLIDE 3 - Why is MAPF Hard?
**[Nimrod - 1:10-1:55]**

> "The obvious approach is to search the joint state space of all agents together.
> But the joint space explodes exponentially - it grows as O of V to the power k,
> where V is the number of vertices and k is the number of agents.
>
> With just 10 agents on a 5 by 5 grid, the state space has nearly 10 million nodes.
> For 30 agents on a realistic map - it is completely infeasible.
>
> In our experiments, Joint A-star succeeded on only 32% of 6-agent instances
> and failed on 100% of 8-agent instances within 5 seconds.
> We need a smarter algorithm."

---

## SLIDE 4 - Conflict Types
**[Nimrod - 1:55-2:30]**

> "Before we explain CBS, let us define what a conflict is.
>
> A vertex conflict happens when two agents occupy the same location at the same timestep.
> An edge conflict - also called a swap conflict - happens when two agents cross the same
> edge in opposite directions between two consecutive timesteps.
>
> The paper also defines following conflicts, cycle conflicts, and swapping conflicts.
> In our implementation we detect and resolve vertex and edge conflicts,
> which is sufficient to guarantee correctness and optimality."

---

## SLIDE 5 - CBS Overview
**[Elad - 2:30-3:00]**

> "Conflict-Based Search, or CBS, is a two-level algorithm.
>
> At the high level, CBS builds a Constraint Tree - a binary tree where each node
> represents a set of constraints imposed on individual agents.
> CBS searches this tree using best-first search, always expanding the node with the lowest
> total Sum of Costs.
>
> At the low level, for each CT node, each agent is planned independently using
> Time-Space A-star, which respects the agent's specific constraint set."

---

## SLIDE 6 - Time-Space A* (Low Level)
**[Elad - 3:00-3:40]**

> "Time-Space A-star is our low-level planner, implemented in tsa_star.py.
> Unlike regular A-star, the state includes both the vertex AND the timestep.
> So the state is the pair (vertex v, time t).
>
> A constraint says: agent i cannot be at vertex v at time t.
> Before expanding any state, we check if it violates any constraint in the agent's constraint set.
> The heuristic is Manhattan distance to the goal - which is admissible on 4-connected grids,
> so TSA-star is optimal.
>
> One important detail: we also check for future constraints at the goal vertex
> before allowing the agent to stop there, to avoid premature termination."

---

## SLIDE 7 - CBS High Level (CT Branching)
**[Elad - 3:40-4:30]**

> "Here is how the high level works, step by step.
>
> First, CBS plans each agent independently with TSA-star - this is the root of the Constraint Tree.
> Then it scans all agent pairs for the first conflict.
> If there is no conflict, we are done - we found an optimal solution.
>
> If there is a conflict - say agents i and j both visit vertex v at time t -
> CBS creates two child nodes.
> In the left child, agent i is forbidden from vertex v at time t.
> In the right child, agent j is forbidden.
> Both children replan only the constrained agent with TSA-star.
>
> CBS picks the cheapest child by Sum of Costs and repeats.
> Because it searches best-first and TSA-star is optimal,
> the first complete solution CBS finds is guaranteed to be globally optimal."

---

## SLIDE 8 - Our Implementation
**[Elad - 4:30-5:00]**

> "We implemented CBS from scratch in Python 3.13 without using the original authors' code.
>
> The implementation is split into seven modules:
> graph.py for the 4-connected grid,
> tsa_star.py for the low-level Time-Space A-star,
> conflict.py for detecting vertex and edge conflicts,
> cbs.py for the high-level Constraint Tree,
> joint_astar.py for the Joint-State-Space A-star baseline,
> and benchmark.py for running all experiments.
>
> The work was divided: Nimrod implemented TSA-star,
> I implemented conflict detection and the CBS tree,
> and Kfir built the Joint A-star baseline, the experiment runner, and the extension."

---

## SLIDE 9 - Reproduction Results
**[Kfir - 5:00-5:50]**

> "For the reproduction, we implemented the two central results from Sharon et al. 2015:
> success rate and runtime as a function of the number of agents.
>
> We ran CBS and Joint-State-Space A-star on a 20 by 20 open grid with 10% random obstacles.
> We tested 8 agent counts from 4 to 20, with 25 random instances each.
> CBS had a 30-second time limit; Joint A-star had a 5-second limit.
>
> The results match the paper's trend:
> CBS succeeds 100% at 4 agents and remains above 90% up to 12 agents,
> before dropping to 60% at 20 agents as problems become harder.
>
> Joint A-star, by contrast, already fails 68% of instances at 6 agents,
> and fails completely - 0% success - from 8 agents onward.
> This confirms the exponential state-space explosion the paper describes."

---

## SLIDE 10 - Extension: Map Topology
**[Kfir - 5:50-6:50]**

> "For our extension, we asked: does map topology affect CBS performance?
>
> We compared two map types on the same 20 by 20 grid size:
> an open grid with 10% random obstacles,
> and a warehouse grid - structured rows of shelves with single-cell-wide corridors,
> designed to simulate a real warehouse environment.
>
> We ran CBS on both maps for 8 agent counts from 4 to 20, with 25 instances each
> and a 15-second time limit.
>
> The results are striking:
> At 20 agents, CBS success on the open grid is 64%,
> while on the warehouse grid it drops to only 28%.
> The Constraint Tree expands 3,258 nodes on the warehouse map
> versus 877 nodes on the open grid - that is 3.7 times more.
>
> Why? Narrow corridors force agents onto the same cells, creating vertex conflicts.
> Each conflict resolution forces a longer detour, which generates new conflicts
> in adjacent corridors - a cascade effect that makes the CT much deeper."

---

## SLIDE 11 - Key Findings
**[Kfir - 6:50-7:30]**

> "To summarize our findings:
>
> First - CBS works. It finds optimal, conflict-free solutions and scales
> far better than Joint A-star, which fails completely from 8 agents onward.
>
> Second - map topology matters significantly.
> Warehouse-style bottleneck maps reduce CBS success from 64% to 28% at 20 agents,
> with 3.7 times more CT node expansions.
> This is a practical insight for real warehouse robot deployments.
>
> Third - our implementation correctly reproduces the paper's trends.
> CBS solves 4-agent problems in under 2 milliseconds,
> and handles 10-agent warehouse problems within 0.26 seconds on average.
>
> The main limitation is scalability beyond 20 agents, where CBS also begins timing out,
> motivating the improvements described in the paper such as
> conflict prioritization and high-level heuristics."

---

## SLIDE 12 - Conclusion
**[Nimrod - 7:30-8:00]**

> "In this project we studied, implemented, and extended the Conflict-Based Search algorithm
> for optimal Multi-Agent Path Finding.
>
> CBS elegantly avoids the exponential joint state space by separating planning per agent
> and resolving only actual conflicts when they arise.
>
> Our extension showed that real-world map structure - specifically warehouse corridors -
> significantly amplifies CBS difficulty by creating cascading vertex conflicts,
> which is a practically important finding for warehouse robotics applications.
>
> Thank you for watching. We are Nimrod, Elad, and Kfir - ready for the defense."

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

---

## KEY NUMBERS TO REMEMBER (from our actual results)

| Metric | Value |
|--------|-------|
| Joint A* success at 6 agents | 32% |
| Joint A* success at 8+ agents | 0% |
| CBS success at 4 agents | 100% |
| CBS success at 20 agents (open) | 60% |
| CBS success at 20 agents (warehouse) | 28% |
| CT nodes at 20 agents (open) | 877 |
| CT nodes at 20 agents (warehouse) | 3,258 (3.7x) |
| CBS time at 4 agents | ~0.002s |
| CBS time at 10 agents (warehouse) | ~0.26s |
| Joint A* time limit | 5s |
| CBS time limit (reproduction) | 30s |
| CBS time limit (extension) | 15s |
| Instances per agent count | 25 |
| Grid size | 20x20 |
| Agent counts tested | 4, 6, 8, 10, 12, 15, 18, 20 |
