from kivy.config import Config
Config.set('input', 'mtdev_%(name)s', '')

from ui.app import PuzzleApp

if __name__ == '__main__':
    PuzzleApp().run()
