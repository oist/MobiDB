import sys
from search_data import SearchData
from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp
from kivy.core.window import Window
from search_data import SearchData
import config


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "MobiDB -Human"
        self.theme_cls.primary_palette = "Blue"
        self.sd = SearchData()
        super().__init__(**kwargs)

    def build(self):
        with open("./theme.kv", "r", encoding="utf8") as f:
            self.root = Builder.load_string(f.read())

    def exit(self):
        sys.exit(1)

    def btn_event(self):
        print("------------------------")
        print(config.threshold_val)
        print(config.threshold_len)
        print(config.fill_gap)
        print("------------------------")
        self.sd.get_text(self.root.ids["th_val"].text, self.root.ids["th_len"].text, self.root.ids["fill_gap"].text)
        print(config.threshold_val)
        print(config.threshold_len)
        print(config.fill_gap)
        print("------------------------")


if __name__ == "__main__":

    Window.size = (647, 400)
    MainApp().run()
