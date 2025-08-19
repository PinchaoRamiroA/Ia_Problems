import time
from kivy.clock import Clock
from core.heuristics import manhattan, misplaced, linear_conflict
from ui.dispatcher import solve_puzzle
from kivy.uix.button import Button
from core.problem import Puzzle
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
            self.app.layout.heur_row.disabled = False
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
            heuristic_func = heuristics.get(self.app.layout.heuristic_spinner.text)

            
            if algorithm_name in ["A*", "Greedy", "Weighted A*", "IDA*"]:
                if heuristic_func:
                    solution_path, expanded_nodes = solve_puzzle(self.problem, algorithm_name, heuristic=heuristic_func)
                else:
                    self.app.show_popup("Error", "Please select a heuristic for this algorithm.")
                    self.app.layout.play_button.text = "play"
                    self.app.layout.play_button.disabled = False
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
                        self.app.layout.play_button.text = "Animating..."
                        self.animation_event = Clock.schedule_interval(self.animate_solution, 0.5)

                        self.metrics.set(
                            algoritmo=algorithm_name,
                            solucion_encontrada=True,
                            pasos=len(solution_path) - 1,
                            nodos_expandidos=expanded_nodes,
                            tiempo=round(elapsed_time, 4)
                        )

                    else:
                        self.show_popup("Error", "The solution path contains nodes without a 'tiles' attribute.")
                        self.play_button.text = "▶"
                        self.play_button.disabled = False
                else:
                    self.show_popup("Error", "No solution found for this puzzle state.")
                    self.play_button.text = "▶"
                    self.play_button.disabled = False
            else:
                self.app.show_popup("Error", "No solution found or returned value is not a list of states.")
                self.app.layout.play_button.text = "▶"
                self.app.layout.play_button.disabled = False

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
            self.app.layout.play_button.text = "Done"
            self.app.layout.play_button.disabled = False
            self.app.display_metrics()

    def update_board_ui(self, state: State):
        """
        Actualiza el tablero de la UI con los valores de un estado dado.
        """

        # Limpia el tablero actual
        self.app.layout.board_layout.clear_widgets()

        # Llena el tablero con los nuevos valores
        for tile in state.tiles:
            # Los botones que representan el espacio vacío pueden tener un estilo diferente
            if tile == 0:
                btn = Button(text='', font_size='36sp', background_color=(0, 0, 0, 0))
            else:
                btn = Button(text=str(tile), font_size='36sp')
            self.app.layout.board_layout.add_widget(btn)

