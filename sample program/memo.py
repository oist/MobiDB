
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import threading
from kivy.core.window import Window
from logging import getLogger, StreamHandler, DEBUG
import time
from kivy.clock import Clock
from kivy.uix.image import Image

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug('hello')


class Top_Screen(Screen):

    """Top画面"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.press_enter_button, 10.0)

    def press_enter_button(self, dt):
    # ボタンイベント，searchに画面遷移する

        logger.debug('Start press_enter_button')

        sm.add_widget(Search_Screen(name='search'))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = 'search'  # Search画面に移動する

        logger.debug('End press_enter_button')


class Search_Screen(Screen):
    """search画面"""

    def score_b(self):
        if self.ids['Score'].state != 'down':
            self.ids['Score'].state = 'normal'
            self.ids['Score'].background_color = 1, 1, 1, 0.9
            self.ids['sp_s'].text = ' '

        elif self.ids['Score'].state != 'normal':
            self.ids['Score'].state = 'down'
            self.ids['Score'].background_color = 7, 1.1, 0.3, 1
            self.ids['sp_s'].is_open = True

    def lengs_b(self):
        if self.ids['Lengs'].state != 'down':
            self.ids['Lengs'].state = 'normal'
            self.ids['Lengs'].background_color = 1, 1, 1, 0.9
            self.ids['sp_l'].text = ' '

        elif self.ids['Lengs'].state != 'normal':
            self.ids['Lengs'].state = 'down'
            self.ids['Lengs'].background_color = 7, 1.1, 0.3, 1
            self.ids['sp_l'].is_open = True

    def gap_b(self):

        if self.ids['Gap'].state != 'down':
            self.ids['Gap'].state = 'normal'
            self.ids['Gap'].background_color = 1, 1, 1, 0.9
            self.ids['sp_g'].text = ' '

        elif self.ids['Gap'].state != 'normal':
            self.ids['Gap'].state = 'down'
            self.ids['Gap'].background_color = 7, 1.1, 0.3, 1
            self.ids['sp_g'].is_open = True

    def __init__(self, **kwargs):
        logger.debug('Start init_SearchScreen')

        super(Search_Screen, self).__init__(**kwargs)

        self.connect_mythread = threading.Thread(target=self.connect_uniprot_thread)  # Uniprotに接続するためのスレッドを生成
        self.connect_mythread.start()  # Uniprotに接続開始

        logger.debug('End init_SearchScreen')

    def connect_uniprot_thread(self):
        # Uniprotに接続する

        logger.debug('Start connect_uniprot_thread')

        from bioservices import UniProt  # Uniprotのメソッドをインポート
        self.service = UniProt()  # ネットに接続する

        logger.debug('End connect_uniprot_thread')

    def press_search_button(self):
        # ボタンイベント，waitに画面遷移し、threadを開始する

        logger.debug('Start press_search_button')

        self.connect_mythread.join()  # Uniprotに接続するまで待機

        sm.add_widget(Wait_Screen(name='wait'))  # wait画面を生成
        sm.current = 'wait'  # wait画面に移動

        self.search_mythread = threading.Thread(target=self.search_to_uniprot_thread)  # 検索するためのスレッドを用意する
        self.search_mythread.start()  # 検索するためのスレッドをスタートする

        logger.debug('End press_search_button')

    def search_to_uniprot_thread(self):
        # データを探す

        logger.debug('Start search_to_uniprot_thread')

        if self.ids['Score'].state == 'down':
            Score = self.ids['sp_s'].text
        else:
            #Score = ' '
            pass

        if self.ids['Lengs'].state == 'down':
            Lengs = self.ids['sp_l'].text
        else:
            #Lengs = ' '
            pass

        if self.ids['Gap'].state == 'down':
            Gap = self.ids['sp_g'].text
        else:
            #Gap = ' '
            pass

        #print(Score, Lengs, Gap)

        t1 = time.time()  # 測定開始

        # keyword = Score + Lengs + Gap

        query = self.ids["text_box"].text  # 検索用の値をqueryとして代入
        result = self.service.search("keyword:" + query)  # データを抽出し出力.

        # query = "GL1147"
        # result = self.service.search(query)

        t2 = time.time()
        print(result)
        # 測定終了
        elapsed_time = t2 - t1  # 処理にかかった時間を計算する
        print(f"経過時間：{elapsed_time}")

        sm.add_widget(Output_Screen(name='output'))
        sm.current = 'output'

        logger.debug('End search_to_uniprot_thread')


class Wait_Screen(Screen):
    """データ抽出中のwait画面"""


    def press_cancel_button(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('Start press_cancel_button')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('End press_cancel_button')


class Output_Screen(Screen):
    """output画面"""

    def press_return_button(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('Start press_return_button')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('End press_return_button')


class ScreenManagement(ScreenManager):
    pass


class memoApp(App):
    def build(self):
        logger.debug('Start memoApp')

        sm.add_widget(Top_Screen(name='top'))
        sm.current = 'top'

        logger.debug('End memoApp')
        return sm


if __name__ == '__main__':
    logger.debug('Start main')

    sm = ScreenManager()  # スクリーンマネージャ
    Window.size = (400, 220)
    memoApp().run()

    logger.debug('end main')