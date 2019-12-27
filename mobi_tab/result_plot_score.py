from logging import getLogger, StreamHandler, DEBUG
import json
from io import StringIO
import tempfile
import webbrowser
from jinja2 import Environment, FileSystemLoader
import config


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Plot:
    """
    指定されたidのスコアをプロットする

    Parameters
    ----------
    self.key : int
        Holds the number to load.
    self.json_dict : dict
        Hold valueth data of succeed_data.mjson.
    self.score : list
        Load score value from json_dict.
    self.sequence : list
        Load sequence from json_dict.
    self.acc : str
        Load accession number from json_dict
    self.name : str
        Load protain names from json_dict
    self.succeed_score_rate
        Percentage of score value above threshold

    Methods
    ----------
    def load_propaty(self) :
        Load valueth data of succeed_data.mjson.
    def calculate_score_rate(self) :
        Calculate percentage of score value above threshold
    def run(self) :
        plot score, sequence, acc, name and succeed_score_rate


    Note
    ----------
    RecycleViewは MVCという概念からできている。

    [Model]
    RecycleViewが持つdataプロパティはModelに相当する。
    dataプロパティは辞書のリストになっており、リストの要素数だけ子widgetができる。
    辞書はキーに子widgetのプロパティ(文字列)を、値にそのプロパティの値を持つ。

    [View]
    RecycleView直下の子widgetは、各子widgetの並びを決定することができる。
    RecycleViewが持つviewclassプロパティにカスタムwidget(文字列)を渡すことで、各子widgetの個々のプロパティを決定することができる。

    [Controller]
    RecycleViewが持つviewclassプロパティに値(文字列)を渡すことで、各子widgetのwindgetの種類を決定することができる。
    RecycleView直下の子widgetは各子widgethへのメソッドを提供することができる。

    参考 : https://labor.hatenablog.jp/entry/2019/09/25/%E7%A7%81%E6%96%87_vs_kivy%285-1%29_RecycleView%E3%81%AE%E5%9F%BA%E6%9C%AC_1

    """

    def __init__(self, value):
        logger.debug("plot_score.py, Plot, __init__()")

        self.key = value

        self.json_dict = dict()
        self.score = list()
        self.sequence = list()
        self.acc = ""
        self.name = ""
        self.succeed_score_rate = 0

    def load_propaty(self):
        logger.debug("plot_score.py, Plot, load_propaty()")

        with open('success_data.json', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == self.key:
                    self.json_dict = json.loads(line)
                    break

        self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
        self.sequence = list(self.json_dict["sequence"])
        self.acc = self.json_dict["acc"]
        self.name = self.json_dict["protein_names"]

    def json_propaty(self):
        logger.debug("plot_score.py, Plot, json_propaty()")

        temp = {
            "acc" : self.acc,
            "sequence" : self.sequence,
            "protain_names" : self.name,
            "score" : self.score
        }
        with open('plot_data.json', 'w') as f:
            json.dump(temp, f, ensure_ascii=False)

    def calculate_score_rate(self):
        logger.debug("plot_score.py, Plot, calculate_score_rate()")

        score_rate = 0
        score_len = len(self.score)
        for i in range(score_len):
            if self.score[i] >= config.threshold_val:
                score_rate += 1

        self.succeed_score_rate = "{0:.3f}".format(score_rate / score_len * 100)

    def run(self):
        logger.debug("plot_score.py, Plot, run()")

        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        tpl = env.get_template('index.html')
        data = {
            "protain_names": self.name,
            "acc": self.acc,
            "score": self.score,
            "seq": self.sequence,
            "threshold": config.threshold_val,
            "percentage": self.succeed_score_rate,
        }
        html = tpl.render(data)
        with tempfile.NamedTemporaryFile("w+") as f:
            print(StringIO(html), file=f)
            webbrowser.open_new_tab(f.name)

        print("score : " + str(self.score))
        print("sequence : " + str(self.sequence))
        print("acc : " + str(self.acc))
        print("name : " + str(self.name))
        print("succeed_score_rate : " + str(self.succeed_score_rate))