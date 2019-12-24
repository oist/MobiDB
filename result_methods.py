from logging import getLogger, StreamHandler, DEBUG
import json

from result_list_button import ResultButton
from kivymd.app import MDApp
from kivy.app import App

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ResultMethods:
    def __init__(self):
        self.success_list = list()

    def store_success_list(self):
        logger.debug("result_main.py, Result, store_success_list()")

        with open('success_data.json', 'r') as fr:
            for (i, line) in enumerate(fr):
                json_dict = json.loads(line)
                self.success_list.append({'value': json_dict["protein_names"], 'index': i})

    def create_buttons(self):
        logger.debug("result_main.py, Result, create_items()")

        app = App.get_running_app()

        for item in self.success_list:
            app.root.ids.scroll.add_widget(ResultButton(text=item))

        MDApp.root = app