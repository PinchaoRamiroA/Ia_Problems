from controllers.puzzle_controller import PuzzleController
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class PuzzleLayout(BoxLayout):
    def __init__(self, controller, initial_state, **kwargs):
        super().__init__(orientation='vertical', padding=25, spacing=20, **kwargs)
        self.controller: PuzzleController = controller

        # ===============================
        # Cabecera
        # ===============================
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=12)

        # Título
        title = Label(
            text='[b]Puzzle-IA[/b]',
            markup=True,
            font_size='32sp',
            size_hint=(1, 0.3),
            halign='center',
            valign='middle'
        )

        # Selección de algoritmo
        algo_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        algo_row.add_widget(Label(text="Algorithm:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),
            size_hint=(0.7, 1)
        )
        self.algo_spinner.bind(text=self.controller.on_algorithm_selected)
        algo_row.add_widget(self.algo_spinner)

        # Selección de heurística
        heur_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        heur_row.add_widget(Label(text="Heuristic:", size_hint=(0.3, 1), halign="right", valign="middle"))

        self.heuristic_spinner = Spinner(
            text='Choose the heuristic',
            values=('Manhattan', 'Misplaced Tiles', 'Linear Conflict'),
            size_hint=(0.7, 1),
            opacity=0,
            disabled=True
        )
        heur_row.add_widget(self.heuristic_spinner)

        # Botones principales
        buttons_row = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.2)

        self.play_button = Button(
            text='Solve',
            size_hint=(0.25, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.play_button.bind(on_press=self.controller.on_play_button_press)

        self.reset_button = Button(
            text='Reset',
            size_hint=(0.25, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.reset_button.bind(on_press=lambda inst: self.controller.app.reset_puzzle())

        self.new_button = Button(
            text='New',
            size_hint=(0.25, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.2, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        self.new_button.bind(on_press=lambda inst: self.controller.app.new_puzzle())

        self.compare_button = Button(
            text='Compare',
            size_hint=(0.25, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.6, 0.4, 0.1, 1),
            color=(1, 1, 1, 1)
        )
        self.compare_button.bind(on_press=self.controller.run_heuristic_comparison)

        buttons_row.add_widget(self.play_button)
        buttons_row.add_widget(self.reset_button)
        buttons_row.add_widget(self.new_button)
        
        compare_row = BoxLayout(orientation = 'horizontal', spacing=10, size_hint_y=0.2)
        self.compare_button = Button(
            text='Compare',
            size_hint=(0.25, 1),
            font_size='20sp',
            background_normal='',
            background_color=(0.6, 0.4, 0.1, 1),
            color=(1, 1, 1, 1)
        )
        self.compare_button.bind(on_press=self.controller.run_heuristic_comparison)
        compare_row.add_widget(self.compare_button)

        # Controles de animación
        anim_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.2)

        self.step_back_btn = Button(text='<-', size_hint=(0.12, 1))
        self.step_back_btn.bind(on_press=self.controller.step_back)

        self.anim_toggle = Button(text='Play', size_hint=(0.2, 1))
        self.anim_toggle.bind(on_press=self.controller.toggle_play_pause)

        self.step_forward_btn = Button(text='->', size_hint=(0.12, 1))
        self.step_forward_btn.bind(on_press=self.controller.step_forward)

        speed_lbl = Label(text='Speed', size_hint=(0.12, 1))
        self.speed_slider = Slider(min=0.05, max=1.5, value=0.5, step=0.05, size_hint=(0.44, 1))
        self.speed_slider.bind(value=self.controller.on_speed_change)

        anim_row.add_widget(self.step_back_btn)
        anim_row.add_widget(self.anim_toggle)
        anim_row.add_widget(self.step_forward_btn)
        anim_row.add_widget(speed_lbl)
        anim_row.add_widget(self.speed_slider)

        # Añadir todo al header
        header_layout.add_widget(title)
        header_layout.add_widget(algo_row)
        header_layout.add_widget(heur_row)
        header_layout.add_widget(buttons_row)
        header_layout.add_widget(compare_row)
        header_layout.add_widget(anim_row)

        # ===============================
        # Tablero
        # ===============================
        self.board_layout = GridLayout(
            cols=3,
            rows=3,
            padding=5,
            spacing=5,
            size_hint_y=0.6
        )
        self.reset_board(initial_state)

        # ===============================
        # Layout principal
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