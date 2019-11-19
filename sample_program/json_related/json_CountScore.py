from logging import getLogger, StreamHandler, DEBUG
import threading
import time
import json
import matplotlib.pyplot as plt

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from logging import getLogger, StreamHandler, DEBUG
import time
import json

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScorePlot:
    def __init__(self, **kwargs):
        logger.debug('ScorePlot_ini Begin')

        super(ScorePlot, self).__init__(**kwargs)

        self.score = []
        self.json_dict = []
        self.count_result = []
        self.count = 0

        logger.debug('ScorePlot_init End')

    def plot_score(self):
        # thread の名前を取得
        logger.debug('plot_score Begin')

        with open("disorder.mjson", 'r') as f:
            for (k, line) in enumerate(f):
                if k == 3:      # jsonを１つずつ読み込む。
                    self.json_dict = json.loads(line)
                    self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]  # scoreの値を取得する

                    for i in range(len(self.score)):
                        if self.score[i] > 0.5:
                            self.count += 1

                div = len(self.score)/self.count    # 割合を計算する

        print(div)

        logger.debug('plot_score End')


if __name__ == '__main__':
    logger.debug('main Begin')
    t1 = time.time()

    sp = ScorePlot()   # ScorePlotをインスタンス化
    sp.plot_score()   # jsonからデータを取得

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)
    logger.debug('main End')
