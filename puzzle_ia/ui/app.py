from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from core.create_puzzle import create_state
from core.problem import Puzzle
from metrics.evaluator import Metrics
from controllers.puzzle_controller import PuzzleController
from ui.layouts import PuzzleLayout

class PuzzleApp(App):
    def build(self):
        initial_state = create_state()
        problem: Puzzle = Puzzle(initial_state)
        self.metrics = Metrics()
        self.controller = PuzzleController(self, problem, self.metrics)
        self.layout = PuzzleLayout(self.controller, initial_state)
        return self.layout

    def display_metrics(self):
        self.show_popup("Métricas de Solución", self.metrics.get_metrics_string())

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, halign='center', valign='middle'), size_hint=(0.8, 0.4))
        popup.open()
