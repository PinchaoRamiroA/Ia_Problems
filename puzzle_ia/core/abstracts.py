
from typing import Any, Iterable, Optional, List, Tuple

class State:
    def key(self) -> Any: raise NotImplementedError
    def __hash__(self): return hash(self.key())
    def __eq__(self, o): return isinstance(o, State) and self.key()==o.key()

class Problem:
    def initial_state(self) -> State: raise NotImplementedError
    def is_goal(self, s: State) -> bool: raise NotImplementedError
    def actions(self, s: State) -> Iterable[Any]: raise NotImplementedError
    def result(self, s: State, a: Any) -> State: raise NotImplementedError
    def step_cost(self, s: State, a: Any, sp: State) -> float: return 1.0

class Node:
    __slots__ = ("state","parent","action","g","depth")
    def __init__(self, state: State, parent: Optional['Node']=None, action=None, g: float=0.0):
        self.state = state; self.parent = parent; self.action = action; self.g = g
        self.depth = 0 if parent is None else parent.depth + 1
    def expand(self, problem: Problem):
        for a in problem.actions(self.state):
            sp = problem.result(self.state, a)
            yield Node(sp, self, a, self.g + problem.step_cost(self.state, a, sp))

# Function that reconstructs the path from the initial state to the goal state
def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return list(reversed(path))
