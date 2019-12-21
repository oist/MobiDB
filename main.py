import sys
from logging import getLogger, StreamHandler, DEBUG

from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp


from menu_tab import Menu
from result_tab import Result


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class MainApp(MDApp):
    def __init__(self, **kwargs):
        logger.debug("main.py, MainApp, __init__()")
        self.title = "MobiDB - Human"
        self.theme_cls.primary_palette = "Indigo"

        super().__init__(**kwargs)

    def build(self):
        logger.debug("main.py, MainApp, build()")

        with open("./theme.kv", "r", encoding="utf8") as f:
            screen = Builder.load_string(f.read())

        self.root = self.create_tab(screen, "Menu", "Result")

    def exit(self):
        logger.debug("main.py, MainApp, exit()")
        sys.exit(1)

    def create_tab(self, screen, name1, name2):
        logger.debug("main.py, MainApp, create_tab()")
        tab = Menu(text=name1)
        screen.ids.tabs.add_widget(tab)

        tab = Result(text=name2)
        screen.ids.tabs.add_widget(tab)

        return screen


if __name__ == "__main__":

    Window.size = (728, 450)
    MainApp().run()
