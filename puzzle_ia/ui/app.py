from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from core.create_puzzle import create_state
from core.problem import Puzzle
from metrics.evaluator import Metrics
from controllers.puzzle_controller import PuzzleController
from ui.layouts import PuzzleLayout

import matplotlib

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
        self.controller.problem = Puzzle(self.initial_state)
        self.layout.reset_board(self.initial_state)

    def show_comparison(self, rows, title="Comparación de heurísticas"):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ----- Tabla -----
        headers = ["Heurística", "Tiempo (s)", "Pasos", "Expandidos"]
        table = GridLayout(cols=len(headers), size_hint_y=None, spacing=5, padding=5)
        table.bind(minimum_height=table.setter('height'))

        # Cabecera
        for h in headers:
            table.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        # Filas
        for r in rows:
            table.add_widget(Label(text=str(r.get("Heurística", "")), size_hint_y=None, height=28))
            table.add_widget(Label(text=str(r.get("Tiempo (s)", "")), size_hint_y=None, height=28))
            table.add_widget(Label(text=str(r.get("Pasos", "")), size_hint_y=None, height=28))
            table.add_widget(Label(text=str(r.get("Expandidos", "")), size_hint_y=None, height=28))

        scroll = ScrollView(size_hint=(1, 0.45))
        scroll.add_widget(table)
        content.add_widget(scroll)

        # ----- Gráfico (opcional con matplotlib) -----
        try:
            import os, tempfile
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            labels = [r["Heurística"] for r in rows if r.get("Tiempo (s)") is not None]
            times  = [r["Tiempo (s)"] for r in rows if r.get("Tiempo (s)") is not None]

            if labels and times:
                plt.figure()
                plt.bar(labels, times)
                plt.title("Tiempo por heurística (A*)")
                plt.ylabel("Segundos")
                plt.tight_layout()

                out_path = os.path.join(tempfile.gettempdir(), "heuristics_cmp.png")
                plt.savefig(out_path)
                plt.close()

                img = Image(source=out_path, size_hint=(1, 0.45), allow_stretch=True, keep_ratio=True)
                content.add_widget(img)
            else:
                content.add_widget(Label(text="No se pudo crear el gráfico (datos vacíos).", size_hint=(1, 0.45)))

        except Exception as e:
            content.add_widget(Label(text=f"No se pudo crear el gráfico: {e}", size_hint=(1, 0.45)))

        popup = Popup(title=title, content=content, size_hint=(0.92, 0.92))
        popup.open()