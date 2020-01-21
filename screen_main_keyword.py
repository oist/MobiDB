from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.tab import MDTabsBase

import config
from kivy.app import App


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenMainKeyword(Screen, BoxLayout, MDTabsBase):
    def btn_event(self):
        logger.debug("screen_main_keyword.py, ScreenMainKeyword, btn_event()")

        try:
            config.keyword = self.ids["keyword"].text
            self.change_screen("wait")
        except ValueError as e:
            print(e)

    def move_filter_screen(self):
        logger.debug("screen_main_keyword.py, ScreenMainKeyword, move_keyword_screen()")

        self.change_screen("search_filter")
        config.isFilter = True
        config.isKeyword = False

    def change_screen(self, name):
        logger.debug("screen_main_keyword.py, ScreenMainKeyword, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
