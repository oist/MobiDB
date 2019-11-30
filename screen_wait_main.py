from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen

from screen_wait_search import SearchScore
import init
"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenWait(Screen):
    def on_enter(self):
        logger.debug("screen_wait_main.py, ScreenWait, on_enter()")

        # 閾値とsocreを比較し、条件に当てはまるものを検索する
        ss = SearchScore()
        ss.start()

    def btn_event(self):
        logger.debug("screen_wait_main.py, ScreenWait, btn_event()")

        # cancelボタンが押されたらsearch画面の値を初期化して戻る
        init.init()
        self.change_screen("search")

