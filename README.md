# The Torchbearer

**Student Name:** Zander Barajas
**Student ID:** 826847977
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single Dijkstra run from S gives the cheapest cost from S to every node, but the route must also travel between relics, and those inter-relic costs are never produced by a run from S. It therefore cannot decide which relic to visit first, second, and so on.

- **What decision remains after all inter-location costs are known:**
  The only thing left to choose is the order in which to visit the relics, since the cost of any walk that uses cheapest paths between consecutive relics is fully determined by that order.

- **Why this requires a search over orders (one sentence):**
  Different visit orders produce different totals from the same distance table, so finding the minimum means searching over the possible orders rather than running one shortest-path computation.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Spawn node `S` | The route starts at `S`, so the search needs the cheapest cost from `S` to every relic. |
| Each relic node `R` in `M` | After collecting a relic the search departs from it to either another relic or the exit, so it needs the cheapest cost from each relic to every other relic and to the exit. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested Python `dict` (`dict[node, dict[node, float]]`) |
| What the keys represent | Outer key is the source node; inner key is the destination node. |
| What the values represent | Cheapest total edge-weight cost from the source to the destination, or `float('inf')` if unreachable. |
| Lookup time complexity | O(1) for `dist_table[u][v]` |
| Why O(1) lookup is possible | Both levels are hash-based dicts, so each key access is expected O(1) and the two chained lookups remain O(1). |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** `k + 1` (one from spawn `S`, one from each of the `k` relics).
- **Cost per run:** `O(m log n)` using a binary-heap priority queue.
- **Total complexity:** `O((k + 1) * m log n) = O(k * m log n)`.
- **Justification (one line):** Each source's run is independent, so the total is the sum of `k + 1` runs of cost `O(m log n)` each.

---

## Part 3: Algorithm Correctness

### Part 3a: Invariant Explanation

- **For nodes already finalized (in S):**
  `dist[v]` is locked in as the true cheapest cost from `x` to `v`, and no later relaxation can lower it.

- **For nodes not yet finalized (not in S):**
  `dist[u]` is the cheapest cost found so far for a path from `x` to `u` whose intermediate stops are all already finalized, and it acts as an upper bound that may still drop as more nodes are finalized.

### Part 3b: Invariant Maintenance

- **Initialization : why the invariant holds before iteration 1:**
  Initially `S` is empty, so the finalized-node clause has nothing to check. Setting `dist[x] = 0` with every other `dist[u] = inf` is correct because the only path discovered so far is the zero-length path from `x` to itself.

- **Maintenance : why finalizing the min-dist node is always correct:**
  The next node added is the non-finalized `u` with the smallest `dist[u]`. Any alternative path from `x` to `u` must first leave `S` at some vertex `w`, and that prefix keeps its interior in `S`, so by the non-finalized clause its cost is at least `dist[w] >= dist[u]`. Because every edge weight is nonnegative, the rest of that path from `w` to `u` only adds cost, so the alternative cannot beat `dist[u]`.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the loop exits every reachable node is in `S`, so every reachable `dist[v]` equals the true shortest-path distance from `x`, and unreachable nodes keep `dist = inf`.

### Part 3c: Why Correctness Matters

The search picks each step by reading `dist_table[u][v]`, so if any of those values is wrong the planner can pick a worse relic order or wrongly reject a valid route, and the final fuel cost will not be optimal.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** Greedy picks the next relic with the smallest direct cost from the current location, without considering how that choice constrains the rest of the trip. A locally cheap step can force an expensive move later, so greedy can miss the optimal total.
- **Counter-example setup:** Spawn `S`, relics `A` and `B`, exit `T`. Pairwise costs: `d(S, A) = 1`, `d(S, B) = 2`, `d(A, B) = 100`, `d(B, A) = 1`, `d(A, T) = 1`, `d(B, T) = 1`.
- **What greedy picks:** From `S` greedy takes `A` because `d(S, A) = 1` is cheaper than `d(S, B) = 2`. From `A` the only remaining relic is `B`, costing 100. From `B` it goes to `T` for 1. Total: `1 + 100 + 1 = 102`.
- **What optimal picks:** The order `S → B → A → T` costs `2 + 1 + 1 = 4`.
- **Why greedy loses:** Choosing the cheap first step `S → A` forces the route to use the expensive `A → B` edge instead of the cheap `B → A` edge, so the 1-fuel saving up front costs 98 fuel later.

### What the Algorithm Must Explore

- The algorithm must explore every possible order in which the relics can be visited, evaluate each order's total cost using the precomputed distance table, and keep the minimum.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | `current_loc` | node (graph key, typically `str`) | The vertex where the Torchbearer currently stands. |
| Relics already collected | `relics_visited_order` | `list[node]` | Ordered list of relics collected on the current branch; appended when a relic is picked up and popped on backtrack. |
| Fuel cost so far | `cost_so_far` | `float` | Sum of edge weights along the path taken from spawn to `current_loc`. |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | Python `set` (held in `relics_remaining`, the still-uncollected relics). |
| Operation: check if relic already collected | Time complexity: O(1) (`relic not in relics_remaining`). |
| Operation: mark a relic as collected | Time complexity: O(1) (`relics_remaining.discard(relic)`). |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) (`relics_remaining.add(relic)`). |
| Why this structure fits | A hash-based set gives expected O(1) membership, removal, and insertion, and the mutate-then-restore pattern fits DFS backtracking without copying the structure at each call. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** `O(k!)` where `k = |M|`.
- **Why:** Without pruning the search must try every permutation of the `k` relics, since any order could in principle be the optimal one.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
