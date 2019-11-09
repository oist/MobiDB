import json
from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import multiprocessing
import time
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
    logger.debug("change_screen: " + screen_name + " Begin")

    if screen_name == "Top":
        sm.add_widget(TopScreen(name=screen_name))  # wait画面を生成
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
        # ボタンイベント，searchに画面遷移する
        change_screen("Search")


class SearchScreen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        logger.debug("SS_init Begin")

        self.threshold_val = 0      # score valueの閾値
        self.threshold_len = 0      # score lengsの閾値
        self.fill_gap = 0           # score gapの閾値
        self.lss = LimitScoreSearch()

        logger.debug("SS_init End")

    def Score_b(self):
        if self.ids["Score"].state != "down":
            self.ids["Score"].state = "normal"
            self.ids["Score"].background_color = 1, 1, 1, 0.9
            self.ids["sp_s"].text = " "

        elif self.ids["Score"].state != "normal":
            self.ids["Score"].state = "down"
            self.ids["Score"].background_color = 6, 2, 0.5, 1
            self.ids["sp_s"].is_open = True

    def Lengs_b(self):
        if self.ids["Lengs"].state != "down":
            self.ids["Lengs"].state = "normal"
            self.ids["Lengs"].background_color = 1, 1, 1, 0.9
            self.ids["sp_l"].text = " "

        elif self.ids["Lengs"].state != "normal":
            self.ids["Lengs"].state = "down"
            self.ids["Lengs"].background_color = 6, 2, 0.5, 1
            self.ids["sp_l"].is_open = True

    def Gap_b(self):

        if self.ids["Gap"].state != "down":
            self.ids["Gap"].state = "normal"
            self.ids["Gap"].background_color = 1, 1, 1, 0.9
            self.ids["sp_g"].text = " "

        elif self.ids["Gap"].state != "normal":
            self.ids["Gap"].state = "down"
            self.ids["Gap"].background_color = 6, 2, 0.5, 1
            self.ids["sp_g"].is_open = True

    def press_btn(self):
        # ボタンイベント，waitに画面遷移し、threadを開始する
        logger.debug("press_btn_SS")

        self.load_parameter()
        change_screen("Wait")

    def load_parameter(self):
        # search画面からデータを受け取る　

        logger.debug("load_parameter Begin")

        if self.ids["Score"].state == "down":
            self.threshold_val = int(float(self.ids["sp_s"].text))
        else:
            pass

        if self.ids["Lengs"].state == "down":
            self.threshold_len = int(self.ids["sp_l"].text)
        else:
            pass

        if self.ids["Gap"].state == "down":
            self.fill_gap = int(self.ids["sp_g"].text)
        else:
            pass

        logger.debug("load_parameter End")


class WaitScreen(Screen):
    """データ抽出中のwait画面"""

    def press_btn(self):
        change_screen("Search")

    def on_enter(self):
        logger.debug("on_enter_WS")
        lss = LimitScoreSearch()
        ss = SearchScreen()

        #p = multiprocessing.Process(target=lss.search_info, args=(ss.threshold_val, ss.threshold_len, ss.fill_gap))
        #p.start()  # プロセスの開始
        #p.join()

        #change_screen("Output")


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

    def search_info(self, val, lengs, gap):
        logger.debug("search_info Begin")
        # jsonファイル読み込み，条件比較を行う
        self.fw = open('success_data.mjson', 'w')
        with open("disorder_add_protain.mjson", "r") as f:
            for (i, line) in enumerate(f):
                json_dict = json.loads(line)
                count = 0
                pos = lengs

                scores = self.load_scores(json_dict, i)
                # print(scores)
                if scores is None:
                    pass
                else:
                    while count < lengs and pos < len(scores):
                        if scores[pos] < val:
                            count = 0
                            pos += lengs
                        else:
                            count += 1
                            pos -= 1

                    if count >= lengs:
                        self.insert_jd(json_dict, i)

                    #else:
                        #false_id.append(i)

        logger.debug("search_info End")

    def load_scores(self, json_dict, i):
        logger.debug("load_scores Begin")

        try:
            return json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

        except IndexError as e:
            print("load_scores IndexError: {}".format(e))
            # error_id.append(i)

        logger.debug("load_scores End")

    def insert_jd(self, jd, i):
        try:
            self.fw.write('{}\n'.format(json.dumps(jd)))
        except Exception:
            print("Insert was failure for success data to Json File, number :", i)


class ScorePlot():
    """scoreのプロット処理"""

    def __init__(self):
        self.ss = SearchScreen()  # threshold_value用のインスタンス

        self.fig, self.ax = plt.subplots()
        self.ln_v = self.ax.axvline(0)
        self.ln_h = self.ax.axhline(0)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

        self.json_dict = {}  # jsonから取り出したデータを保持
        self.list_id = []  # 閾値の条件をクリアしたidを保持
        self.score = []  # plot用にjson_dictからscoreをload
        self.sequence = []  # plot用にjson_dictからsequenceをload
        self.acc = ""  # plot用にjson_dictからaccをload
        self.pName = ""  # plot用にjson_dictからプロテイン名をload
        self.div = 0  # 閾値を超えているスコア数と全体の割合を保持
        self.key = 0  # 出力するデータを決めるkey
        self.text = ""  # plot画面に表示するtext

        # initでプロパティを読み込みplotする
        self.load_propaty()
        self.plot_json_data()
        self.fig.canvas.draw()

        # canvasの一部を再描画するためのやつ
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def load_propaty(self):
        #
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
        try:
            self.pName = self.json_dict["protein names"]
        except KeyError:
            self.pName = "No Name"
        for i in range(len(self.score)):
            if self.score[i] > self.ss.threshold_value:
                div += 1

            self.list_id.append(i)

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
        self.ax.spines["top"].set_color("none")  # 上枠消し
        self.ax.spines["left"].set_color("m")  # 左枠をマゼンダに
        self.ax.spines["bottom"].set_color("c")
        self.ax.text(0, 1.1, self.text, fontweight="semibold", style='italic',
                     bbox={'facecolor': 'blue', 'alpha': 0.3, 'pad': 10})

        for i in range(len(self.score)):
            self.ax.annotate(self.sequence[i], (i, 1.05), size=5, horizontalalignment='center')

        plt.hlines([self.ss.threshold_value], 0, len(self.score), "r", linestyle=":", lw=1)

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
        score = ScorePlot()
        score.key = value       # keyを上書きする
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
