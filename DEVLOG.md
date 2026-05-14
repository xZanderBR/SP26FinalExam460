# Development Log – The Torchbearer

**Student Name:** Zander Barajas
**Student ID:** 826847977

---

## Entry 1 – 05-09-2026: Initial Plan

My plan is to build the solution in pipeline order: `run_dijkstra` first, then
`select_sources` and `precompute_distances`, then `find_optimal_route` and
`_explore` together. I expect the lower-bound estimate in Part 6b to be the
hardest piece, so I will start with a simple admissible bound and only tighten
it if time allows. I will get an unpruned DFS over relic orders working before
adding the best-so-far prune, so I can confirm the prune does not change any
result. I plan to test with hand-traced graphs for `run_dijkstra`, the four
provided tests for the full pipeline, and a few extra graphs with known
optimal costs.

---

## Entry 2 – 05-12-2026: Wrong assumption about source selection

I first wrote `select_sources` to include the exit node, because my intuition was that every named node we care about should be a Dijkstra source. Going back over the design for Part 2a I realized the exit is only ever a destination (the route never departs from it), so running Dijkstra from the exit would waste an entire run with no entry in `dist_table` that the search would ever read. I removed `exit_node` from `select_sources` and confirmed the table still contains every lookup the search needs: spawn-to-anywhere and relic-to-anywhere, where "anywhere" already includes the exit as an inner-dict key.

---

## Entry 3 – 05-13-2026: State design split across two variables

For Part 5 I had to commit to a representation for the relics already collected, and the search needs two different views of that information: an ordered list to return as the final answer, and a fast-membership structure for backtracking inside the DFS. Picking only one would hurt: a list alone makes membership O(k) per check, and a set alone loses the visit order. I kept both. `relics_visited_order` is a list that I append to on collect and pop on backtrack, and `relics_remaining` is a set of still-uncollected relics that gives O(1) membership, removal, and re-insertion. I am holding off on writing `find_optimal_route` and `_explore` until Part 6 is locked, since the prune logic lives inside `_explore` and one pass avoids a rewrite.

---

## Entry 4 – 05-14-2026: Post-Implementation Reflection

With more time the first improvement I would make is sorting the relics inside the recursive loop by step cost, so that the cheapest first move is tried first. This makes `best[0]` drop earlier in the search, which causes the prune to fire on more later branches. I would also tighten the lower bound by adding the cheapest edge into a remaining relic plus the cheapest edge from a remaining relic to the exit, since the current bound only counts the direct path to the exit and ignores the cost of routing through any uncollected relic. Finally, I would add tests with larger `k` and asymmetric graphs, since the four provided tests all use `k <= 3` and do not really stress the prune.

---

## Final Entry – 05-14-2026: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 0.5 |
| Part 2: Precomputation Design | 1.0 |
| Part 3: Algorithm Correctness | 1.5 |
| Part 4: Search Design | 1.0 |
| Part 5: State and Search Space | 1.0 |
| Part 6: Pruning | 1.5 |
| Part 7: Implementation | 3.0 |
| README and DEVLOG writing | 2.0 |
| **Total** | **11.5** |
