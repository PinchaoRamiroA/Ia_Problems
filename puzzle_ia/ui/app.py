from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from core.create_puzzle import create_state
from core.problem import Puzzle
from metrics.evaluator import Metrics
from controllers.puzzle_controller import PuzzleController
from ui.layouts import PuzzleLayout

class PuzzleApp(App):
    def build(self):
        self.initial_state = create_state()
        problem: Puzzle = Puzzle(self.initial_state)
        self.metrics = Metrics()
        self.controller = PuzzleController(self, problem, self.metrics)
        self.layout = PuzzleLayout(self.controller, self.initial_state)
        return self.layout

    def display_metrics(self):
        self.show_popup("Métricas de Solución", self.metrics.get_metrics_string())

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        label = Label(text=message, halign='center', valign='middle')
        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        
        content.add_widget(label)
        content.add_widget(close_btn)

        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def save_metrics(self, filename="metrics.txt"):
        with open(filename, "a") as f:
            f.write(self.metrics.get_metrics_string() + "\n")

    def reset_puzzle(self):
        """Restaura el tablero al estado inicial actual."""
        self.controller.problem.start = self.controller.problem.__class__(self.initial_state).start
        self.layout.reset_board(self.initial_state)

    def new_puzzle(self):
        """Crea un nuevo tablero y lo establece como estado inicial."""
        self.initial_state = create_state()
        self.controller.problem = Puzzle(self.initial_state)  # reemplazar el problema con nuevo inicio
        self.layout.reset_board(self.initial_state)



