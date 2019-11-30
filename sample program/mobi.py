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
import webbrowser
import re
Show_Func = Window.show


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("hello")


def rename_protain(name):
    name = name[:name.find('(')]
    #name = name[:name.find('[')]
    #name = name[:name.find(',')]
    return name


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

    print(type(screen_name))
    sm.current = screen_name  # wait画面に移動

    logger.debug("change_screen: " + screen_name + "End")


def make_sure_text(ss_text):
    if ss_text == "":
        return 0
    else:
        return float(ss_text.replace('"', ''))


class TopScreen(Screen):
    """Top画面"""

    def press_btn(self):
        change_screen("Search")


class SearchScreen(Screen):
    """search画面"""

    def press_btn(self):
        logger.debug("press_btn_SS")
        try:
            config.threshold_val = make_sure_text(self.ids["th_val"].text)
            config.threshold_len = int(make_sure_text(self.ids["th_len"].text))
            config.fill_gap = int(make_sure_text(self.ids["fill_gap"].text))

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
                name = rename_protain(json_dict["protein names"])
                self.rv.data.append({'value': name, 'index': i})

        logger.debug("on_enter_OS End")

    def sort(self):
        logger.debug("sort Begin")
        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])

        logger.debug("sort End")

    def filter(self):
        logger.debug("filter Begin")
        config.keyword = self.ids["keyword"].text

        temp = []

        with open('success_data.mjson', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                if config.keyword in json_dict["protein names"]:
                    name = rename_protain(json_dict["protein names"])
                    temp.append({'value': name, 'index': i})

            self.rv.data = temp

        logger.debug("filter End")

    def return_window(self):
        change_screen("Search")


class LimitScoreSearch:
    """閾値以上のScoreを探索する"""
    def __init__(self):
        logger.debug('LSS_init Begin')

    def search_info(self):
        logger.debug("search_info Begin")

        # print(config.threshold_len)
        # print(config.threshold_val)

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
        """
        score[pos]              : pos番目のscore値。
        config.threshold_val    : score値用の閾値。
        config.threshold_len    : 閾値以上が何回続けばよいかを決める変数。
        succeeded_times         : scores[pos] > config.threshold_val が True であった回数を保持する変数。

        whileループは　succeeded_times > threshold_len のときに抜ける。

        config.fill_gap         : 閾値以下を何回まで許すかを決める変数　
                                  例）　score[ 1, 1, 0, 0, 1, 1 ], threshold_val = 0.5 とする。
                                     ---------------------------------------------
                                        for i in len(score):
                                            if score[i] > threshold_val:
                                                i += 1
                                            elif score[i] < threshold_val
                                                i = 0
                                     ---------------------------------------------
                                     上記のように比較した場合の出力は、
                                        fill_gap == 1 -> 2
                                        fill_gap == 2 -> 6
                                     と違いがでる。
                                     このように、閾値以下を何回許すかを決める変数をfill_gapとする。

        ignored_times           : 無視した回数の合計を保持する変数。
        """

        for (i, line) in enumerate(fr):
            json_dict = json.loads(line)

            succeeded_times = 0
            ignored_times = 0
            pos = config.threshold_len

            try:
                # keywordが含まれているか判定
                if config.keyword not in json_dict["protein names"]:
                    continue

                scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

                while pos < len(scores):

                    # scoreが閾値を超えているか判定
                    if scores[pos] > config.threshold_val:
                        succeeded_times += 1
                        pos -= 1
                        ignored_times = 0
                    else:
                        # fill_gapの処理を入れる
                        if config.fill_gap > ignored_times:
                            succeeded_times += 1
                            pos -= 1
                            ignored_times += 1
                        else:
                            succeeded_times = 0
                            pos += config.threshold_len + ignored_times
                            ignored_times = 0

                    if succeeded_times >= config.threshold_len:
                        fw.write('{}\n'.format(json.dumps(json_dict)))
                        break

            except IndexError as e:
                pass


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
        name = rename_protain(self.json_dict["protein names"])

        # 閾値以上の数の割合を計算する
        for i in range(len(self.score)):
            if self.score[i] >= config.threshold_val:
                div += 1

            self.list_id.append(i)

        # プロット時に表示するデータの構成
        # print(str(div))
        # print(str(len(self.score)))
        # print(round(div / len(self.score) * 100, 3))
        self.text = "ACC:" + self.acc + "\n" + \
                    "Protain Names : " + name + "\n" + \
                    "Percentage (x >= " + str(config.threshold_val) + "):" + str(round(div / len(self.score) * 100, 3)) + "%"

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

    def go_UniProt(self, value):
        with open('success_data.mjson', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == value:
                    json_dict = json.loads(line)
                    break

        url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
        browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
        browser.open(url)


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
