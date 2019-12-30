"""from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config

Config.set('graphics', 'width', '150')
Config.set('graphics', 'height', '40')

class Display(Widget):
    def measure(self):
        self.ids.la01.text="Push"   #ここを追加

class TestApp(App):
    def build(self):
        disp=Display()
        return disp

if __name__ == '__main__':
    TestApp().run()"""

"""from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class PhilippsRadioApp(App):
    pass

class RadioRoot(BoxLayout):

    def previous(self):
        print("Previous")

    def play_stop(self):
        print("Play/Stop")


    def next(self):
        print("Next")

    def shutdown(self):
        print("Shutdown")

    def channel(self, num):
        print("Channel")


if __name__ == '__main__':
    PhilippsRadioApp().run()"""

"""from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class MyButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.source = 'atlas://data/images/defaulttheme/checkbox_off'

    def on_press(self):
        self.source = 'atlas://data/images/defaulttheme/checkbox_on'

    def on_release(self):
        self.source = 'atlas://data/images/defaulttheme/checkbox_off'


class SampleApp(App):
    def build(self):
        return MyButton()


SampleApp().run()"""

"""from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class IconButton(ButtonBehavior, Image):
    def on_press(self):
        print("on_press")


class SampleApp(App):
    def build(self):
        return IconButton()


SampleApp().run()"""

"""from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class RootWidget(FloatLayout):
    pass

class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        print ('pressed')

Builder.load_string(""
<RootWidget>:  
    ImageButton:  
        source:'kusunoki.jpg'  
        size:  .400, .220  
"")

class The_AssignmentApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    The_AssignmentApp().run()"""

"""from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

Builder.load_string(
<ImageButton>:  
    FloatLayout:  
        Image:  
            source:'kusunoki.jpg'  
            size:400, 220 
)

class ImageButton(ButtonBehavior,FloatLayout, Image):
    def on_press(self):
        print ('pressed')


class The_AssignmentApp(App):
    def build(self):
        return ImageButton()

if __name__ == "__main__":
    The_AssignmentApp().run()"""
"""
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_string('''
<CustomLayout>
    canvas.before:
        BorderImage:
            # BorderImage behaves like the CSS BorderImage
            border: 10, 10, 10, 10
            texture: self.background_image.texture
            pos: self.pos
            size: self.size

<RootWidget>
    CustomLayout:
        size_hint: .9, .9
        pos_hint: {'center_x': .5, 'center_y': .5}
        rows:1
        Label:
            text: "I don't suffer from insanity, I enjoy every minute of it"
            text_size: self.width-20, self.height-20
            valign: 'top'
        Label:
            text: "When I was born I was so surprised; I didn't speak for a year and a half."
            text_size: self.width-20, self.height-20
            valign: 'middle'
            halign: 'center'
        Label:
            text: "A consultant is someone who takes a subject you understand and makes it sound confusing"
            text_size: self.width-20, self.height-20
            valign: 'bottom'
            halign: 'justify'
''')


class CustomLayout(GridLayout):

    background_image = ObjectProperty(
        Image(
            source='wait2.gif',
            anim_delay=0.25))


class RootWidget(FloatLayout):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    MainApp().run()"""

"""from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock

import os
import glob
import random
import threading
from time import sleep


class ImageSlideWidget(Widget):
    image = ObjectProperty(None)
    image_src = StringProperty('')

    def __init__(self, **kwargs):
        super(ImageSlideWidget, self).__init__(**kwargs)
        self.image_src = 'wait2.zip'
        Clock.schedule_interval(self.update, 0.01)
        pass

    def update(self, dt):
        self.image.reload()

    def set_image_src(self, src):
        self.image_src = src

    def slides(app, a):
        dir_name = "./images"
        files = glob.glob(os.path.join(dir_name, "*.png"))

        while True:
            random.shuffle(files)
            for file_name in files:
                sleep(1)
                app.set_image_src(file_name)

    def memo2app_run(app, a):
        app.run()

    if __name__ == '__main__':
        app =App()

        th_app = threading.Thread(target=memo2app_run, args=(app, 0), daemon=True)
        th_app.start()

        sleep(1)

        th_slide = threading.Thread(target=slides, args=(app, 0), daemon=True)
        th_slide.start()

        input('Pless any key.\n')"""

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

"""from kivy.base import runTouchApp
from kivy.lang import Builder


kv = '''
<ButImage@ButtonBehavior+Image>

FloatLayout:
    ButImage:
        
        size_hint: .5, .5
        
        allow_stretch: True
        keep_ratio: False
        source: './wait2.gif'
        


'''

if __name__ == '__main__':
    runTouchApp(Builder.load_string(kv))"""
