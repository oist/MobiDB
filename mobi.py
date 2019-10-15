
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import threading
from kivy.core.window import Window
import json
from logging import getLogger, StreamHandler, DEBUG
import time
from kivy.uix.image import Image

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug('hello')


class LimitScoreSearch:
    def __init__(self):
        logger.debug('LSS_init Begin')

        self.success_id = []  # 条件に当てはまったIDを格納する
        self.false_id = []
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。

        logger.debug('LSS_init End')

    def search_info(self, val, lengs, gap):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う

        with open("disorder_add_protain.mjson", 'r') as f:
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
                        self.success_id.append(i)
                    else:
                        self.false_id.append(i)

        logger.debug('search_info End')

        return self.success_id

    def load_scores(self, json_dict, i):
        logger.debug('load_scores Begin')

        try:
            return json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

        except IndexError as e:
            print("load_scores IndexError: {}".format(e))
            self.error_id.append(i)

        logger.debug('load_scores End')


class TopScreen(Screen):
    """Top画面"""

    def press_btn(self):
        # ボタンイベント，searchに画面遷移する

        logger.debug('press_btn_TS Begin')

        sm.add_widget(SearchScreen(name='search'))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = 'search'  # Search画面に移動する

        logger.debug('press_btn_TS End')


class SearchScreen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        logger.debug('SS_init Begin')

        self.threshold_val = 0
        self.threshold_len = 0
        self.fill_gap = 0
        self.lss = LimitScoreSearch()

        logger.debug('SS_init End')

    def Score_b(self):
        if self.ids['Score'].state != 'down':
            self.ids['Score'].state = 'normal'
            self.ids['Score'].background_color = 1, 1, 1, 0.9
            self.ids['sp_s'].text = ' '

        elif self.ids['Score'].state != 'normal':
            self.ids['Score'].state = 'down'
            self.ids['Score'].background_color = 6, 2, 0.5, 1
            self.ids['sp_s'].is_open = True

    def Lengs_b(self):
        if self.ids['Lengs'].state != 'down':
            self.ids['Lengs'].state = 'normal'
            self.ids['Lengs'].background_color = 1, 1, 1, 0.9
            self.ids['sp_l'].text = ' '

        elif self.ids['Lengs'].state != 'normal':
            self.ids['Lengs'].state = 'down'
            self.ids['Lengs'].background_color = 6, 2, 0.5, 1
            self.ids['sp_l'].is_open = True

    def Gap_b(self):

        if self.ids['Gap'].state != 'down':
            self.ids['Gap'].state = 'normal'
            self.ids['Gap'].background_color = 1, 1, 1, 0.9
            self.ids['sp_g'].text = ' '

        elif self.ids['Gap'].state != 'normal':
            self.ids['Gap'].state = 'down'
            self.ids['Gap'].background_color = 6, 2, 0.5, 1
            self.ids['sp_g'].is_open = True

    def press_btn(self):
        # ボタンイベント，waitに画面遷移し、threadを開始する

        logger.debug('press_btn_SS Begin')
        self.load_parameter()
        info = self.lss.search_info(self.threshold_val, self.threshold_len, self.fill_gap)
        print(info)
        sm.add_widget(WaitScreen(name='wait'))  # wait画面を生成

        sm.current = 'wait'  # wait画面に移動

        logger.debug('press_btn_SS End')

    def load_parameter(self):
        # データを探す

        logger.debug('load_parameter Begin')

        if self.ids['Score'].state == 'down':
            self.threshold_val = int(float(self.ids['sp_s'].text))
        else:
            pass

        if self.ids['Lengs'].state == 'down':
            self.threshold_len = int(self.ids['sp_l'].text)
        else:
            pass

        if self.ids['Gap'].state == 'down':
            self.fill_gap = int(self.ids['sp_g'].text)
        else:
            pass

        logger.debug('load_parameter End')


class WaitScreen(Screen):
    """データ抽出中のwait画面"""

    def press_btn(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('press_btn_WS Begin ')

        sm.remove_widget(self)
        sm.add_widget(OutputScreen(name='out'))
        sm.current = 'out'

        logger.debug('press_btn_WS End')


class OutputScreen(Screen):
    """output画面"""

    def press_btn(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('press_btn_OS Begin')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('press_btn_OS End')


class ScreenManagement(ScreenManager):
    pass


class MobiApp(App):
    def build(self):
        logger.debug('App Begin')

        sm.add_widget(TopScreen(name='top'))
        sm.current = 'top'

        logger.debug('App End')
        return sm


if __name__ == '__main__':
    logger.debug('main Begin')

    sm = ScreenManager()  # スクリーンマネージャ
    Window.size = (400, 220)
    MobiApp().run()

    logger.debug('main End')