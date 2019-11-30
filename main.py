import json
from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import time
import config
import webbrowser

from logging import getLogger, StreamHandler, DEBUG

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("main Begin")


class MobiApp(App):
    def build(self):
        logger.debug("App Begin")

        logger.debug("App End")
        return sm


if __name__ == "__main__":
    logger.debug("main Begin")

    # kvファイルをstring型としてload
    with open("./theme2.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (800, 600)
    sm = ScreenManager()  # スクリーンマネージャ
    MobiApp().run()

    logger.debug("main End")
