from logging import getLogger, StreamHandler, DEBUG
import config
from kivy.factory import Factory

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class SearchData:

    def __init__(self):
        self.root = Factory.ScreenSearch()

    def get_text(self):
        logger.debug("screen_search_main.py, ScreenSearch, btn_event()")
        self.root = Factory.ScreenSearch()

        try:
            config.threshold_val = self.substitute_text(self.root.ids["th_val"].text)
            config.threshold_len = int(self.substitute_text(self.root.ids["th_len"].text))
            config.fill_gap = int(self.substitute_text(self.root.ids["fill_gap"].text))

        except ValueError as e:
            print(e)

    def substitute_text(self, ss_text):
        logger.debug("screen_search_main.py, ScreenSearch, make_sure_text()")

        if ss_text == "":
            return 0
        else:
            return float(ss_text.replace('"', ''))