import time
from kivy.clock import Clock
from core.heuristics import manhattan, misplaced, linear_conflict
from ui.dispatcher import solve_puzzle
from kivy.uix.button import Button
from core.problem import Puzzle, PuzzleState
from core.abstracts import State

class PuzzleController:
    def __init__(self, app, problem, metrics):
        self.app = app
        self.problem: Puzzle = problem
        self.metrics = metrics
        self.solution_steps = []
        self.current_step_index = 0
        self.animation_event = None
        self.is_animating = False

    def on_algorithm_selected(self, spinner, text):
        """Muestra u oculta el selector de heurísticas según el algoritmo elegido."""
        heuristic_algos = ["A*", "Greedy", "Weighted A*", "IDA*"]
        if text in heuristic_algos:
            self.app.layout.heuristic_spinner.opacity = 1
            self.app.layout.heuristic_spinner.disabled = False
        else:
            self.app.layout.heuristic_spinner.opacity = 0
            self.app.layout.heuristic_spinner.disabled = True
            self.app.layout.heuristic_spinner.text = "Choose the heuristic"

    def on_play_button_press(self, instance):
        """Se activa al presionar el botón de Play."""
        selected_algorithm = self.app.layout.algo_spinner.text
        if selected_algorithm == "Choose the algorithm":
            self.app.show_popup("Error", "Please select an algorithm first.")
            return

        if self.is_animating:
            self.app.show_popup("Info", "Animation is already running. Please wait.")
            return

        self.app.layout.play_button.text = "Solving..."
        self.app.layout.play_button.disabled = True

        # Iniciar la búsqueda del algoritmo en un hilo separado o un cronómetro
        # para evitar bloquear la UI
        Clock.schedule_once(lambda dt: self.solve_puzzle(selected_algorithm), 0.1)

    def solve_puzzle(self, algorithm_name):
        """Resuelve el puzzle usando el algoritmo seleccionado y almacena los pasos."""
        print(f"Starting to solve with {algorithm_name}...")

        solution_path = None
        expanded_nodes = 0
        elapsed_time = 0
        
        try:
            start_time = time.time()
            heuristics = {
                "Manhattan": manhattan,
                "Misplaced Tiles": misplaced,
                "Linear Conflict": linear_conflict,
            }
            heuristic = self.app.layout.heuristic_spinner.text
            heuristic_func = heuristics.get(heuristic)

            
            if algorithm_name in ["A*", "Greedy", "Weighted A*", "IDA*"]:
                if heuristic_func:
                    solution_path, expanded_nodes = solve_puzzle(self.problem, algorithm_name, heuristic=heuristic_func)
                else:
                    self.error_solution("Please select a heuristic for this algorithm.")
                    return
            else:
                solution_path, expanded_nodes = solve_puzzle(self.problem, algorithm_name)
            
            elapsed_time = time.time() - start_time
        except ValueError as e:
            self.app.show_popup("Error", str(e))
            return
        except Exception as e:
            self.app.show_popup("Error", f"An unexpected error occurred: {e}")
            return
        finally:
            if solution_path is not None and isinstance(solution_path, (list, tuple)):
                if solution_path:
                    # Validar que los elementos en la solución sean del tipo correcto
                    if all(hasattr(node.state, 'tiles') for node in solution_path):
                        self.solution_steps = solution_path
                        self.current_step_index = 0
                        self.is_animating = True
                        self.app.layout.play_button.text = "Solving..."
                        self.animation_event = Clock.schedule_interval(self.animate_solution, 0.5)

                        self.metrics.set(
                            algoritmo=algorithm_name,
                            heuristica=heuristic if heuristic_func else None,
                            solucion_encontrada=True,
                            pasos=len(solution_path) - 1,
                            nodos_expandidos=expanded_nodes,
                            tiempo=round(elapsed_time, 4)
                        )

                    else:
                        self.error_solution("Invalid solution path.")
                else:
                    self.error_solution("No solution found for this puzzle state.")
            else:
                self.error_solution("No solution found or returned value is not a list of states.")

    def animate_solution(self, dt):
        """
        Actualiza la UI para mostrar el siguiente paso de la solución.
        """
        if self.current_step_index < len(self.solution_steps):
            # Accede al atributo '.state' del nodo antes de pasarlo a la UI
            state_to_display = self.solution_steps[self.current_step_index].state
            self.update_board_ui(state_to_display)
            self.current_step_index += 1
        else:
            # Detiene la animación cuando se ha mostrado toda la solución
            if self.animation_event:
                self.animation_event.cancel()
            self.is_animating = False
            self.app.layout.play_button.text = "Again?"
            self.app.layout.play_button.disabled = False
            self.app.display_metrics()

    def update_board_ui(self, state: State):
        """
        Actualiza el tablero de la UI con los valores de un estado dado.
        """

        # Limpia el tablero actual
        self.app.layout.board_layout.clear_widgets()

        # Llena el tablero con los nuevos valores
        for index, tile in enumerate(state.tiles):
            # Los botones que representan el espacio vacío pueden tener un estilo diferente
            if tile == 0:
                btn = self.app.layout.create_tile(0, index)  # Espacio vacío
            else:
                btn = self.app.layout.create_tile(tile, index)
            self.app.layout.board_layout.add_widget(btn)

    def on_tile_press(self, index):
        """Maneja el click en una celda para mover manualmente las fichas."""
        if self.is_animating:
            return  # Desactiva interacción mientras se anima

        current_state = self.problem.start  # PuzzleState actual
        tiles = list(current_state.tiles)   # copiamos porque es tupla

        empty_index = tiles.index(0)

        # Solo si la ficha es vecina al hueco
        if self.is_adjacent(index, empty_index):
            # Intercambiar
            tiles[empty_index], tiles[index] = tiles[index], tiles[empty_index]

            # Nuevo estado
            new_state = PuzzleState(tiles)
            self.problem.start = new_state  # <<<< guardar como nuevo inicio
            self.app.layout.reset_board(new_state.tiles)  # refrescar tablero

            # Verifica si es victoria
            if self.is_goal_state(new_state):
                self.app.show_popup("¡Victoria!", "Has resuelto el puzzle.")
                self.app.layout.play_button.text = "Again?"
                self.app.layout.play_button.disabled = False


    def is_adjacent(self, i1, i2):
        """Verifica si dos posiciones son adyacentes en la grilla 3x3."""
        x1, y1 = divmod(i1, 3)
        x2, y2 = divmod(i2, 3)
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def is_goal_state(self, state: State) -> bool:
        """Verifica si el estado actual es el estado objetivo."""
        return self.problem.is_goal(state)

    def error_solution(self, message):
        self.app.show_popup("Error", message)
        self.app.layout.play_button.text = "Play"
        self.app.layout.play_button.disabled = False