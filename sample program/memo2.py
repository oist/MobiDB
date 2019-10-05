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

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

# 日本語フォント設定
#resource_add_path('./fonts')
#LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')






class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        self.rv.data = []
        btn_list = ['a','b','c','d','e','f','g','h','i','j','k']
        for btn_list_any in btn_list:
            self.rv.data.append({'value': btn_list_any})



class VariousButtons(BoxLayout):
    def on_select_button(self, button):
        print('press:'+button.text)


class memo2App(App):
    def build(self):
        return Test()


if __name__ == '__main__':

    memo2App().run()

