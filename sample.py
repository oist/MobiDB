from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.tab import MDTabsBase

kv = """
<Example@BoxLayout>:
    orientation: "vertical"

    MDToolbar:
        title: app.title
        md_bg_color: app.theme_cls.primary_color
        background_palette: "Primary"
        left_action_items: [["menu", lambda x: x]]

    MDTabs:
        id: android_tabs


<MyTab>:

    FloatLayout:

        MDLabel:
            text: "Content"
            halign: "center"
            theme_text_color: "Primary"
            font_style: "H6"


"""


class MyTab(BoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    list_name_icons = ListProperty(list(md_icons.keys())[0:15])

    def __init__(self, **kwargs):
        self.title = "KivyMD Examples - Tabs"
        super().__init__(**kwargs)

    def build(self):
        Builder.load_string(kv)
        screen = Factory.Example()

        for name_tab in self.list_name_icons:
            tab = MyTab(text=name_tab)
            screen.ids.android_tabs.add_widget(tab)
        self.root = screen


if __name__ == "__main__":
    MainApp().run()