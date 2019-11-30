from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.app import App

sm = ScreenManager()
"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("screen_top_main Begin")


class ScreenTop(Screen):
    """Top画面"""

    def btn_event(self):
        logger.debug("ST_btn_event Begin")
        app = App.get_running_app()
        app.sm.current = "search"
