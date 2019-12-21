from logging import getLogger, StreamHandler, DEBUG
from menu_search_data import SearchData
from menu_load_text import Load

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Menu(BoxLayout, MDTabsBase):
    def __init__(self, **kwargs):
        logger.debug("menu_tab.py, Menu, __init__()")
        super().__init__(**kwargs)

        self.sd = SearchData()
        self.load = Load()

    def btn_event(self):
        logger.debug("menu_tab.py, Menu, btn_event()")

        self.load.load_text(self.ids["th_val"].text, self.ids["th_len"].text, self.ids["fill_gap"].text)
        self.sd.start()