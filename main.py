import sys
from logging import getLogger, StreamHandler, DEBUG

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ObservableList, ObjectProperty, ListProperty, Property
from kivymd.app import MDApp

from filter_main import Filter
from result_main import Result
from keyword_main import Keyword
import config


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class MainApp(MDApp):
    tab = ObjectProperty()
    tab_bar = ObjectProperty()

    def __init__(self, **kwargs):
        logger.debug("main.py, MainApp, __init__()")
        self.title = "MobiDB - Human"
        self.theme_cls.primary_palette = "Indigo"
        self.result = Result



        super().__init__(**kwargs)

    def build(self):
        logger.debug("main.py, MainApp, build()")

        with open("./theme.kv", "r", encoding="utf8") as f:
            screen = Builder.load_string(f.read())
            self.root = self.create_tab(screen)

    def exit(self):
        logger.debug("main.py, MainApp, exit()")
        sys.exit(1)

    def create_tab(self, screen):
        logger.debug("main.py, MainApp, create_tab()")

        name_list = ["Keyword", "Filter", "Result"]
        list_len = len(name_list)

        for i in range(list_len):
            if i == 0:
                tab = Keyword(text=name_list[i])
            elif i == 1:
                tab = Filter(text=name_list[i])
            else:
                tab = Result(text=name_list[i])

            screen.ids.tabs.add_widget(tab)

        return screen

    def p(self, ed_self):

        print(ed_self)


if __name__ == "__main__":
    Window.size = (728, 450)
    MainApp().run()
