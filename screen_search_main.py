from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen
"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("screen_search_main Begin")


class ScreenSearch(Screen):
    """Top画面"""
    pass