# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from kivy.core.window import Window
from kivy.lang import Builder
from logging import getLogger, StreamHandler, DEBUG
import time

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

    def press_enter_button(self):
        #ボタンイベント，searchに画面遷移する
        logger.debug('Start press_enter_button')

        sm.add_widget(Search_Screen(name='search'))         # Search画面を生成する
        sm.remove_widget(self)                              # Top画面を破棄する
        sm.current = 'search'                               # Search画面に移動する

        logger.debug('End press_enter_button')


class Search_Screen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        logger.debug('Start init_SearchScreen')

        super(Search_Screen, self).__init__(**kwargs)

        self.connect_mythread = threading.Thread(target=self.connect_uniprot_thread)   # Uniprotに接続するためのスレッドを生成
        self.connect_mythread.start()                                                  # Uniprotに接続開始

        logger.debug('end init_SearchScreen')

    def connect_uniprot_thread(self):
        # Uniprotに接続する

        logger.debug('Start connect_uniprot_thread')

        from bioservices import UniProt     # Uniprotのメソッドをインポート
        self.service = UniProt()            # ネットに接続する

        logger.debug('Start connect_uniprot_thread')

    def press_search_button(self):
        #ボタンイベント，waitに画面遷移し、threadを開始する

        logger.debug('Start press_search_button')
        # t1 = time.time()                             # 測定開始

        self.wait_screen_mythread = threading.Thread(target=self.wait_screen_thread)
        self.wait_screen_mythread.start()
        self.wait_screen_mythread.join()
        self.connect_mythread.join()

        self.search_mythread = threading.Thread(target=self.search_to_uniprot_thread)
        self.search_mythread.start()
        self.search_mythread.join()

        self.output_screen_mythread = threading.Thread(target=self.output_screen_thread)
        self.output_screen_mythread.start()
        self.output_screen_mythread.join()


        print(self.result)

        # t2 = time.time()                              # 測定終了
        # elapsed_time = t2 - t1                        # 処理にかかった時間を計算する
        # print(f"経過時間：{elapsed_time}")
        logger.debug('End press_search_button')


    def search_to_uniprot_thread(self):
        # データを探す

        logger.debug('Start search_to_uniprot_thread')

        query = self.ids["text_box"].text                       # 検索用の値をqueryとして代入
        self.result = self.service.search("keyword:" + query)   # データを抽出し出力.

        logger.debug('End search_to_uniprot_thread')


    def wait_screen_thread(self):
        # ボタンイベント，waitに画面遷移する

        logger.debug('Start wait_Screen_thread')

        sm.add_widget(Wait_Screen(name='wait'))
        sm.current = 'wait'

        logger.debug('End wait_Screen_thread')

    def output_screen_thread(self):
        # ボタンイベント，waitに画面遷移する

        logger.debug('Start wait_Screen_thread')

        sm.add_widget(Output_Screen(name='output'))
        sm.current = 'output'

        logger.debug('End wait_Screen_thread')


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



class mobiApp(App):
    def build(self):
        logger.debug('Start mobiApp')

        sm.add_widget(Top_Screen(name='top'))
        sm.current = 'top'

        logger.debug('End mobiApp')
        return sm



if __name__ == '__main__':
    logger.debug('Start main')

    sm = ScreenManager()            # スクリーンマネージャ
    Builder.load_file("design.kv")  # kvファイルをロードする
    Window.size = (400, 220)
    mobiApp().run()

    logger.debug('end main')