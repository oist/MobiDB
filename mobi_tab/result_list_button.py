from logging import getLogger, StreamHandler, DEBUG

from kivy.uix.boxlayout import BoxLayout

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ResultButton(BoxLayout):
    pass