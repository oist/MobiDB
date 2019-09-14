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

from kivy.base import runTouchApp
from kivy.lang import Builder


kv = '''
<ButImage@ButtonBehavior+Image>

FloatLayout:
    ButImage:
        
        size_hint: .5, .5
        
        allow_stretch: True
        keep_ratio: False
        source: 'wait2.gif'
        


'''

if __name__ == '__main__':
    runTouchApp(Builder.load_string(kv))