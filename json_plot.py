from logging import getLogger, StreamHandler, DEBUG
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

        self.json_dict = {}
        self.list_id = []
        self.score = []
        self.sequence = []
        self.acc = ""
        self.pName = ""
        self.div = 0
        self.threshold = 0.75
        self.ln_v = plt.axvline(0)
        self.text = ""

        logger.debug('ScorePlot_init End')

    def load_propaty(self):
        logger.debug('load_propaty Begin')

        div = 0

        with open("disorder_add_protain.mjson", 'r') as f:
            for (k, line) in enumerate(f):
                if k == 20020:
                    self.json_dict = json.loads(line)

                    break

        self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]  # scoreの値を取得する
        self.sequence = list(self.json_dict["sequence"])  # シーケンスの値を取得する
        self.acc = self.json_dict["acc"]  # Entry nameを取得する
        try:
            self.pName = self.json_dict["protein names"]
        except KeyError:
            self.pName = "No Name"
        for i in range(len(self.score)):
            if self.score[i] > self.threshold:
                div += 1

            self.list_id.append(i)

        self.text = "ACC:" + self.acc + "\n" + \
                    "Protain Names : " + self.pName + "\n" + \
                    "Percentage (High):" + str(round(div / len(self.score) * 100, 3)) + "%"

        logger.debug('load_propaty End')

    def set_plt(self):
        logger.debug('set_plot Begin')

        # plt.plots(sp.core, color='black', alpha=0.5)self.sequence
        plt.scatter(self.list_id, self.score, s=25, c=self.score, cmap='jet')
        plt.plot(self.score, color='black', linestyle='solid', alpha=0.7)

        plt.ylim(0, 1.1)
        plt.xlabel('Array', fontsize=16)
        plt.ylabel('Score', fontsize=16)
        plt.colorbar()

        plt.grid(True)

        ax = plt.gca()
        ax.spines["right"].set_color("none")  # 右枠消し
        ax.spines["top"].set_color("none")  # 上枠消し
        ax.spines["left"].set_color("m")  # 左枠をマゼンダに
        ax.spines["bottom"].set_color("c")
        ax.text(0, 1.1, self.text, fontweight="semibold", style='italic',
                bbox={'facecolor': 'blue', 'alpha': 0.3, 'pad': 10})

        for i in range(len(self.score)):
            ax.annotate(self.sequence[i], (i, 1.05), size=5, horizontalalignment='center')

        plt.hlines([self.threshold], 0, len(self.score), "r", linestyle=":", lw=1)

        plt.tight_layout()
        logger.debug('set_plot End')


def motion(event):
    x = event.xdata
    sp.ln_v.set_xdata(x)
    plt.draw()


if __name__ == '__main__':
    logger.debug('main Begin')

    sp = ScorePlot()

    sp.load_propaty()
    sp.set_plt()

    plt.connect('motion_notify_event', motion)

    plt.show()

    logger.debug('main End')
