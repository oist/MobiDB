
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


def load_scores(json_dict):
    logger.debug('load_scores Begin')

    try:
        return json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

    except IndexError as e:
        print("load_scores IndexError: {}".format(e))

    logger.debug('load_scores End')


class VariousButtons(Screen):
    def on_select_button(self, button):
        logger.debug('on_VB_button Begin')

        print('press:'+button.text)

        logger.debug('on_VB_button End')


class TopScreen(Screen):
    """Top画面"""

    def press_enter_button(self):
        # ボタンイベント，searchに画面遷移する

        logger.debug('Start press_enter_button')

        sm.add_widget(SearchScreen(name='search'))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = 'search'  # Search画面に移動する

        logger.debug('End press_enter_button')


class SearchScreen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        logger.debug('Start init_SearchScreen')

        super(SearchScreen, self).__init__(**kwargs)
        self.threshold_value = 0
        self.threshold_lengs = 0
        self.fill_gap = 0

        logger.debug('End init_SearchScreen')

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

    def press_search_button(self):
        # ボタンイベント，waitに画面遷移し、threadを開始する

        logger.debug('Start press_search_button')

        sm.add_widget(WaitScreen(name='wait'))  # wait画面を生成
        sm.current = 'wait'  # wait画面に移動

        self.store_propaty()
        sm.read_acc = self.search_info()

        sm.add_widget(OutputScreen(name='output'))
        sm.current = 'output'

        logger.debug('End press_search_button')

    def store_propaty(self):
        # データを探す

        logger.debug('store_propaty Begin')

        if self.ids['Score'].state == 'down':
            self.threshold_value = int(float(self.ids['sp_s'].text))
        else:
            # threshold_value = ' '
            pass

        if self.ids['Lengs'].state == 'down':
            self.threshold_lengs = int(self.ids['sp_l'].text)
        else:
            # threshold_lengs = ' '
            pass

        if self.ids['Gap'].state == 'down':
            self.fill_gap = int(self.ids['sp_g'].text)
        else:
            # fill_gap = ' '
            pass

        logger.debug('store_propaty End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う
        true_id = []
        false_id = []

        with open("disorder_add_protain.mjson", 'r') as f:
            for (i, line) in enumerate(f):
                print(i)
                logger.debug('loop Begin')
                json_dict = json.loads(line)
                count = 0
                pos = self.threshold_lengs

                scores = load_scores(json_dict)
                # print(scores)
                if scores is None:
                    pass
                else:
                    while count < self.threshold_lengs and pos < len(scores):
                        if scores[pos] < self.threshold_value:
                            count = 0
                            pos += self.threshold_lengs
                        else:
                            count += 1
                            pos -= 1

                    if count >= self.threshold_lengs:
                        true_id.append(json_dict["acc"])

                    else:
                        false_id.append(i)
        logger.debug('search_info End')
        print(true_id)
        return true_id


class WaitScreen(Screen):
    """データ抽出中のwait画面"""


    def press_cancel_button(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('Start press_cancel_button')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('End press_cancel_button')


class OutputScreen(Screen):
    """output画面"""
    def __init__(self, **kwargs):
        super(OutputScreen, self).__init__(**kwargs)
#        self.rv.data = []
        #for i in sm.read_acc:
            #print(type(self.rv.data))
            #self.rv.data.append({'value': i})
        #print(self.rv.data)

    def press_return_button(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('Start press_return_button')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('End press_return_button')


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.read_acc = []


class mobiApp(App):
    def build(self):
        logger.debug('Start mobiApp')

        sm.add_widget(TopScreen(name='top'))
        sm.current = 'top'

        logger.debug('End mobiApp')
        return sm


if __name__ == '__main__':
    logger.debug('Start main')

    sm = ScreenManager()  # スクリーンマネージャ
    Window.size = (400, 220)
    mobiApp().run()

    logger.debug('end main')