"""
from kivy.base import runTouchApp

from kivy.app import App
from kivy.uix.button import Label, Button
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.Sample1Btn = ToggleButton(text="Sample1", font_size="18sp",
                                       state='down', size_hint=(.3, .15), pos_hint={'center_x': .2, 'center_y': .7})
        self.Sample1Btn.bind(on_press=self.Sample1Btncallback)
        self.add_widget(self.Sample1Btn)

        self.Sample2Btn = ToggleButton(text="Sample2", font_size="18sp",
                                       size_hint=(.3, .15), pos_hint={'center_x': .2, 'center_y': .5})
        self.Sample2Btn.bind(on_press=self.Sample2Btncallback)
        self.add_widget(self.Sample2Btn)

    def Sample1Btncallback(self, instance):
        if self.Sample1Btn.state != 'down':
            self.Sample1Btn.state = 'normal'
        elif self.Sample1Btn.state != 'normal':
            self.Sample1Btn.state = 'down'
    def Sample2Btncallback(self, instance):
        if self.Sample2Btn.state != 'down':
            self.Sample2Btn.state = 'normal'
        elif self.Sample2Btn.state != 'normal':
            self.Sample2Btn.state = 'down'


class memo2App(App):
    def build(self):
        self.root = root = RootWidget()
        self.title = 'Test Sample'
        return self.root


memo2App().run()"""
"""from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.app import App
class MatchView(RecycleView):

    def __init__(self,**kwargs):
        super(MatchView,self).__init__(**kwargs)

        self.titles     = ['aiueo','tyuukansikenyada','marasonnkirai','amerika','jouho','ai','art']
        self.match_data = {}

    def match(self,word):
        self.data = [{'text': title.replace(word, '[/color]' + word + '[/color]')}
                     for title in self.titles
                     if title.find(word.lower()) >= 0 or title.find(word.upper()) >= 0]



class memo2App(App):
    pass

memo2App().run()"""

from random import sample
from string import ascii_lowercase
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

# 日本語フォント設定
#resource_add_path('./fonts')
#LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')






class Test(BoxLayout):
    """search画面"""

    def search_criteria_button(self):
        if self.ids['Score'].state != 'down':
            self.ids['sp_s'].text = ' '

        elif self.ids['Score'].state != 'normal'and self.ids['Score'].on_press:
            self.ids['sp_s'].is_open = True
            self.ids['sp_l'].is_open = False
            self.ids['sp_g'].is_open = False

        if self.ids['Lengs'].state != 'down':
            self.ids['sp_l'].text = ' '

        elif self.ids['Lengs'].state != 'normal'and self.ids['Lengs'].on_press:
            self.ids['sp_l'].is_open = True
            self.ids['sp_s'].is_open = False
            self.ids['sp_g'].is_open = False

        if self.ids['Gap'].state != 'down':
            self.ids['sp_g'].text = ' '

        elif self.ids['Gap'].state != 'normal'and self.ids['Gap'].on_press:
            self.ids['sp_g'].is_open = True
            self.ids['sp_s'].is_open = False
            self.ids['sp_l'].is_open = False

    """def lengs_b(self):
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
            self.ids['sp_g'].is_open = True"""

class memo2App(App):
    def build(self):
        return Test()


if __name__ == '__main__':

<<<<<<< HEAD:sample_program/mobi_related/memo2.py
    memo2App().run()

=======
    memo2App().run()"""
"""
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle

class anime(Widget):
    wimg = Image(source='loading4.gif')

class memo2App(App):
    def __init__(self, **kwargs):
        super(memo2App, self).__init__(**kwargs)
        self.root = RelativeLayout()

        animated_icon = Image(source='loading4.gif')
        animated_icon.bind(texture=self.update_texture)

        self.r = Rectangle(texture=animated_icon.texture, size_hint=(1, 0.4), pos=(100, 100))
        self.root.canvas.add(self.r)

    def update_texture(self, instance, value):
        self.r.texture = value

    def build(self):
        return self.root


if __name__ == '__main__':
    memo2App().run()"""

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder





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
from kivy.clock import Clock
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
        Window.size = (400, 220)
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


class memo2App(App):
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
    with open("./memo.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    Window.size = (400, 220)

    sm = ScreenManager()  # スクリーンマネージャ
    memo2App().run()

    logger.debug("main End")
>>>>>>> e88d7f1f5641455c6c71c440a7d505980a13807d:sample program/design_related/memo2.py
