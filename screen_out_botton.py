from logging import getLogger, StreamHandler, DEBUG

from kivy.properties import ListProperty
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


class ResultBotton(Screen):
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
    menu_items = ListProperty()

    def __init__(self, **kw):
        logger.debug("screen_out_botton.py, ResultBotton, __init__()")
        super().__init__(**kw)

        self.protein_id = 0

        self.menu_items = [
            {
                "viewclass": "MDMenuItem",
                "text": "Plot Score",
                "callback": self.callback_for_btn_plot,
            },
            {
                "viewclass": "MDMenuItem",
                "text": "Search in Uniplot",
                "callback": self.callback_for_btn_uniplot,
            }
        ]

    def store_protain_propaty(self, value):
        logger.debug("screen_out_botton.py, ResultBotton, store_protain_propaty()")
        self.protein_id = value
        print(self.protein_id)

    def callback_for_btn_plot(self, text):
        logger.debug("screen_out_botton.py, ResultBotton, callback_for_btn_plot()")

        score = ScorePlot(self.protein_id)

        # value番目のプロパティを取得
        score.load_propaty()
        score.json_propaty()
        score.calculate_score_rate()

        # JSまたはC#によるplotを実行する
        score.run()

    def callback_for_btn_uniplot(self, text):
        logger.debug("screen_out_botton.py, ResultBotton, callback_for_btn_uniplot()")
        print(self.protein_id)

        with open('success_data.json', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == self.protein_id:
                    json_dict = json.loads(line)
                    break

        url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
        browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
        browser.open(url)
