from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty

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
    submit = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenSearchKeyword, self).__init__(**kwargs)

        Window.bind(on_key_down=self._on_keyboard_down)


    def btn_event(self):
        logger.debug("screen_search_main.py, ScreenSearch, btn_event()")

        try:
            config.keyword = self.ids["keyword"].text
            self.change_screen("wait")
            print(config.keyword)
        except ValueError as e:
            print(e)

    def move_filter_screen(self):
        logger.debug("screen_search_main.py, ScreenSearchFilter, move_keyword_screen()")

        self.change_screen("search_filter")
        config.isFilter = True
        config.isKeyword = False

    def change_screen(self, name):
        logger.debug("screen_search_keyword_main.py, ScreenSearchKeyword, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        app = App.get_running_app()
        if app.sm.current == "search_keyword" and keycode == 40:  # 40 - Enter key pressed
            self.btn_event()
