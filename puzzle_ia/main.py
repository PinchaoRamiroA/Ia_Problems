from core.create_puzzle import create_state
from core.problem import Puzzle
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.popup import Popup

kivy.require('1.9.0')

class PuzzleApp(App):
    def build(self, board: Puzzle):
        # Layout principal de la aplicación
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=20)

        # Contenedor para la cabecera (título)
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.5)

        # Contenedor de los controles
        controls_layout = BoxLayout(orientation='horizontal', size_hint_y=0.5)

        # Título de la aplicación
        title = Label(text='Puzzle-IA', font_size='24sp', size_hint_x=0.8, halign='left')

        # Espacio de separación
        header_layout.add_widget(Label(size_hint_x=0.1))

        # Botón para escoger el algoritmo (Spinner)
        self.algo_spinner = Spinner(
            text='Choose the algorithm',
            values=('BFS', 'DFS', 'UCS', 'Greedy', 'A*', 'Weighted A*', 'IDA*'),  # Aquí puedes poner los nombres de tus algoritmos
            size_hint=(0.7, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.algo_spinner.bind(text=self.on_algorithm_selected)
        
        # Botón para iniciar el puzzle
        play_button = Button(text='play', size_hint=(0.2, 0.8), font_size='32sp')
        play_button.bind(on_press=self.on_play_button_press)

        # Añadir widgets al layout de los controles
        controls_layout.add_widget(self.algo_spinner)
        controls_layout.add_widget(play_button)

        # Tablero del puzzle (GridLayout de 3x3)
        self.board_layout = GridLayout(cols=3, rows=3, padding=5, spacing=5, size_hint_y=0.6)
        
        # Crear los 9 cuadros del tablero
        for i in range(9):
            cell = Button(text=str(i + 1), font_size='36sp') # Puedes inicializarlo como quieras
            self.board_layout.add_widget(cell)

        # Añadir todos los layouts al layout principal
        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.board_layout)

        return main_layout

    def on_algorithm_selected(self, spinner, text):
        # Función para manejar la selección de un algoritmo
        print(f"Algorithm selected: {text}")
        # Aquí puedes implementar la lógica para el algoritmo escogido
    
    def on_play_button_press(self, instance):
        # Función para manejar el clic en el botón de Play
        selected_algorithm = self.algo_spinner.text
        if selected_algorithm == "Choose the algorithm":
            self.show_popup("Error", "Please select an algorithm first.")
            return

        print(f"Starting the puzzle with algorithm: {selected_algorithm}")
        # Aquí puedes implementar la lógica para resolver el puzzle
        
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()


if __name__ == '__main__':
    initial = create_state()
    problem = Puzzle(initial)
    PuzzleApp(problem).run()
