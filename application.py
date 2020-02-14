from logging import getLogger, StreamHandler, DEBUG

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp

from screen_main_filter import ScreenMainFilter
from screen_wait_main import ScreenWait
from screen_out_main import ScreenOut
from screen_main_keyword import ScreenMainKeyword


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class MobiApp(MDApp):

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
    sm = ScreenManager(transition=NoTransition())

    def build(self):
        logger.debug("application.py, App, build()")

        # 画面をScreenManagerに追加する
        self.title = "MobiDB - Human"
        self.theme_cls.primary_palette = "Indigo"
        self.add_screen()

        return MobiApp.sm

    def add_screen(self):
        logger.debug("application.py, App, add_screen()")

        MobiApp.sm.add_widget(ScreenMainKeyword(name="search_keyword"))
        MobiApp.sm.add_widget(ScreenMainFilter(name="search_filter"))
        MobiApp.sm.add_widget(ScreenWait(name="wait"))
        MobiApp.sm.add_widget(ScreenOut(name="out"))