from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.uix.screenmanager import Screen
from screen_out_result_button import ResultButton
import json

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenOut(Screen):
    """
    app.sm.current == "out" 時の処理

    Methods
    ----------
    on_enter(self)
        success_data.mjsonからプロテイン名のみを抽出し、self.rv.dataに追加することで、
        ボタンの名前表示を追加していく。

    btn_event(self, int)
        iの値に応じて処理を行う。
        1.キーワード検索メソッドの実行
        2.abc順でソートする
        3.ScreennSearchに移動する。

    filter_keyword(self)
        success_data.mjsonからプロテイン名のみを抽出し、キーワードが含まれているかを判定し
        Trueならself.rvにappendする。

    sort_abc(self)
        ラムダ関数を使ったsortを行う

    """
    def on_enter(self):
        logger.debug("screen_out_main.py, ScreenOut, on_enter()")

        with open('success_data.json', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                self.rv.data.append({'value': json_dict["protein_names"], 'index': i})

        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])

    def btn_event(self):
        logger.debug("screen_out_main.py, ScreenOut, btn_event()")

        self.change_screen("search_filter")

    def change_screen(self, name):
        logger.debug("screen_top_main.py, ScreenOut, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
