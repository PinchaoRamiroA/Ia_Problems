from core.problem import EightPuzzle
from core.search import bfs, dfs, astar
from core.heuristics import misplaced, manhattan

def menu_cli():
    print("\n=== Menú de Algoritmos ===")
    print("1. BFS")
    print("2. DFS")
    print("3. A* (Manhattan)")

    choice = input("Selecciona opción: ")
    initial = (1,2,3,4,5,6,7,0,8)
    goal = (1,2,3,4,5,6,7,8,0)
    problem = EightPuzzle(initial, goal)

    if choice == "1":
        bfs(problem)
    elif choice == "2":
        dfs(problem)
    elif choice == "3":
        astar(problem, manhattan)
    else:
        print("Opción inválida")
