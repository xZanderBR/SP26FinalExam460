# Development Log – The Torchbearer

**Student Name:** Zander Barajas
**Student ID:** 826847977

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 05-09-2026: Initial Plan

I will build the solution in pipeline order: `run_dijkstra` first, then
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

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
