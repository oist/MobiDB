from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen_top_main import ScreenTop
from screen_search_main import ScreenSearch
from screen_wait_main import ScreenWait
from screen_out_main import ScreenOut


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class MobiApp(App):

    """
    Build app and add screen

    Parameters
    ----------
    sm : class kivy.uix.screenmanager.ScreenManager
        アプリケーションの複数画面を管理する。画面を生成し、追加することで構築できる。
        一番最初にaddしたscreenがそのまま表示される

    Methods
    ----------
    add_screen(self)
        ScreenManagerにscreenを追加する。
    
    Examples
    ----------
    sm.add_widget(class name(name="screen name"))

    Notes
    ----------
    ScreenManagerの詳細は以下のURL
    https://pyky.github.io/kivy-doc-ja/api-kivy.uix.screenmanager.html

    """
    sm = ScreenManager()

    def build(self):
        logger.debug("application.py, App, build()")

        # 画面をScreenManagerに追加する
        self.add_screen()

        return MobiApp.sm

    def add_screen(self):
        logger.debug("application.py, App, add_screen()")

        MobiApp.sm.add_widget(ScreenTop(name="top"))
        MobiApp.sm.add_widget(ScreenSearch(name="search"))
        MobiApp.sm.add_widget(ScreenWait(name="wait"))
        MobiApp.sm.add_widget(ScreenOut(name="out"))


