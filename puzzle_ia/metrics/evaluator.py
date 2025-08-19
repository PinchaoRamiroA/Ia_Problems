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

class Metrics:
    def __init__(self):
        self.metrics = {
            "algoritmo": None,
            "solucion_encontrada": False,
            "heuristica": None,
            "pasos": 0,
            "nodos_expandidos": 0,
            "tiempo": 0.0
        }

    def set(self, algoritmo, heuristica, solucion_encontrada, pasos, nodos_expandidos, tiempo):
        self.metrics.update({
            "algoritmo": algoritmo,
            "solucion_encontrada": solucion_encontrada,
            "heuristica": heuristica,
            "pasos": pasos,
            "nodos_expandidos": nodos_expandidos,
            "tiempo": tiempo
        })

    def get_metrics_string(self):
        if self.metrics["heuristica"]:
            return (
                f"Algoritmo: {self.metrics['algoritmo']}\n"
                f"Heurística: {self.metrics['heuristica']}\n"
                f"Solución encontrada: {'Sí' if self.metrics['solucion_encontrada'] else 'No'}\n"
                f"Pasos: {self.metrics['pasos']}\n"
                f"Nodos expandidos: {self.metrics['nodos_expandidos']}\n"
                f"Tiempo de ejecución: {self.metrics['tiempo']} segundos"
            )
        return (
            f"Algoritmo: {self.metrics['algoritmo']}\n"
            f"Solución encontrada: {'Sí' if self.metrics['solucion_encontrada'] else 'No'}\n"
            f"Pasos: {self.metrics['pasos']}\n"
            f"Nodos expandidos: {self.metrics['nodos_expandidos']}\n"
            f"Tiempo de ejecución: {self.metrics['tiempo']} segundos"
        )
