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
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=10)

        # Título centrado
        title = Label(
            text='[b]Puzzle-IA[/b]',
            markup=True,
            font_size='32sp',
            size_hint=(1, 0.4),
            halign='center',
            valign='middle'
        )

        # Fila de selección de algoritmos
        algo_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.2)
        algo_row.add_widget(Label(text="Algorithm:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),
            size_hint=(0.7, 1)
        )
        self.algo_spinner.bind(text=self.controller.on_algorithm_selected)
        algo_row.add_widget(self.algo_spinner)

        # Fila de selección de heurísticas
        heur_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.2)
        heur_row.add_widget(Label(text="Heuristic:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.heuristic_spinner = Spinner(
            text='Choose the heuristic',
            values=('Manhattan', 'Misplaced Tiles', 'Linear Conflict'),
            size_hint=(0.7, 1),
            opacity=0,
            disabled=True
        )
        heur_row.add_widget(self.heuristic_spinner)

        # Fila de botones (Play, Reset, New)
        buttons_row = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.2, padding=(0, 5))

        self.play_button = Button(
            text='Play',
            size_hint=(0.33, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.play_button.bind(on_press=self.controller.on_play_button_press)

        self.reset_button = Button(
            text='Reset',
            size_hint=(0.33, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.reset_button.bind(on_press=lambda instance: self.controller.app.reset_puzzle())

        self.new_button = Button(
            text='New',
            size_hint=(0.33, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.2, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        self.new_button.bind(on_press=lambda instance: self.controller.app.new_puzzle())

        buttons_row.add_widget(self.play_button)
        buttons_row.add_widget(self.reset_button)
        buttons_row.add_widget(self.new_button)


        # Añadir todo al header
        header_layout.add_widget(title)
        header_layout.add_widget(algo_row)
        header_layout.add_widget(heur_row)
        header_layout.add_widget(buttons_row)

        # ===============================
        # Tablero
        # ===============================
        self.board_layout = GridLayout(
            cols=3,
            rows=3,
            padding=5,
            spacing=5,
            size_hint_y=0.65
        )

        for index, tile in enumerate(initial_state):
            self.board_layout.add_widget(self.create_tile(tile, index))

        # ===============================
        # Estructura general
        # ===============================
        self.add_widget(header_layout)
        self.add_widget(self.board_layout)

    # -------------------------------
    # Helpers
    # -------------------------------
    def create_tile(self, value: int, index: int):
        """Crea un botón para representar una celda del puzzle."""
        btn = Button(
            text='' if value == 0 else str(value),
            font_size='36sp',
            background_normal='',
            background_color=(0, 0, 0, 0) if value == 0 else (0.2, 0.4, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        btn.bind(on_press=lambda inst: self.controller.on_tile_press(index))
        return btn

    def reset_board(self, new_state):
        """Reinicia el tablero con un nuevo estado."""
        self.board_layout.clear_widgets()
        for index, tile in enumerate(new_state):
            self.board_layout.add_widget(self.create_tile(tile, index))