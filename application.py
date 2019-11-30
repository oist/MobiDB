from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen_top_main import ScreenTop
from screen_search_main import ScreenSearch
from screen_wait_main import ScreenWait
from screen_out_main import ScreenOut
from kivy.properties import StringProperty, ObjectProperty

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("application Begin")


class MobiApp(App):
    sm = ScreenManager()  # スクリーンマネージャ

    def build(self):
        logger.debug("App, build Begin")

        self.add_screen()
        app = App.get_running_app()
        app.sm.current = "top"

        logger.debug("App, build End")
        return MobiApp.sm

    def add_screen(self):
        logger.debug("App, add_screen() Begin")

        MobiApp.sm.add_widget(ScreenTop(name="top"))
        MobiApp.sm.add_widget(ScreenSearch(name="search"))
        MobiApp.sm.add_widget(ScreenWait(name="wait"))
        MobiApp.sm.add_widget(ScreenOut(name="out"))

        logger.debug("App, add_screen() End")

