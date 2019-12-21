import sys
from logging import getLogger, StreamHandler, DEBUG

from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast

from load_text import Load
from search_data import SearchData


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
        self.title = "MobiDB -Human"
        self.theme_cls.primary_palette = "Blue"
        self.sd = SearchData()
        self.load = Load()
        super().__init__(**kwargs)

    def build(self):
        logger.debug("main.py, MainApp, build()")
        with open("./theme.kv", "r", encoding="utf8") as f:
            self.root = Builder.load_string(f.read())

    def exit(self):
        logger.debug("main.py, MainApp, exit()")
        sys.exit(1)

    def btn_event(self):
        logger.debug("main.py, MainApp, btn_event()")
        self.load.load_text(self.root.ids["th_val"].text, self.root.ids["th_len"].text, self.root.ids["fill_gap"].text)

        self.sd = SearchData()
        self.sd.start()

    def show_toast(self):
        logger.debug("main.py, MainApp, show_toast()")
        toast("Load is Successed")


if __name__ == "__main__":

    Window.size = (647, 400)
    MainApp().run()
