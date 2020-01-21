import time
from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.tab import MDTabsBase

import config
from kivy.app import App


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ScreenSearchFilter(Screen, BoxLayout, MDTabsBase):
    """
    app.sm.current == "search" 時の処理

    Methods
    ----------
    btn_event(self)
        "Search with the condition"と書かれたボタンをクリックすると、
        テキストフィールドの情報をグローバル変数に格納してスクリーンを移動する。

    substitute_text(self, str = num)
        textから取得したデータは必ずstr型である。
        str型　→　float型に変換するときは、""を取り除く必要がある。

    Raises
    ------
    ValueError
    入力された文字が数字以外のときに発生。

    Notes
    ----------
    Button イベントは theme.ScreenSearchに記載。
    config.threshold_val, config.threshold_len, config.fill_gapの使い方は
    screen_wait_search.pyに記載。

    """
    submit = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenSearchFilter, self).__init__(**kwargs)

        Window.bind(on_key_down=self._on_keyboard_down)

    def btn_event(self):
        logger.debug("screen_search_main.py, ScreenSearch, btn_event()")

        try:
            config.threshold_val = self.substitute_text(self.ids["th_val"].text)
            config.threshold_len = int(self.substitute_text(self.ids["th_len"].text))
            config.fill_gap = int(self.substitute_text(self.ids["fill_gap"].text))

            print(config.threshold_val)

            self.change_screen("wait")
        except ValueError as e:
            print(e)

    def move_keyword_screen(self):
        logger.debug("screen_search_main.py, ScreenSearchFilter, move_keyword_screen()")

        self.change_screen("search_keyword")
        config.isFilter = False
        config.isKeyword = True


    def substitute_text(self, ss_text):
        logger.debug("screen_search_main.py, ScreenSearch, make_sure_text()")

        if ss_text == "":
            return 0
        else:
            return float(ss_text.replace('"', ''))

    def change_screen(self, name):
        logger.debug("screen_search_main.py, ScreenSearch, change_screen()")

        app = App.get_running_app()
        app.sm.current = name

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        app = App.get_running_app()
        if app.sm.current == "search_filter" and keycode == 40:  # 40 - Enter key pressed
            self.btn_event()
