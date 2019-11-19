import json
from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import time
import config
Show_Func = Window.show

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("hello")


def change_screen(screen_name):
    """画面遷移する"""
    logger.debug("change_screen: " + screen_name + " Begin")

    if screen_name == "Top":
        sm.add_widget(TopScreen(name=screen_name))  # Top画面を生成
    elif screen_name == "Search":
        sm.add_widget(SearchScreen(name=screen_name))
    elif screen_name == "Wait":
        sm.add_widget(WaitScreen(name=screen_name))
    elif screen_name == "Output":
        sm.add_widget(OutputScreen(name=screen_name))

    sm.current = screen_name  # wait画面に移動

    logger.debug("change_screen: " + screen_name + "End")


class TopScreen(Screen):
    """Top画面"""

    def press_btn(self):
        change_screen("Search")


class SearchScreen(Screen):
    """search画面"""

    def press_btn(self):
        logger.debug("press_btn_SS")
        try:
            config.keyword = self.ids["keyword"].text

            val = self.ids["th_val"].text
            config.threshold_val = float(val.replace('"', ''))
            config.threshold_len = int(self.ids["th_len"].text)
            config.fill_gap = self.ids["fill_gap"].text

            change_screen("Wait")
        except ValueError as e:
            print(e)


class WaitScreen(Screen):
    """データ抽出中のwait画面"""

    def press_btn(self):
        change_screen("Search")

    def on_enter(self):
        logger.debug("on_enter_WS")
        lss = LimitScoreSearch()

        t = threading.Thread(target=lss.search_info)
        t.start()  # プロセスの開始


class OutputScreen(Screen):
    """output画面"""
    def __init__(self, **kwargs):
        super(OutputScreen, self).__init__(**kwargs)

    def on_enter(self):
        logger.debug("on_enter_OS Begin")

        with open('success_data.mjson', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                try:
                    name = json_dict["protein names"]
                except KeyError:
                    name = "No Name"
                self.rv.data.append({'value': name, 'index': i})

        logger.debug("on_enter_OS End")

    def sort(self, value):
        logger.debug("sort_OS Begin")
        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])
        logger.debug("sort_OS End")

    def filter(self, value):
        logger.debug("filter_OS Begin")

        # write code of filter method

        logger.debug("filter_OS End")

    def return_window(self):
        change_screen("Search")


class LimitScoreSearch:
    """閾値以上のScoreを探索する"""
    def __init__(self):
        logger.debug('LSS_init Begin')

        # 2019/11/19
        # search画面でデータが取得できないため、一時的に固定で扱う

    def search_info(self):
        logger.debug("search_info Begin")

        print(config.threshold_len)
        print(config.threshold_val)

        # jsonファイル読み込み，条件比較を行う
        with open('success_data.mjson', 'w') as fw:
            with open("disorder_add_protain.mjson", "r") as fr:
                t1 = time.time()

                t = threading.Thread(target=self.worker, args=(fr, fw))
                t.start()
                t.join()

                t2 = time.time()
                elapsed_time = t2 - t1  # 処理にかかった時間を計算する
                print("経過時間：", elapsed_time)

        change_screen("Output")
        logger.debug("search_info End")

    def worker(self, fr, fw):
        scores = []

        for (i, line) in enumerate(fr):
            json_dict = json.loads(line)
            count = 0
            pos = config.threshold_len
            try:
                # logger.debug("success")
                scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
            except IndexError as e:
                print(e)

            if scores is None:
                pass
            else:
                while count < config.threshold_len and pos < len(scores):
                    if scores[pos] < config.threshold_val:
                        count = 0
                        pos += config.threshold_len
                    else:
                        count += 1
                        pos -= 1

                if count >= config.threshold_len:
                    fw.write('{}\n'.format(json.dumps(json_dict)))


class ScorePlot:
    """scoreのプロット処理"""

    def __init__(self, value):
        self.fig, self.ax = plt.subplots()
        self.ln_v = self.ax.axvline(0)
        self.ln_h = self.ax.axhline(0)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.json_dict = {}         # jsonから取り出したデータを保持
        self.list_id = []           # scatter用のx軸を表す配列
        self.score = []             # json_dictからscoreをload
        self.sequence = []          # json_dictからsequenceをload
        self.acc = ""               # json_dictからaccをload
        self.pName = ""             # json_dictからプロテイン名をload
        self.div = 0                # 閾値を超えているスコア数と全体の割合を保持
        self.key = value                # 出力するデータを決めるkey
        self.text = ""              # plot画面に表示するtext
        # print("ScorePlot value:" + str(self.key))

        # initでプロパティを読み込む
        self.load_propaty()
        self.plot_json_data()
        self.fig.canvas.draw()

        # canvasの一部を再描画するためのやつ
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def load_propaty(self):

        logger.debug('load_propaty Begin')

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
        self.pName = self.json_dict["protein names"]

        # 閾値以上の数の割合を計算する
        for i in range(len(self.score)):
            if self.score[i] > config.threshold_val:
                div += 1

            self.list_id.append(i)

        # プロット時に表示するデータの構成
        # print(str(div))
        # print(str(len(self.score)))
        # print(round(div / len(self.score) * 100, 3))
        self.text = "ACC:" + self.acc + "\n" + \
                    "Protain Names : " + self.pName + "\n" + \
                    "Percentage (High):" + str(round(div / len(self.score) * 100, 3)) + "%"

    def plot_json_data(self):
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
        self.ln_v.set_xdata(event.xdata)
        self.ln_h.set_ydata(event.ydata)

        self.fig.canvas.restore_region(self.bg)
        self.ax.draw_artist(self.ln_h)
        self.ax.draw_artist(self.ln_v)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def run(self):
        self.fig.show()


class Row(Screen):
    """OutputScreenのRecycleViewで使用するボタンの設定"""

    def score_plot(self, value):
        # ボタンイベント処理
        logger.debug("score_plot_R Begin")
        print("Row value:" + str(value))
        score = ScorePlot(value)
        score.run()
        plt.show()

        logger.debug("score_plot_R End")


class MobiApp(App):
    def build(self):
        logger.debug("App Begin")

        change_screen("Top")

        logger.debug("App End")
        return sm


if __name__ == "__main__":
    logger.debug("main Begin")

    # デバッグ用の配列
    error_id = []

    # kvファイルをstring型としてload
    with open("./theme.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (800, 600)
    sm = ScreenManager()  # スクリーンマネージャ
    MobiApp().run()

    logger.debug("main End")
