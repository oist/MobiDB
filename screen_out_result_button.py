from logging import getLogger, StreamHandler, DEBUG

from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from screen_out_score_plot import ScorePlot
from screen_out_show_uniplot import ShowUniplot


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ResultButton(Screen):
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
        logger.debug("screen_out_result_button.py, ResultButton, __init__()")
        super().__init__(**kw)

        self.protein_id = 0

        self.menu_items = [
            {
                "viewclass": "MDMenuItem",
                "text": "Plot Score",
                "callback": self.callback_for_score_plot,
            },
            {
                "viewclass": "MDMenuItem",
                "text": "Search in Uniplot",
                "callback": self.callback_for_show_uniplot,
            }
        ]

    def store_protain_propaty(self, value):
        logger.debug("screen_out_result_button.py, ResultButton, store_protain_propaty()")
        self.protein_id = value

    def callback_for_score_plot(self, text):
        logger.debug("screen_out_result_button.py, ResultButton, callback_for_score_plot()")

        sp = ScorePlot(self.protein_id)

        # value番目のプロパティを取得
        sp.load_propaty()
        sp.json_propaty()
        sp.calculate_score_rate()

        # JSまたはC#によるplotを実行する
        sp.run()

    def callback_for_show_uniplot(self, text):
        logger.debug("screen_out_result_button.py, ResultButton, callback_for_show_uniplot()")

        scu = ShowUniplot(self.protein_id)
        scu.run()