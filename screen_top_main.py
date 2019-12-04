from logging import getLogger
from kivy.uix.screenmanager import Screen
from kivy.app import App


logger = getLogger(__name__)


class ScreenTop(Screen):
    """
    app.sm.current == "top"　時の処理

    Parameters
    ----------
    app : class application.MobiApp
        現在の app の情報を取得
    app.sm.current(self, name = "search")　: str
        表示するスクリーンを name = "search" にする

    Notes
    ----------
    Button イベントは theme.ScreenTopに記載されている。

    """
    def btn_event(self):
        logger.debug("screen_top_main.py, ScreenTop, btn_event()")

        self.change_screen("search")

    def change_screen(self, name):
        logger.debug("screen_top_main.py, ScreenTop, change_screen()")

        app = App.get_running_app()
        app.sm.current = name