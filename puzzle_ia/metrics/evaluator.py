import time

class SearchResult:
    def __init__(self, path, cost, expanded, depth, elapsed):
        self.path = path
        self.cost = cost
        self.expanded = expanded
        self.depth = depth
        self.elapsed = elapsed


def run_and_measure(search_fn, problem, heuristic=None):
    start = time.perf_counter()
    if heuristic:
        result = search_fn(problem, heuristic)
    else:
        result = search_fn(problem)
    end = time.perf_counter()

    # result aquí debería incluir (path, cost, expanded, depth)
    return SearchResult(result.path, result.cost, result.expanded,
                        result.depth, end - start)
