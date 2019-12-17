from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.uix.screenmanager import Screen
from screen_out_plot import ScorePlot
import json
import webbrowser


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Row(Screen):
    """
    app.sm.current == "out" 時の処理

    Methods
    ----------
    btn_event(self, id, boolean)
        true  : value=idを受け取り、プロットメソッドを呼び出す。マルチプロセスで処理する。
        false : value=idを受け取り、Uniprot(Webサイト)にアクセスする。

    Notes
    ----------
    Rowクラスの親クラスがScreenOutクラス

    """

    def btn_event(self, value, i):

        if i:
            logger.debug("screen_out_row.py, Row, btn_event, plot_score()")

            score = ScorePlot(value)

            # value番目のプロパティを取得
            score.load_propaty()
            score.json_propaty()
            score.calculate_score_rate()

            # JSまたはC#によるplotを実行する
            score.run()

        else:
            logger.debug("screen_out_row.py, Row, btn_event, go_to_uniplot()")
            with open('success_data.json', 'r') as fr:
                for (k, line) in enumerate(fr):
                    if k == value:
                        json_dict = json.loads(line)
                        break

            url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
            browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
            browser.open(url)


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

    def change_screen(self, name):
        logger.debug("screen_top_main.py, ScreenOut, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
