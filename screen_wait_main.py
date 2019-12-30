from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen
from kivy.app import App
from screen_wait_search import SearchScore
import config


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenWait(Screen):
    """
        app.sm.current == "wait" 時の処理

        Parameters
        ----------
        ss : class screen_wait_search.SearchScore
            SearchScoreクラスのインスタンスを作成。検索メソッドをもつ。

        Methods
        ----------
        on_enter(self)
            wait画面に入ったときに、検索を開始する。

        btn_event(self)
            "cancel"が押されたとき処理を中断し search画面に戻る。
            on_enterの処理はスレッドで行っているため、実行可。
        ss.start()
            runメソッドを実行する。
            Thredingで行われる。


        Notes
        ----------
        Button イベントは theme.ScreenWaitに記載。

        """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.ss = SearchScore()

    def on_enter(self):
        logger.debug("screen_wait_main.py, ScreenWait, on_enter()")

        # 閾値とscoreを比較し、条件に当てはまるものを検索する
        if config.isFilter:
            self.ss = SearchScore()
            self.ss.start()

        else:
            print("Keyword Search")

    def btn_event(self):
        logger.debug("screen_wait_main.py, ScreenWait, btn_event()")

        # cancelボタンが押されたらsearch画面の値を初期化して戻る
        self.ss.kill()
        self.change_screen("search_filter")

    def change_screen(self, name):
        logger.debug("screen_wait_main.py, ScreenWait, change_screen()")

        app = App.get_running_app()
        app.sm.current = name

