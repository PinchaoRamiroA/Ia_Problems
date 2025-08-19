import time
from kivy.clock import Clock
from core.heuristics import manhattan, misplaced, linear_conflict
from ui.dispatcher import solve_puzzle
from core.problem import Puzzle, PuzzleState
from core.abstracts import State

class PuzzleController:
    def __init__(self, app, problem, metrics):
        self.app = app
        self.problem: Puzzle = problem
        self.metrics = metrics
        self.solution_steps = []
        self.current_step_index = 0

        # ---- animación ----
        self.anim_event = None
        self.anim_speed = 0.5
        self.is_animating = False
        self.is_paused = False

    # ------------------------
    # Spinners
    # ------------------------
    def on_algorithm_selected(self, spinner, text):
        heuristic_algos = ["A*", "Greedy", "Weighted A*", "IDA*"]
        if text in heuristic_algos:
            self.app.layout.heuristic_spinner.opacity = 1
            self.app.layout.heuristic_spinner.disabled = False
        else:
            self.app.layout.heuristic_spinner.opacity = 0
            self.app.layout.heuristic_spinner.disabled = True
            self.app.layout.heuristic_spinner.text = "Choose the heuristic"

    # ------------------------
    # Play principal
    # ------------------------
    def on_play_button_press(self, instance):
        selected_algorithm = self.app.layout.algo_spinner.text
        if selected_algorithm == "Choose the algorithm":
            self.app.show_popup("Error", "Please select an algorithm first.")
            return

        if self.is_animating:
            self.app.show_popup("Info", "Animation is already running. Please wait.")
            return

        self.app.layout.play_button.text = "Solving..."
        self.app.layout.play_button.disabled = True

        Clock.schedule_once(lambda dt: self.solve_puzzle(selected_algorithm), 0.1)

    def solve_puzzle(self, algorithm_name):
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
                    solution_path, expanded_nodes = solve_puzzle(
                        self.problem, algorithm_name, heuristic=heuristic_func
                    )
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
            if solution_path and all(hasattr(node.state, 'tiles') for node in solution_path):
                self.solution_steps = solution_path
                self.current_step_index = 0
                self.metrics.set(
                    algoritmo=algorithm_name,
                    heuristica=heuristic if heuristic_func else None,
                    solucion_encontrada=True,
                    pasos=len(solution_path) - 1,
                    nodos_expandidos=expanded_nodes,
                    tiempo=round(elapsed_time, 4)
                )
                self.start_animation()
            else:
                self.error_solution("No solution found or invalid solution path.")

    # ------------------------
    # Animación con play/pause/step
    # ------------------------
    def start_animation(self):
        if not self.solution_steps:
            return
        self.stop_animation()
        self.is_animating = True
        self.is_paused = False
        self.app.layout.anim_toggle.text = "Pause"
        self.anim_event = Clock.schedule_interval(self._tick, self.anim_speed)

    def _tick(self, dt):
        if self.is_paused:
            return
        if self.current_step_index < len(self.solution_steps):
            state = self.solution_steps[self.current_step_index].state
            self.update_board_ui(state)
            self.current_step_index += 1
        else:
            self.stop_animation()
            self.app.layout.play_button.text = "Again?"
            self.app.layout.play_button.disabled = False
            self.app.display_metrics()

    def toggle_play_pause(self, *_):
        if not self.solution_steps:
            return
        if not self.is_animating:
            self.start_animation()
            return
        self.is_paused = not self.is_paused
        self.app.layout.anim_toggle.text = "Play" if self.is_paused else "Pause"

    def step_forward(self, *_):
        if not self.solution_steps:
            return
        if self.is_animating and not self.is_paused:
            self.toggle_play_pause()
        if self.current_step_index < len(self.solution_steps):
            state = self.solution_steps[self.current_step_index].state
            self.update_board_ui(state)
            self.current_step_index += 1

    def step_back(self, *_):
        if not self.solution_steps:
            return
        if self.is_animating and not self.is_paused:
            self.toggle_play_pause()
        if self.current_step_index >= 2:
            self.current_step_index -= 2
            self.step_forward()

    def on_speed_change(self, slider, value):
        self.anim_speed = max(0.05, float(value))
        if self.anim_event and self.is_animating and not self.is_paused:
            self.anim_event.cancel()
            self.anim_event = Clock.schedule_interval(self._tick, self.anim_speed)

    def stop_animation(self):
        if self.anim_event:
            self.anim_event.cancel()
            self.anim_event = None
        self.is_animating = False
        self.is_paused = False
        self.current_step_index = 0
        if hasattr(self.app.layout, "anim_toggle"):
            self.app.layout.anim_toggle.text = "Play"

    # ------------------------
    # Juego manual
    # ------------------------
    def on_tile_press(self, index):
        if self.is_animating:
            return
        current_state = self.problem.start
        tiles = list(current_state.tiles)
        empty_index = tiles.index(0)
        if self.is_adjacent(index, empty_index):
            tiles[empty_index], tiles[index] = tiles[index], tiles[empty_index]
            new_state = PuzzleState(tiles)
            self.problem.start = new_state
            self.app.layout.reset_board(new_state.tiles)
            if self.is_goal_state(new_state):
                self.app.show_popup("¡Victoria!", "Has resuelto el puzzle.")
                self.app.layout.play_button.text = "Again?"
                self.app.layout.play_button.disabled = False

    def is_adjacent(self, i1, i2):
        x1, y1 = divmod(i1, 3)
        x2, y2 = divmod(i2, 3)
        return abs(x1 - x2) + abs(y1 - y2) == 1

    def is_goal_state(self, state: State) -> bool:
        return self.problem.is_goal(state)

    # ------------------------
    # Utilidades
    # ------------------------
    def update_board_ui(self, state: State):
        self.app.layout.board_layout.clear_widgets()
        for index, tile in enumerate(state.tiles):
            btn = self.app.layout.create_tile(tile, index)
            self.app.layout.board_layout.add_widget(btn)

    def error_solution(self, message):
        self.app.show_popup("Error", message)
        self.app.layout.play_button.text = "Play"
        self.app.layout.play_button.disabled = False

    # ------------------------
    # Comparador de heurísticas
    # ------------------------
    def run_heuristic_comparison(self, *_ , algorithm="A*"):
        cases = [
            ("Manhattan",        manhattan),
            ("Misplaced Tiles",  misplaced),
            ("Linear Conflict",  linear_conflict),
        ]
        rows = []
        for name, h in cases:
            t0 = time.perf_counter()
            try:
                path, expanded = solve_puzzle(self.problem, algorithm, heuristic=h)
                elapsed = time.perf_counter() - t0
                steps = len(path) - 1 if path else None
                rows.append({
                    "Heurística": name,
                    "Tiempo (s)": round(elapsed, 4),
                    "Pasos": steps if steps is not None else "-",
                    "Expandidos": expanded
                })
            except Exception as e:
                rows.append({
                    "Heurística": name,
                    "Tiempo (s)": None,
                    "Pasos": None,
                    "Expandidos": None,
                    "Error": str(e)
                })
        self.app.show_comparison(rows, title=f"Comparación ({algorithm})")
