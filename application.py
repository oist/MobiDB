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
    sm = ScreenManager()

    # Appの初期化
    def build(self):
        logger.debug("application.py, App, build()")

        # 画面をScreenManagerに追加する
        self.add_screen()

        # 画面遷移する
        app = App.get_running_app()
        app.sm.current = "top"

        return MobiApp.sm

    def add_screen(self):
        logger.debug("application.py, App, add_screen()")

        MobiApp.sm.add_widget(ScreenTop(name="top"))
        MobiApp.sm.add_widget(ScreenSearch(name="search"))
        MobiApp.sm.add_widget(ScreenWait(name="wait"))
        MobiApp.sm.add_widget(ScreenOut(name="out"))


