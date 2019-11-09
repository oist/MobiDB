import json
from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
import time

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("hello")


class LimitScoreSearch:
    """閾値以上のScore"""

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
            error_id.append(i)

        logger.debug("load_scores End")

    def insert_jd(self, jd, i):
        try:
            self.fw.write('{}\n'.format(json.dumps(jd)))
        except Exception:
            print("Insert was failure for success data to Json File, number :", i)


class TopScreen(Screen):
    """Top画面"""

    def press_btn(self):
        # ボタンイベント，searchに画面遷移する

        logger.debug("press_btn_TS Begin")

        sm.add_widget(SearchScreen(name="search"))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = "search"  # Search画面に移動する

        logger.debug("press_btn_TS End")


class SearchScreen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        logger.debug("SS_init Begin")

        self.threshold_val = 0
        self.threshold_len = 0
        self.fill_gap = 0
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

        logger.debug("press_btn_SS Begin")
        self.load_parameter()
        self.lss.search_info(self.threshold_val, self.threshold_len, self.fill_gap)

        sm.add_widget(WaitScreen(name="wait"))  # wait画面を生成
        sm.current = "wait"  # wait画面に移動

        logger.debug("press_btn_SS End")

    def load_parameter(self):
        # データを探す

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
        # ボタンが押されたときSearch画面に戻る

        logger.debug("press_btn_WS Begin ")

        sm.remove_widget(self)
        sm.add_widget(OutputScreen(name="out"))
        sm.current = "out"

        logger.debug("press_btn_WS End")


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

        print("filter")

        logger.debug("filter_OS End")

    def return_window(self):
        logger.debug("return_window Begin")

        sm.add_widget(OutputScreen(name="search"))
        sm.remove_widget(self)
        sm.current = "search"

        logger.debug("return_window End")


class ScorePlot():
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
        self.key = 0
        self.threshold = 0.75
        self.text = ""

        self.load_propaty()
        self.plot_json_data()
        self.fig.canvas.draw()

        # canvasの一部を再描画するためのやつ
        self.bg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def load_propaty(self):
        logger.debug('load_propaty Begin')

        div = 0

        with open('success_data.mjson', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == self.key:
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

        self.fig.canvas.restore_region(self.bg)
        self.ax.draw_artist(self.ln_h)
        self.ax.draw_artist(self.ln_v)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def run(self):
        self.fig.show()


class Row(Screen):
    def score_plot(self, value):
        logger.debug("score_plot_R Begin")
        print(value)
        print(type(value))
        score = ScorePlot()
        score.key = value
        score.run()
        plt.show()

        logger.debug("score_plot_R End")


class MobiApp(App):
    def build(self):
        logger.debug("App Begin")

        sm.add_widget(TopScreen(name="top"))
        sm.current = "top"

        logger.debug("App End")
        return sm


if __name__ == "__main__":
    logger.debug("main Begin")

    success_id = []  # 条件に当てはまったIDを格納する
    false_id = []
    error_id = []


    with open("./theme.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (800, 600)
    sm = ScreenManager()  # スクリーンマネージャ
    MobiApp().run()

    logger.debug("main End")
