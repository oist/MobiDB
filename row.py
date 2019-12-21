from logging import getLogger, StreamHandler, DEBUG
from plot_score import Plot
import webbrowser
import json


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Row:
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
            logger.debug("row.py, btn_event, plot_score()")

            score = Plot(value)

            # value番目のプロパティを取得
            score.load_propaty()
            score.json_propaty()
            score.calculate_score_rate()

            # JSまたはC#によるplotを実行する
            score.run()

        else:
            logger.debug("row.py, btn_event, go_to_uniplot()")

            with open('success_data.json', 'r') as fr:
                for (k, line) in enumerate(fr):
                    if k == value:
                        json_dict = json.loads(line)
                        break

            url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
            browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
            browser.open(url)
