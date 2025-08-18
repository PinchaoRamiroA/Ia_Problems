from core.structures import MinHeap, Queue, Stack
from core.abstracts import State, Problem

# Representación: tupla de 9 ints; 0 = hueco
GOAL = (1,2,3,4,5,6,7,8,0)
GOAL_POS = {v:i for i,v in enumerate(GOAL)}

class PuzzleState(State):
    __slots__ = ("tiles",)
    def __init__(self, tiles): 
        self.tiles = tuple(tiles)

    def key(self): 
        return self.tiles

    def __repr__(self): 
        return f"PuzzleState{self.tiles}"

class Puzzle(Problem):
    def __init__(self, start):
        self.start = PuzzleState(start)

    def initial_state(self) -> State: 
        return self.start

    def is_goal(self, s: PuzzleState) -> bool: 
        return s.tiles == GOAL

    def actions(self, s: PuzzleState):
        i = s.tiles.index(0); x,y = divmod(i,3)
        for dx,dy,a in ((1,0,"DOWN"),(-1,0,"UP"),(0,1,"RIGHT"),(0,-1,"LEFT")):
            nx,ny = x+dx,y+dy
            if 0 <= nx < 3 and 0 <= ny < 3: 
                yield a

    def result(self, s: PuzzleState, a):
        delta = {"DOWN":(1,0),"UP":(-1,0),"RIGHT":(0,1),"LEFT":(0,-1)}[a]
        i = s.tiles.index(0); x,y = divmod(i,3)
        nx,ny = x+delta[0], y+delta[1]; j = nx*3+ny
        tiles = list(s.tiles); tiles[i], tiles[j] = tiles[j], tiles[i]
        
        new_state = PuzzleState(tiles)
        return new_state

    def print_state(self, s: PuzzleState):
        for i in range(0, 9, 3):
            print(s.tiles[i:i+3])
        print()
