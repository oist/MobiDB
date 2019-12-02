
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import threading
import json
from logging import getLogger, StreamHandler, DEBUG
import time

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

kv = """
<VariousButtons>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Button:
        text: root.value
        background_normal: ''
        background_color: 0.5, 0.5, 0.75, 1
        color: 1, 1 ,1 ,1
        on_press: root.on_select_button(self)
<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: sp(60) #スクロール速度
        bar_width: sp(20)
        viewclass: 'VariousButtons'
        RecycleBoxLayout:
            default_size: None, sp(160)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(8)
"""

Builder.load_string(kv)

class LimitScoreSearch:
    def __init__(self):
        logger.debug('LSS_init Begin')

        self.th_val = 0.7  # 閾値
        self.th_len = 40  # どれだけ連続で続くかを決める
        self.success_id = []  # 条件に当てはまったIDを格納する
        self.false_id = []
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。

        logger.debug('LSS_init End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う

        with open("disorder.mjson", 'r') as f:
            for (i, line) in enumerate(f):
                json_dict = json.loads(line)
                count = 0
                pos = self.th_len

                scores = self.load_scores(json_dict, i)
                # print(scores)
                if scores is None:
                    pass
                else:
                    while count < self.th_len and pos < len(scores):
                        if scores[pos] < self.th_val:
                            count = 0
                            pos += self.th_len
                        else:
                            count += 1
                            pos -= 1

                    if count >= self.th_len:
                        self.success_id.append(json_dict["acc"])
                    else:
                        self.false_id.append(i)
        logger.debug('search_info End')
        return self.success_id


        # print("success :", self.success_id)
        # ("false :", self.false_id)
        # print("error", self.error_id)



    def load_scores(self, json_dict, i):
        logger.debug('load_scores Begin')

        try:
            return json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

        except IndexError as e:
            print("load_scores IndexError: {}".format(e))
            self.error_id.append(i)

        logger.debug('load_scores End')


class Test(BoxLayout):

    def __init__(self, **kwargs):
        logger.debug('Test Begin')

        super(Test, self).__init__(**kwargs)

        self.rv.data = []
        self.btn_list = lss.search_info()
        for btn_list_any in self.btn_list:
            self.rv.data.append({'value': btn_list_any})

        logger.debug('Test End')

    def make(self):
        print(type(self.btn_list))
        print(self.btn_list)


        print(self.rv.data)


class VariousButtons(BoxLayout):
    def on_select_button(self, button):
        logger.debug('on_VB_button Begin')

        print('press:'+button.text)

        logger.debug('on_VB_button End')


class TestApp(App):
    def build(self):
        return Test()




if __name__ == '__main__':
    logger.debug('main Begin')
    t1 = time.time()

    lss = LimitScoreSearch()  # インスタンスを作成する

    TestApp().run()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logger.debug('main End')
