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


class ScreenSearchKeyword(Screen, BoxLayout, MDTabsBase):
    def check_event(self, text, active):
        logger.debug("screen_search_keyword_main.py, ScreenSearchKeyword, check_event()")

        if text == "Filter":
            if active:
                self.change_screen("search_filter")

    def change_screen(self, name):
        logger.debug("screen_search_keyword_main.py, ScreenSearchKeyword, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
