from core.heuristics import misplaced, manhattan, linear_conflict
from core.algorithms import BFS, DFS, UCS, Greedy, A_star, IDA_star, Weighted_A_star
from core.problem import Puzzle
from core.create_puzzle import create_state
from metrics.evaluator import run_search

def action_choosing(problem, name, algorithm, heuristic=None, weight=None):
    if( heuristic != None and weight != None):
        print(run_search(name, algorithm, problem, heuristic, weight=weight))
    elif(heuristic != None):
        print(run_search(name, algorithm, problem, heuristic))
    else:
        print(run_search(name, algorithm, problem))

    print("Click to continue")
    input()

def menu_cli():
    print("=== Bienvenido al Solucionador de Rompecabezas ===")
    initial = create_state()
    problem = Puzzle(initial)

    problem.print_state(problem.initial_state())
    while True:
        print("\n=== Menú de Algoritmos ===")
        print("1. BFS")
        print("2. DFS")
        print("3. A* (Manhattan)")
        print("4. A* (Misplaced Tiles)")
        print("5. A* (Conflictos Lineales)")
        print("6. UCS")
        print("7. Greedy")
        print("8. IDA*")
        print("9. Weighted A*")
        print("0. Salir")

        choice = input("Selecciona opción: ")

        if choice == "1":
            action_choosing(problem, "BFS", BFS)
        elif choice == "2":
            action_choosing(problem, "DFS", DFS)
        elif choice == "3":
            action_choosing(problem, "A* (Manhattan)", A_star, manhattan)
        elif choice == "4":
            action_choosing(problem, "A* (Misplaced Tiles)", A_star, misplaced)
        elif choice == "5":
            action_choosing(problem, "A* (Conflictos Lineales)", A_star, linear_conflict)
        elif choice == "6":
            action_choosing(problem, "UCS", UCS)
        elif choice == "7":
            action_choosing(problem, "Greedy (manhattan)", Greedy, manhattan)
        elif choice == "8":
            action_choosing(problem, "IDA* (manhattan)", IDA_star, manhattan)
        elif choice == "9":
            w = float(input("Introduce el valor de w: "))
            action_choosing(problem, f"Weighted A* (w={w})", Weighted_A_star, manhattan, weight=w)
        elif choice == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")
