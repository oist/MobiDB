from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


sm = ScreenManager()


class ScreenTop(Screen):
    def btn_event(self):
        logger.debug("screen_top_main.py, ScreenTop, btn_event()")

        self.change_screen("search")

    def change_screen(self, name):
        logger.debug("screen_top_main.py, ScreenTop, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
