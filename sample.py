from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

kv = """
<VariousButtons>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Button:
        text: root.value
        background_normal: ''
        background_color: 0.5, 0.5, 0.75, 1
        color: 1, 1 ,1 ,1
        on_press: root.on_select_button(self)
<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: sp(60) #スクロール速度
        bar_width: sp(20)
        viewclass: 'VariousButtons'
        RecycleBoxLayout:
            default_size: None, sp(160)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(8)
"""

Builder.load_string(kv)


class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        self.rv.data = []
        print(type(self.rv.data))

        btn_list = ['ひつまぶし','味噌煮込みうどん','味噌カツ','台湾ラーメン' \
                    ,'手羽先','小倉トースト','きしめん','あんかけスパ','どて煮' \
                    ,'ういろう','甘口バナナスパ']
        print(type(btn_list))
        for btn_list_any in btn_list:
            self.rv.data.append({'value': btn_list_any})



class VariousButtons(BoxLayout):
    def on_select_button(self, button):
        print('press:'+button.text)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()
