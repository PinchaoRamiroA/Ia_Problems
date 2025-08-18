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

# Asume que estas clases están en los archivos core/
# El código para estas clases se mantuvo en el hilo de conversación anterior
from core.create_puzzle import create_state
from core.problem import Puzzle
from core.abstracts import State
from core.heuristics import manhattan, misplaced, linear_conflict
from core.algorithms import BFS, DFS, UCS, Greedy, A_star, IDA_star, Weighted_A_star

kivy.require('1.9.0')


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
    elif algorithm == "IDA*":
        return IDA_star(problem, heuristic)
    else:
        raise ValueError("Algoritmo no soportado")
    
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

    def build(self):
        """
        Este método es llamado por Kivy para construir la interfaz de usuario.
        No recibe argumentos.
        """
        # Creación del problema inicial
        initial_state = create_state()
        self.problem = Puzzle(initial_state)

        # Layout principal de la aplicación (vertical)
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=20)

        # Contenedor para la cabecera (título y controles)
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        
        # Fila del título
        title_row = BoxLayout(orientation='horizontal')
        title = Label(text='Puzzle-IA', font_size='24sp', size_hint_x=0.8, halign='left')
        title_row.add_widget(title)
        
        # Fila de los controles
        controls_row = BoxLayout(orientation='horizontal', spacing=10)
        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),  # Actualizado con todos los algoritmos
            size_hint=(0.7, 1)
        )
        self.algo_spinner.bind(text=self.on_algorithm_selected)
        
        self.play_button = Button(text='▶', size_hint=(0.3, 1), font_size='32sp')
        self.play_button.bind(on_press=self.on_play_button_press)

        controls_row.add_widget(self.algo_spinner)
        controls_row.add_widget(self.play_button)
        
        header_layout.add_widget(title_row)
        header_layout.add_widget(controls_row)

        # Tablero del puzzle (GridLayout de 3x3)
        self.board_layout = GridLayout(cols=3, rows=3, padding=5, spacing=5, size_hint_y=0.8)
        
        # Inicializa el tablero con el estado inicial del puzzle
        self.update_board_ui(self.problem.initial_state())

        # Añadir todos los layouts al layout principal
        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.board_layout)
        
        return main_layout

    def on_algorithm_selected(self, spinner, text):
        """Se activa cuando se selecciona un algoritmo del Spinner."""
        print(f"Algorithm selected: {text}")

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
        
        try:
            # Los algoritmos A* y otros necesitan una heurística.
            if algorithm_name in ["A*", "Greedy", "Weighted A*", "IDA*"]:
                # Asume que manhattan_distance está implementado en core.algorithms
                solution_path, extended = solve_puzzle(self.problem, algorithm_name, heuristic=manhattan)
            else:
                solution_path, extended = solve_puzzle(self.problem, algorithm_name)
        except ValueError as e:
            self.show_popup("Error", str(e))
            self.play_button.text = "▶"
            self.play_button.disabled = False
            return
            
        if solution_path:
            print("Solution found!")
            self.solution_steps = solution_path
            self.current_step_index = 0
            self.is_animating = True
            self.play_button.text = "Animating..."
            # Inicia la animación en la UI
            self.animation_event = Clock.schedule_interval(self.animate_solution, 0.5)
        else:
            self.show_popup("Error", "No solution found for this puzzle state.")
            self.play_button.text = "▶"
            self.play_button.disabled = False

    def animate_solution(self, dt):
        """
        Actualiza la UI para mostrar el siguiente paso de la solución.
        """
        if self.current_step_index < len(self.solution_steps):
            state_to_display = self.solution_steps[self.current_step_index]
            self.update_board_ui(state_to_display)
            self.current_step_index += 1
        else:
            # Detiene la animación cuando se ha mostrado toda la solución
            if self.animation_event:
                self.animation_event.cancel()
            self.is_animating = False
            self.play_button.text = "Done"
            self.play_button.disabled = False
            self.show_popup("Success", "Puzzle solved!")

    def update_board_ui(self, state: State):
        """
        Actualiza el tablero de la UI con los valores de un estado dado.
        """
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

    def show_popup(self, title, message):
        """Muestra una ventana emergente."""
        popup = Popup(title=title, content=Label(text=message, halign='center', valign='middle'), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    PuzzleApp().run()
