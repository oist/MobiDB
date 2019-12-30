from logging import getLogger, StreamHandler, DEBUG
import json
import time
import matplotlib.pyplot as plt
import numpy as np


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScorePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ln_v = self.ax.axvline(0)
        self.ln_h = self.ax.axhline(0)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.json_dict = {}
        self.list_id = []
        self.score = []
        self.sequence = []
        self.acc = ""
        self.pName = ""
        self.div = 0
        self.threshold = 0.75
        self.text = ""
        self.figure_size = self.fig.get_size_inches()

        self.load_propaty()
        self.plot_json_data()
        self.fig.canvas.draw()

        ## canvasの一部を再描画するためのやつ
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)


    def load_propaty(self):
        logger.debug('load_propaty Begin')

        div = 0

        with open("disorder_add_protain.mjson", 'r') as f:
            for (k, line) in enumerate(f):
                if k == 20020:
                    self.json_dict = json.loads(line)
                    break

        try:
            self.score = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]  # scoreの値を取得する
        except:
            pass
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
        try:
            self.text = "ACC:" + self.acc + "\n" + \
                    "Protain Names : " + self.pName + "\n" + \
                    "Percentage (High):" + str(round(div / len(self.score) * 100, 3)) + "%"
        except:
            pass

    def plot_json_data(self):
        plt.scatter(self.list_id, self.score, s=25, c=self.score, cmap='jet')
        plt.plot(self.score, color='black', linestyle='solid', alpha=0.7)

        plt.ylim(0, 1.1)
        plt.xlabel('Array', fontsize=16)
        plt.ylabel('Score', fontsize=16)
        plt.colorbar()

        plt.grid(True)

        self.ax.spines["right"].set_color("none")  # 右枠消し
        self.ax.spines["top"].set_color("none")  # 上枠消し
        self.ax.spines["left"].set_color("m")  # 左枠をマゼンダに
        self.ax.spines["bottom"].set_color("c")
        self.ax.text(0, 1.1, self.text, fontweight="semibold", style='italic',
                bbox={'facecolor': 'blue', 'alpha': 0.3, 'pad': 10})

        for i in range(len(self.score)):
            self.ax.annotate(self.sequence[i], (i, 1.05), size=5, horizontalalignment='center')

        plt.hlines([self.threshold], 0, len(self.score), "r", linestyle=":", lw=1)

        plt.tight_layout()
        self.fig.canvas.draw()

    def on_motion(self, event):
        self.ln_v.set_xdata(event.xdata)
        self.ln_h.set_ydata(event.ydata)

        #window = plt.get_current_fig_manager().window
        fig_size = self.fig.get_size_inches()
        if any(not fig_size == self.figure_size):
            print("bg update.")
            self.figure_size = fig_size
            self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        self.fig.canvas.restore_region(self.bg)
        self.ax.draw_artist(self.ln_h)
        self.ax.draw_artist(self.ln_v)
        self.fig.canvas.blit(self.ax.bbox)
        #self.fig.canvas.update()
        #self.fig.canvas.flush_events()



    def run(self):
        self.fig.show()


if __name__ == "__main__":
    score = ScorePlot()
    score.run()
    plt.show()
