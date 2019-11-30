from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen
import config
from kivy.app import App

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenSearch(Screen):
    def btn_event(self):
        logger.debug("screen_search_main.py, ScreenSearch, btn_event()")

        try:
            config.threshold_val = self.make_sure_text(self.ids["th_val"].text)
            config.threshold_len = int(self.make_sure_text(self.ids["th_len"].text))
            config.fill_gap = int(self.make_sure_text(self.ids["fill_gap"].text))

            self.change_screen("wait")
        except ValueError as e:
            print(e)

    def make_sure_text(self, ss_text):
        logger.debug("screen_search_main.py, ScreenSearch, make_sure_text()")

        if ss_text == "":
            return 0
        else:
            return float(ss_text.replace('"', ''))

    def change_screen(self, name):
        logger.debug("screen_search_main.py, ScreenSearch, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
