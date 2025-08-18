from core.structures import MinHeap, Queue, Stack
from core.problem import Problem
from core.abstracts import Node, reconstruct_path


class PriorityQueue:
    # redefinida aquí para aislar dependencia (opcional: usa la de estructuras)
    def __init__(self):
        self._h = MinHeap()
        self._t = 0
    def push(self, priority, item):
        self._t += 1
        self._h.push((priority, self._t, item))
    def pop(self):
        return self._h.pop()[2]
    def is_empty(self): return self._h.is_empty()
    def __len__(self): return len(self._h)

def BFS(problem: Problem):
    frontier = Queue()
    frontier.enqueue(Node(problem.initial_state()))
    explored = set()
    expanded = 0
    while not frontier.is_empty():
        n = frontier.dequeue()
        if problem.is_goal(n.state): return reconstruct_path(n), expanded
        if n.state in explored: continue
        explored.add(n.state); expanded += 1
        for c in n.expand(problem): frontier.enqueue(c)
    return None, expanded

def DFS(problem: Problem, depth_limit=None):
    frontier = Stack()
    frontier.push(Node(problem.initial_state()))
    explored = set()
    expanded = 0
    while not frontier.is_empty():
        n = frontier.pop()
        if problem.is_goal(n.state): return reconstruct_path(n), expanded
        if n.state in explored: continue
        if depth_limit is not None and n.depth > depth_limit: continue
        explored.add(n.state); expanded += 1
        for c in n.expand(problem): frontier.push(c)
    return None, expanded

def UCS(problem: Problem):
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(0.0, start)
    best = {start.state: 0.0}
    expanded = 0
    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state): return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(c.g, c)
    return None, expanded

def Greedy(problem: Problem, h):
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(h(start.state), start)
    seen = set()
    expanded = 0
    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state): return reconstruct_path(n), expanded
        if n.state in seen: continue
        seen.add(n.state); expanded += 1
        for c in n.expand(problem): pq.push(h(c.state), c)
    return None, expanded

def A_star(problem: Problem, h):
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(h(start.state) + start.g, start)
    best = {start.state: 0.0}
    expanded = 0
    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state): return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            f = c.g + h(c.state)
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(f, c)
    return None, expanded

def IDA_star(problem: Problem, h):
    from math import inf
    start = Node(problem.initial_state())
    bound = h(start.state)
    expanded_total = 0

    def dfs_limited(n, g, bound):
        nonlocal expanded_total
        f = g + h(n.state)
        if f > bound: return f, None
        if problem.is_goal(n.state): return f, reconstruct_path(n)
        m = inf
        for c in n.expand(problem):
            expanded_total += 1
            t, sol = dfs_limited(c, g + (c.g - n.g), bound)
            if sol is not None: return t, sol
            if t < m: m = t
        return m, None

    while True:
        t, sol = dfs_limited(start, 0, bound)
        if sol is not None: return sol, expanded_total
        if t == float("inf"): return None, expanded_total
        bound = t

def Weighted_A_star(problem: Problem, h, weight=1.5):
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    f_start = start.g + weight * h(start.state)
    pq.push(f_start, start)
    best = {start.state: 0.0}
    expanded = 0

    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            f = c.g + weight * h(c.state)
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(f, c)
    return None, expanded
