# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from kivy.core.window import Window
from kivy.lang import Builder
import time
import logging
#デバック用のスレッドを残す
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
logging.debug('Starting')
logging.debug('Exiting')

class Top_Screen(Screen):
    """Top画面"""

    def press_enter_button(self):
        sm.add_widget(Search_Screen(name='search'))# 初期処理を動かしたい画面は遷移の直前に追加する
        sm.remove_widget(self)
        sm.current = 'search'#遷移

class Search_Screen(Screen):
    """search画面"""

    def __init__(self, **kwargs):
        super(Search_Screen, self).__init__(**kwargs)
        self.text = ''# 検索のキーワードを取得
        self.mythread = threading.Thread(target=self.search_to_uniprot_thread)

    def press_search_button(self):
        #ボタンが押されたときスレッドをスタート

        print("begin")
        sm.add_widget(Wait_Screen(name='wait'))# 初期処理を動かしたい画面は遷移の直前に追加する
        sm.current = 'wait'#遷移
        self.mythread.start()#スレッドスタート]
        self.mythread.setDaemon(True)


    def search_to_uniprot_thread(self):
        # Uniprotに接続
        from bioservices import UniProt
        service = UniProt()


        # 検索用の値をqueryとして代入

        query = self.ids["text_box"].text

        # データを抽出し出力.
        result = service.search("keyword:" + query)
        print(result)
        print("finish")

        sm.add_widget(Output_Screen(name='output'))# 初期処理を動かしたい画面は遷移の直前に追加する
        sm.current = 'output'

class Wait_Screen(Screen):
    """データ抽出中のwait画面"""

    def press_cancel_button(self):
        # ボタンが押されたときSearch画面に戻る

        sm.remove_widget(self)
        sm.current = 'search'

class Output_Screen(Screen):
    """output画面"""

    def press_return_button(self):
        # ボタンが押されたときSearch画面に戻る

        sm.remove_widget(self)
        sm.current = 'search'

class ScreenManagement(ScreenManager):
    pass

sm = ScreenManager()
#スクリーンマネージャ
Builder.load_file("design.kv")


class mobiApp(App):
    def build(self):
        sm.add_widget(Top_Screen(name='top'))
        sm.current = 'top'

        return sm

if __name__ == '__main__':
    Window.size = (400, 220)
    mobiApp().run()