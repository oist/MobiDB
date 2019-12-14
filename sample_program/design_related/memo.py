import json
from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.resources import resource_add_path
resource_add_path('./image')


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
        with open("C:/Users/Akihiro Kusumi/Documents/MobiDB/disorder_add_protain.mjson", "r") as f:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.ten_seconds_later, 1.0)

    def ten_seconds_later(self, dt):
        # ボタンイベント，searchに画面遷移する

        logger.debug('Start ten_seconds_later')

        sm.add_widget(SearchScreen(name='search'))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = 'search'  # Search画面に移動する

        logger.debug('End ten_seconds_later')


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

        self.threshold_val = int(float(self.ids["text_box_score"].text))
        self.threshold_len = int(float(self.ids["text_box_lengs"].text))
        self.fill_gap = int(float(self.ids["text_box_gap"].text))

        logger.debug("load_parameter End")


class WaitScreen(Screen):
    """データ抽出中のwait画面"""
    source = StringProperty('loading5.gif')  # アニメーションgifを表示

    def press_btn(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug("press_btn_WS Begin ")

        sm.remove_widget(self)
        Window.size = (800, 600)
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
                self.rv.data.append({'value': name})

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

        Window.size = (400, 220)

        sm.add_widget(OutputScreen(name="search"))
        sm.remove_widget(self)
        sm.current = "search"

        logger.debug("return_window End")


class Row(Screen):
    def print(self):
        logger.debug("print")


class memoApp(App):
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


    with open("./memo.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (400, 220)
    sm = ScreenManager()  # スクリーンマネージャ
    memoApp().run()

    logger.debug("main End")
