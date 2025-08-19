from controllers.puzzle_controller import PuzzleController
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label


class PuzzleLayout(BoxLayout):
    def __init__(self, controller, initial_state, **kwargs):
        super().__init__(orientation='vertical', padding=25, spacing=20, **kwargs)
        self.controller: PuzzleController = controller

        # ===============================
        # Cabecera
        # ===============================
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10)

        # Título centrado
        title = Label(
            text='[b]Puzzle-IA[/b]',
            markup=True,
            font_size='32sp',
            size_hint=(1, 0.5),
            halign='center',
            valign='middle'
        )

        # Fila de selección de algoritmos
        algo_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.25)
        algo_row.add_widget(Label(text="Algorithm:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),
            size_hint=(0.7, 1)
        )
        self.algo_spinner.bind(text=self.controller.on_algorithm_selected)
        algo_row.add_widget(self.algo_spinner)

        # Fila de selección de heurísticas
        heur_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.25)
        heur_row.add_widget(Label(text="Heuristic:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.heuristic_spinner = Spinner(
            text='Choose the heuristic',
            values=('Manhattan', 'Misplaced Tiles', 'Linear Conflict'),
            size_hint=(0.7, 1),
            opacity=0,
            disabled=True
        )
        heur_row.add_widget(self.heuristic_spinner)

        # Botón de ejecución (centrado)
        play_row = BoxLayout(orientation='horizontal', size_hint_y=0.25, padding=(0, 10))
        self.play_button = Button(
            text='play',
            size_hint=(0.5, 1),
            font_size='24sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.play_button.bind(on_press=self.controller.on_play_button_press)
        play_row.add_widget(Label(size_hint=(0.25, 1)))  # Espaciador
        play_row.add_widget(self.play_button)
        play_row.add_widget(Label(size_hint=(0.25, 1)))  # Espaciador

        # Añadir todo al header
        header_layout.add_widget(title)
        header_layout.add_widget(algo_row)
        header_layout.add_widget(heur_row)
        header_layout.add_widget(play_row)

        # ===============================
        # Tablero
        # ===============================
        self.board_layout = GridLayout(
            cols=3,
            rows=3,
            padding=5,
            spacing=5,
            size_hint_y=0.7
        )

        for tile in initial_state:
            self.board_layout.add_widget(self.create_tile(tile))

        # ===============================
        # Estructura general
        # ===============================
        self.add_widget(header_layout)
        self.add_widget(self.board_layout)

    # -------------------------------
    # Helpers
    # -------------------------------
    def create_tile(self, value: int) -> Button:
        """Crea un botón para representar una celda del puzzle."""
        if value == 0:
            return Button(
                text='',
                font_size='36sp',
                background_normal='',
                background_color=(0.8, 0.8, 0.8, 1)  # gris claro para el espacio vacío
            )
        return Button(
            text=str(value),
            font_size='36sp',
            background_normal='',
            background_color=(0.2, 0.4, 0.8, 1),  # azul para piezas
            color=(1, 1, 1, 1)  # texto blanco
        )
