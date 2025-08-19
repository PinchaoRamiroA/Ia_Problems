import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import time

from core.create_puzzle import create_state
from core.problem import Puzzle
from core.abstracts import State
from core.heuristics import manhattan, misplaced, linear_conflict

from ui.dispatcher import solve_puzzle
from metrics.evaluator import Metrics
    
class PuzzleApp(App):
    def __init__(self, **kwargs):
        """
        Constructor de la aplicación.
        Aquí inicializamos los atributos de la instancia.
        """
        super().__init__(**kwargs)
        self.problem = None
        self.solution_steps = []
        self.current_step_index = 0
        self.animation_event = None
        self.is_animating = False
        self.metrics : Metrics = Metrics()

    def build(self):
        # Creación del problema inicial
        initial_state = create_state()
        self.problem = Puzzle(initial_state)

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=20)

        # Cabecera
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        
        title_row = BoxLayout(orientation='horizontal')
        title = Label(text='Puzzle-IA', font_size='24sp', size_hint_x=0.8, halign='left')
        title_row.add_widget(title)
        
        controls_row = BoxLayout(orientation='horizontal', spacing=10)

        # Spinner de algoritmos
        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),
            size_hint=(0.7, 1)
        )
        # Evento para mostrar/ocultar heurísticas
        self.algo_spinner.bind(text=self.on_algorithm_selected)

        # Spinner de heurísticas (inicialmente oculto)
        self.heuristic_spinner = Spinner(
            text='Choose the heuristic',
            values=('Manhattan', 'Misplaced Tiles', 'Linear Conflict'),
            size_hint=(0.7, 1)
        )
        self.heuristic_spinner.opacity = 0
        self.heuristic_spinner.disabled = True

        # Botón play
        self.play_button = Button(text='▶', size_hint=(0.3, 1), font_size='32sp')
        self.play_button.bind(on_press=self.on_play_button_press)

        controls_row.add_widget(self.algo_spinner)
        controls_row.add_widget(self.heuristic_spinner)
        controls_row.add_widget(self.play_button)
        
        header_layout.add_widget(title_row)
        header_layout.add_widget(controls_row)

        # Tablero
        self.board_layout = GridLayout(cols=3, rows=3, padding=5, spacing=5, size_hint_y=0.8)
        self.update_board_ui(self.problem.initial_state())

        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.board_layout)
        
        return main_layout

    def on_algorithm_selected(self, spinner, text):
        """Muestra u oculta el selector de heurísticas según el algoritmo elegido."""
        heuristic_algos = ["A*", "Greedy", "Weighted A*", "IDA*"]
        if text in heuristic_algos:
            self.heuristic_spinner.opacity = 1
            self.heuristic_spinner.disabled = False
        else:
            self.heuristic_spinner.opacity = 0
            self.heuristic_spinner.disabled = True
            self.heuristic_spinner.text = "Choose the heuristic"

    def on_play_button_press(self, instance):
        """Se activa al presionar el botón de Play."""
        selected_algorithm = self.algo_spinner.text
        if selected_algorithm == "Choose the algorithm":
            self.show_popup("Error", "Please select an algorithm first.")
            return

        if self.is_animating:
            self.show_popup("Info", "Animation is already running. Please wait.")
            return

        self.play_button.text = "Solving..."
        self.play_button.disabled = True
        
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
            heuristic_name = self.heuristic_spinner.text
            heuristic_func = None
            if heuristic_name == "Manhattan":
                heuristic_func = manhattan
            elif heuristic_name == "Misplaced Tiles":
                heuristic_func = misplaced
            elif heuristic_name == "Linear Conflict":
                heuristic_func = linear_conflict
            
            if algorithm_name in ["A*", "Greedy", "Weighted A*", "IDA*"]:
                if heuristic_func:
                    solution_path, expanded_nodes = solve_puzzle(self.problem, algorithm_name, heuristic=heuristic_func)
                else:
                    self.show_popup("Error", "Please select a heuristic for this algorithm.")
                    self.play_button.text = "▶"
                    self.play_button.disabled = False
                    return
            else:
                solution_path, expanded_nodes = solve_puzzle(self.problem, algorithm_name)
            
            elapsed_time = time.time() - start_time
        except ValueError as e:
            self.show_popup("Error", str(e))
        except Exception as e:
            self.show_popup("Error", f"An unexpected error occurred: {e}")
        finally:
            if solution_path is not None and isinstance(solution_path, (list, tuple)):
                if solution_path:
                    # Validar que los elementos en la solución sean del tipo correcto
                    if all(hasattr(node.state, 'tiles') for node in solution_path):
                        self.solution_steps = solution_path
                        self.current_step_index = 0
                        self.is_animating = True
                        self.play_button.text = "Animating..."
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
                self.show_popup("Error", "No solution found or returned value is not a list of states.")
                self.play_button.text = "▶"
                self.play_button.disabled = False

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
            self.play_button.text = "Done"
            self.play_button.disabled = False
            self.display_metrics()

    def update_board_ui(self, state: State):
        """
        Actualiza el tablero de la UI con los valores de un estado dado.
        """
        # La validación ahora es redundante si se corrige animate_solution,
        # pero es buena práctica mantenerla.
        if not hasattr(state, 'tiles'):
            print("Error: El objeto de estado no tiene el atributo 'tiles'.")
            return
            
        # Limpia el tablero actual
        self.board_layout.clear_widgets()
        
        # Llena el tablero con los nuevos valores
        for tile in state.tiles:
            # Los botones que representan el espacio vacío pueden tener un estilo diferente
            if tile == 0:
                btn = Button(text='', font_size='36sp', background_color=(0, 0, 0, 0))
            else:
                btn = Button(text=str(tile), font_size='36sp')
            self.board_layout.add_widget(btn)

    def display_metrics(self):
        """Muestra las métricas de la solución en un popup."""
        self.show_popup("Métricas de Solución", self.metrics.get_metrics_string())

    def show_popup(self, title, message):
        """Muestra una ventana emergente."""
        popup = Popup(title=title, content=Label(text=message, halign='center', valign='middle'), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    PuzzleApp().run()
