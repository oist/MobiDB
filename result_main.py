from logging import getLogger, StreamHandler, DEBUG
import json


from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Row:
    pass

class Result(BoxLayout, MDTabsBase):
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

    def __init__(self, **kwargs):
        logger.debug("result_main.py, Result, __init__()")
        super().__init__(**kwargs)
        self.success_list = list()

    def store(self):
        logger.debug("screen_out_main.py, ScreenOut, store()")

        with open('success_data.json', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                self.rv.data.append({'value': json_dict["protein_names"], 'index': i})
        print(self.rv.data)

    def btn_event(self, i):
        logger.debug("screen_out_main.py, ScreenOut, btn_event()")

        if i == 0:
            self.filter_keyword()
        elif i == 1:
            self.sort_abc()
        elif i == 2:
            self.change_screen("search")

    def filter_keyword(self):
        logger.debug("screen_out_main.py, ScreenOut, filter_keyword()")
        temp = []


        with open('success_data.json', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                if self.ids["keyword"].text in json_dict["protein_names"]:
                    temp.append({'value': json_dict["protein_names"], 'index': i})

        self.rv.data = temp

    def sort_abc(self):
        logger.debug("screen_out_main.py, ScreenOut, sort_abc()")
        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])