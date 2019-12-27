from logging import getLogger, StreamHandler, DEBUG
from filter_search_data import SearchData
from filter_load_text import Load

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Filter(BoxLayout, MDTabsBase):
    def __init__(self, **kwargs):
        logger.debug("filter_main.py, Filter, __init__()")
        super().__init__(**kwargs)

        self.sd = SearchData()
        self.load = Load()

    def btn_event(self):
        logger.debug("filter_main.py, Filter, btn_event()")

        self.load.load_text(self.ids["th_val"].text, self.ids["th_len"].text, self.ids["fill_gap"].text)
        self.sd.start()