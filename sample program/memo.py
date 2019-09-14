"""from kivy.app import App
from kivy.lang import Builder

kv = '''
AnchorLayout:
    anchor_x: 'center'
    anchor_y: 'center'
    Button:
        size: 200, 200
        size_hint: None, None
        Image:
            source: "kivy-logo-black-256.png"
            center_x: self.parent.center_x
            center_y: self.parent.center_y
'''

class MyApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    MyApp().run()"""

"""from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

import glob

class MyImage(Image):
    def on_touch_down(self, touch):
     if self.collide_point(*touch.pos):
      print (self.source)

class Image_Gallery(GridLayout):

    def __init__(self, **kwargs):
     super(Image_Gallery, self).__init__(**kwargs)
     images = glob.glob('kusunoki.jpg')
     self.cols = 3
     for img in images:
      thumb = MyImage(source=img)
      self.add_widget(thumb)


class mainApp(App):


    def build(self):
     return Image_Gallery()


if __name__ == '__main__':
    mainApp().run()"""

"""import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty


class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)


class PicturesApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root
        filename = "kusunoki.jpg"
        try:
            # load the image
            picture = Picture(source=filename, rotation=randint(-30, 30))
            # add to the main field
            root.add_widget(picture)

        except Exception as e:
            Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()""


"""
"""import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty


class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)


class PicturesApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root
        filename = "kusunoki.jpg"
        try:
            # load the image
            picture = Picture(source=filename, rotation=randint(-30, 30))
            # add to the main field
            root.add_widget(picture)

        except Exception as e:
            Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()""


"""
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import threading
from kivy.core.window import Window
from kivy.lang import Builder
from logging import getLogger, StreamHandler, DEBUG
import time
from kivy.base import runTouchApp
from kivy.lang import Builder

from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
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
        # ボタンイベント，searchに画面遷移する

        logger.debug('Start press_enter_button')

        sm.add_widget(Search_Screen(name='search'))  # Search画面を生成する
        sm.remove_widget(self)  # Top画面を破棄する
        sm.current = 'search'  # Search画面に移動する

        logger.debug('End press_enter_button')


class Search_Screen(Screen):
    """search画面"""

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

        t1 = time.time()  # 測定開始

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