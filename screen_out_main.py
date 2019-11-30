from logging import getLogger, StreamHandler, DEBUG
from kivy.app import App
from kivy.uix.screenmanager import Screen
from screen_out_plot import ScorePlot

import config
import matplotlib.pyplot as plt
import json
import webbrowser


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Row(Screen):
    """OutputScreenのRecycleViewで使用するボタンの設定"""
    def btn_event(self, value, i):
        if i == 0:
            logger.debug("screen_out_row.py, Row, btn_event, plot_score")
            print("Row value:" + str(value))
            score = ScorePlot(value)
            score.run()
            plt.show()
        else:
            logger.debug("screen_out_row.py, Row, btn_event, go_to_uniplot")
            with open('success_data.mjson', 'r') as fr:
                for (k, line) in enumerate(fr):
                    if k == value:
                        json_dict = json.loads(line)
                        break

            url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
            browser = webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')
            browser.open(url)


class ScreenOut(Screen):
    def on_enter(self):
        logger.debug("screen_out_main.py, ScreenOut, on_enter()")

        with open('success_data.mjson', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                self.rv.data.append({'value': json_dict["protein names"], 'index': i})

    def btn_event(self, i):
        logger.debug("screen_out_main.py, ScreenOut, btn_event()")

        if i == 0:
            self.filter_keyword()
        elif i == 1:
            self.sort_abc()
        else:
            self.change_screen("search")

    def sort_abc(self):
        logger.debug("screen_out_main.py, ScreenOut, sort_abc()")

        self.rv.data = sorted(self.rv.data, key=lambda x: x['value'])

    def filter_keyword(self):
        logger.debug("screen_out_main.py, ScreenOut, filter_keyword()")

        config.keyword = self.ids["keyword"].text
        temp = []

        with open('success_data.mjson', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                if config.keyword in json_dict["protein names"]:
                    temp.append({'value': json_dict["protein names"], 'index': i})

            self.rv.data = temp

    def change_screen(self, name):
        logger.debug("screen_top_main.py, ScreenOut, change_screen()")

        app = App.get_running_app()
        app.sm.current = name
