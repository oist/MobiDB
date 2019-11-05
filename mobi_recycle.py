from kivy.config import Config
from random import sample
from string import ascii_lowercase
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from logging import getLogger, StreamHandler, DEBUG

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '150')

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
logger.debug("hello")


class ListScreen(Screen):

    def populate(self):
        logger.debug("populate")
        self.rv.data = [{'value': ''.join(sample(ascii_lowercase, 6))}
                        for x in range(50)]
        print(self.rv.data)


    def sort(self):
        logger.debug("sort")
        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])

    def clear(self):
        logger.debug("clear")
        self.rv.data = []

    def insert(self, value):
        logger.debug("insert")
        self.rv.data.insert(0, {'value': value or 'default value'})

    def update(self, value):
        logger.debug("update")
        if self.rv.data:
            self.rv.data[0]['value'] = value or 'default new value'
            self.rv.refresh_from_data()

    def remove(self):
        logger.debug("remove")
        if self.rv.data:
            self.rv.data.pop(0)

    def print(self):
        logger.debug("print")

    def Load(self):
        logger.debug("Load")


class Row(Screen):
    def print(self):
        logger.debug("print")


class LoginScreen(Screen):
    def Login(self, ti):
        app = App.get_running_app()

        app.user = ti.text

        if ti.text.isdigit():
            print("Login:[%s]" % ti.text)
            Window.size = (800, 600)
            sm.current = "List"
            sm.remove_widget(self)
        else:
            print("Wrong ID!")
        ti.text = ""

    def Cancel(self, ti):
        print("Cancel")
        ti.text = ""


class TestApp(App):
    user = StringProperty(None)

    def build(self):

        sm.add_widget(LoginScreen(name="LogIn"))
        sm.add_widget(ListScreen(name="List"))
        return sm


if __name__ == '__main__':
    with open("./mobi_recycle.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())
    sm = ScreenManager()
    TestApp().run()