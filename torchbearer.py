"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Zander Barajas
Student ID:   826847977

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "A single Dijkstra run from S gives the cheapest cost from S to every "
        "node, but the route must also travel between relics, and those "
        "inter-relic costs are never produced by a run from S. It therefore "
        "cannot decide which relic to visit first, second, and so on.\n\n"
        "The only thing left to choose is the order in which to visit the "
        "relics, since the cost of any walk that uses cheapest paths between "
        "consecutive relics is fully determined by that order.\n\n"
        "Different visit orders produce different totals from the same "
        "distance table, so finding the minimum means searching over the "
        "possible orders rather than running one shortest-path computation."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    sources = {spawn}
    sources.update(relics)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    dist_table = {}
    for source in select_sources(spawn, relics, exit_node):
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return (
        "dist[v] is locked in as the true cheapest cost from x to v, and no "
        "later relaxation can lower it.\n\n"
        "dist[u] is the cheapest cost found so far for a path from x to u "
        "whose intermediate stops are all already finalized, and it acts as "
        "an upper bound that may still drop as more nodes are finalized.\n\n"
        "Initially S is empty, so the finalized-node clause has nothing to "
        "check. Setting dist[x] = 0 with every other dist[u] = inf is "
        "correct because the only path discovered so far is the zero-length "
        "path from x to itself.\n\n"
        "The next node added is the non-finalized u with the smallest "
        "dist[u]. Any alternative path from x to u must first leave S at "
        "some vertex w, and that prefix keeps its interior in S, so by the "
        "non-finalized clause its cost is at least dist[w] >= dist[u]. "
        "Because every edge weight is nonnegative, the rest of that path "
        "from w to u only adds cost, so the alternative cannot beat "
        "dist[u].\n\n"
        "When the loop exits every reachable node is in S, so every "
        "reachable dist[v] equals the true shortest-path distance from x, "
        "and unreachable nodes keep dist = inf.\n\n"
        "The search picks each step by reading dist_table[u][v], so if any "
        "of those values is wrong the planner can pick a worse relic order "
        "or wrongly reject a valid route, and the final fuel cost will not "
        "be optimal."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
        "Greedy picks the next relic with the smallest direct cost from the "
        "current location, without considering how that choice constrains "
        "the rest of the trip. A locally cheap step can force an expensive "
        "move later, so greedy can miss the optimal total.\n\n"
        "Spawn S, relics A and B, exit T. Pairwise costs: d(S, A) = 1, "
        "d(S, B) = 2, d(A, B) = 100, d(B, A) = 1, d(A, T) = 1, "
        "d(B, T) = 1.\n\n"
        "From S greedy takes A because d(S, A) = 1 is cheaper than "
        "d(S, B) = 2. From A the only remaining relic is B, costing 100. "
        "From B it goes to T for 1. Total: 1 + 100 + 1 = 102.\n\n"
        "The order S -> B -> A -> T costs 2 + 1 + 1 = 4.\n\n"
        "Choosing the cheap first step S -> A forces the route to use the "
        "expensive A -> B edge instead of the cheap B -> A edge, so the "
        "1-fuel saving up front costs 98 fuel later.\n\n"
        "The algorithm must explore every possible order in which the "
        "relics can be visited, evaluate each order's total cost using the "
        "precomputed distance table, and keep the minimum."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    best = [float('inf'), []]
    relics_remaining = set(relics)
    relics_visited_order = []
    _explore(dist_table, spawn, relics_remaining, relics_visited_order,
             0, exit_node, best)
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    """
    # Base case: every relic collected, finish at exit.
    if not relics_remaining:
        finish_cost = dist_table[current_loc].get(exit_node, float('inf'))
        total = cost_so_far + finish_cost
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    # Pruning is safe because the lower bound is admissible: every completion
    # of this branch must end at exit_node, and by Dijkstra correctness
    # dist_table[current_loc][exit_node] is the cheapest possible cost to get
    # there, with the rest of any completion only adding nonnegative cost on
    # top. So if cost_so_far + lower_bound is already at least best[0], no
    # completion can beat best[0] and skipping this branch cannot lose the
    # optimal solution.
    lower_bound = dist_table[current_loc].get(exit_node, float('inf'))
    if cost_so_far + lower_bound >= best[0]:
        return

    # Recursive case with backtracking over every uncollected relic.
    for relic in list(relics_remaining):
        step_cost = dist_table[current_loc].get(relic, float('inf'))
        if step_cost == float('inf'):
            continue
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        _explore(dist_table, relic, relics_remaining, relics_visited_order,
                 cost_so_far + step_cost, exit_node, best)
        relics_visited_order.pop()
        relics_remaining.add(relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
