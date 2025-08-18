from core.algorithms import BFS, DFS, UCS, Greedy, A_star, IDA_star, Weighted_A_star

def solve_puzzle(problem, algorithm, heuristic=None, weight=1.5):
    if algorithm == "BFS":
        return BFS(problem)
    elif algorithm == "DFS":
        return DFS(problem)
    elif algorithm == "UCS":
        return UCS(problem)
    elif algorithm == "Greedy":
        return Greedy(problem, heuristic)
    elif algorithm == "A*":
        return A_star(problem, heuristic)
    elif algorithm == "Weighted A*":
        return Weighted_A_star(problem, heuristic, weight)
    else:
        raise ValueError("Algoritmo no soportado")