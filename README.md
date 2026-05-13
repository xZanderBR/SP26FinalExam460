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

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

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
