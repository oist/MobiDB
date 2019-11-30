import json
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from application import MobiApp
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import time
import config
import webbrowser
from screen_top_main import ScreenTop
from screen_search_main import ScreenSearch
from screen_wait_main import ScreenWait
from screen_out_main import ScreenOut

from logging import getLogger, StreamHandler, DEBUG

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("main Begin")


if __name__ == "__main__":
    logger.debug("main Begin")

    # kvファイルをstring型としてload
    with open("./theme2.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (800, 600)

    MobiApp().run()

    logger.debug("main End")
