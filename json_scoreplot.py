from logging import getLogger, StreamHandler, DEBUG
import time
import json
import matplotlib.pyplot as plt
import pandas as pd


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
        with open("disorder_add_protain.mjson", 'r') as f:
            for (k, line) in enumerate(f):
                if k == 25:
                    self.json_dict = json.loads(line)

                    break

        self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]  # scoreの値を取得する
        self.sequence = list(self.json_dict["sequence"])  # シーケンスの値を取得する
        self.acc = self.json_dict["acc"]  # Entry nameを取得する
        self.pName = self.json_dict["protein names"]
        self.div = 0

        logger.debug('ScorePlot_init End')

    def plot_score(self):
        # thread の名前を取得
        logger.debug('get_json Begin')
        count = 0

        for i in range(len(self.score)):
            if self.score[i] > 0.5:
                plt.scatter(i, self.score[i], marker='.', c="red")
                count += 1
            else:
                plt.scatter(i, self.score[i], marker='.', c="blue")

            # シーケンスをグラフ直下にプロット
            plt.text(i, -0.1, self.sequence[i], size=10, horizontalalignment='center')

        self.div = count/len(self.score)*100

        logger.debug('get_json End')

def store_graph():
    logger.debug('set_graph Begin')

    plt.ylim(-0.2, 1.2)
    plt.title('Score-Plot Test', fontsize=20)
    plt.xlabel('score', fontsize=16)
    plt.ylabel('array number', fontsize=16)

    plt.grid(True)

    logger.debug('set_graph End')


def motion(event):
    x = event.xdata
    # y = event.ydata
    ln_v.set_xdata(x)
    # ln_h.set_ydata(y)
    plt.draw()


if __name__ == '__main__':
    logger.debug('main Begin')

    t1 = time.time()

    sp = ScorePlot()
    sp.plot_score()   # jsonからデータを取得
    store_graph()  # グラフの初期設定

    ln_v = plt.axvline(0)   # 十字線の生成
    # ln_h = plt.axhline(0)

    plt.connect('motion_notify_event', motion)

    try:
        plt.plot(sp.score, color='black', linestyle='solid', alpha=0.5, label="protain names : " + sp.pName)
    except:
        plt.plot(sp.score, color='black', linestyle='solid', alpha=0.5, label="acc: " + sp.acc)

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    plt.show()

    logger.debug('main End')
