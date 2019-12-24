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


class Keyword(BoxLayout, MDTabsBase):
    pass
