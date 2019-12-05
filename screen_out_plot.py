from logging import getLogger, StreamHandler, DEBUG
import matplotlib.pyplot as plt
import config
import json


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScorePlot:
    """
    指定されたidのスコアをプロットする

    """

    def __init__(self, value):
        logger.debug("screen_out_plot.py, ScorePlot, __init__()")

        self.fig, self.ax = plt.subplots()
        self.ln_v = self.ax.axvline(0)
        self.ln_h = self.ax.axhline(0)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.json_dict = dict()     # jsonデータを保持する変数

        self.list_id = list()           # scatter用のx軸を表す配列
        self.score = list()             # json_dictからscoreをload
        self.sequence = list()          # json_dictからsequenceをload

        self.acc = ""               # json_dictからaccをload
        self.name = ""             # json_dictからプロテイン名をload
        self.div = 0                # 閾値を超えているスコア数と全体の割合を保持
        self.key = value                # 出力するデータを決めるkey
        self.text = ""              # plot画面に表示するtext

        # initでプロパティを読み込む
        self.load_propaty()
        self.plot_json_data()
        self.fig.canvas.draw()

        # canvasの一部を再描画するためのやつ
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def load_propaty(self):
        logger.debug("screen_out_plot.py, ScorePlot, load_propaty()")

        div = 0

        # key番目のデータのみを取り出す
        with open('success_data.mjson', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == self.key:
                    self.json_dict = json.loads(line)
                    break

        # 値を取得する
        self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
        self.sequence = list(self.json_dict["sequence"])
        self.acc = self.json_dict["acc"]
        self.name = self.json_dict["protein names"]

        # 閾値以上の数の割合を計算する
        for i in range(len(self.score)):
            if self.score[i] >= config.threshold_val:
                div += 1

            self.list_id.append(i)

        # プロット時に表示するデータの構成
        self.text = "ACC:" + self.acc + "\n" + \
                    "Protain Names : " + self.name + "\n" + \
                    "Percentage (x >= " + str(config.threshold_val) + "):" + str(round(div / len(self.score) * 100, 3)) + "%"

    def plot_json_data(self):
        logger.debug("screen_out_plot.py, ScorePlot, plot_json_data()")

        plt.scatter(self.list_id, self.score, s=25, c=self.score, cmap='jet')
        plt.plot(self.score, color='black', linestyle='solid', alpha=0.7)

        plt.ylim(0, 1.1)
        plt.xlabel('Array', fontsize=16)
        plt.ylabel('Score', fontsize=16)
        plt.colorbar()

        plt.grid(True)

        self.ax.spines["right"].set_color("none")  # 右枠消し
        self.ax.spines["top"].set_color("none")    # 上枠消し
        self.ax.spines["left"].set_color("m")      # 左枠をマゼンダに
        self.ax.spines["bottom"].set_color("c")
        self.ax.text(0, 1.1, self.text, fontweight="semibold", style='italic',
                     bbox={'facecolor': 'blue', 'alpha': 0.3, 'pad': 10})

        for i in range(len(self.score)):
            self.ax.annotate(self.sequence[i], (i, 1.05), size=5, horizontalalignment='center')

        plt.hlines([config.threshold_val], 0, len(self.score), "r", linestyle=":", lw=1)

        plt.tight_layout()
        self.fig.canvas.draw()

    def on_motion(self, event):
        logger.debug("screen_out_plot.py, ScorePlot, on_motion()")

        self.ln_v.set_xdata(event.xdata)
        self.ln_h.set_ydata(event.ydata)

        self.fig.canvas.restore_region(self.bg)
        self.ax.draw_artist(self.ln_h)
        self.ax.draw_artist(self.ln_v)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def run(self):
        logger.debug("screen_out_plot.py, ScorePlot, run()")

        self.fig.show()