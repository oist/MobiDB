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


class TopScreen(Screen):
    """Top画面"""

    def btnClicked_top(self):
        logger.debug('btnClicked_top Begin')

        sm.add_widget(SearchScreen(name='search'))         # Search画面を生成する
        sm.remove_widget(self)                              # Top画面を破棄する
        sm.current = 'search'                               # Search画面に移動する

        logger.debug('btnClicked_top End')


class SearchScreen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        logger.debug('ss_init Begin')

        super(SearchScreen, self).__init__(**kwargs)

        self.con_mythread = threading.Thread(target=self.th_uniConn)   # Uniprotに接続するためのスレッドを生成
        self.con_mythread.start()                                                  # Uniprotに接続開始

        logger.debug('ss_init End')

    def th_uniConn(self):
        logger.debug('th_uniConn Begin')

        from bioservices import UniProt     # Uniprotのメソッドをインポート
        self.service = UniProt()            # ネットに接続する

        logger.debug('th_uniConn End')

    def btnClicked_search(self):
        logger.debug('btnClicked_search Begin')

        self.con_mythread.join()                # Uniprotに接続するまで待機

        sm.add_widget(WaitScreen(name='wait'))     # wait画面を生成
        sm.current = 'wait'                         # wait画面に移動

        self.search_mythread = threading.Thread(target=self.th_uniData_search)   # 検索するためのスレッドを用意する
        self.search_mythread.start()                                                    # 検索するためのスレッドをスタートする

        logger.debug('btnClicked_search End')

    def th_uniData_search(self):
        logger.debug('th_uniData_search Begin')
        t1 = time.time()                                   # 測定開始
        
        query = self.ids["text_box"].text                  # 検索用の値をqueryとして代入
        result = self.service.search("keyword:" + query)   # データを抽出し出力.

        # query = "GL1147"
        # result = self.service.search(query)

        t2 = time.time()
        print(result)
        elapsed_time = t2 - t1                             # 処理にかかった時間を計算する
        print("経過時間：", elapsed_time)

        sm.add_widget(OutputScreen(name='output'))
        sm.current = 'output'

        logger.debug('th_uniData_search End')


class WaitScreen(Screen):
    """データ抽出中のwait画面"""

    def btnClicked_wait(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('btnClicked_wait Start')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('btnClicked_wait End')


class OutputScreen(Screen):
    """output画面"""

    def btnClicked_out(self):
        # ボタンが押されたときSearch画面に戻る

        logger.debug('btnClicked_out Begin')

        sm.remove_widget(self)
        sm.current = 'search'

        logger.debug('btnClicked_out End')


class ScreenManagement(ScreenManager):
    pass


class MobiApp(App):
    def build(self):
        logger.debug('MobiApp Begin')

        sm.add_widget(TopScreen(name='top'))
        sm.current = 'top'

        logger.debug('MobiApp End')
        return sm


if __name__ == '__main__':
    logger.debug('main Begin')

    sm = ScreenManager()            # スクリーンマネージャ
    Window.size = (400, 220)
    MobiApp().run()

    logger.debug('main End')