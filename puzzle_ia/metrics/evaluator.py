import time

def print_solution(solution):
    print("\n--- Camino de la solución ---")
    for step, node in enumerate(solution):
        action = node.action
        state = node.state
        if action:
            print(f"Paso {step}: mover {action}")
        else:
            print(f"Paso {step}: (estado inicial)")

        # usamos state.tiles (la tupla con los números)
        for i in range(0, 9, 3):
            row = state.tiles[i:i+3]
            print(" ".join(str(x) if x != 0 else " " for x in row))
        print("-"*7)


# Función para ejecutar un algoritmo y medir métricas
def run_search(name, func, problem, heuristic=None, **kwargs):
    start_time = time.time()
    if heuristic:
        solution, expanded = func(problem, heuristic, **kwargs)
    else:
        solution, expanded = func(problem, **kwargs)
    elapsed = time.time() - start_time

    if solution:
        steps = len(solution) - 1
        print_solution(solution)
    else:
        steps = None

    return {
        "algoritmo": name,
        "solucion_encontrada": solution is not None,
        "pasos": steps,
        "nodos_expandidos": expanded,
        "tiempo": round(elapsed, 4)
    }