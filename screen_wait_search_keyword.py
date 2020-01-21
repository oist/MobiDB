from logging import getLogger, StreamHandler, DEBUG
import json
import config
import threading
from kivy.app import App

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class SearchKeyword(threading.Thread):

    def __init__(self):
        super().__init__()
        self.alive = True

    def run(self):
        logger.debug("screen_wait_search_keyword, SearchKeyword, search_score()")

        with open('success_data.json', 'w') as fw:
            with open("mobiDB_human.json", "r") as fr:
                for (i, line) in enumerate(fr):
                    json_dict = json.loads(line)
                    succeeded_times = 0
                    ignored_times = 0
                    current_pos = config.threshold_len

                    try:
                        if config.keyword in json_dict["protein_names"]:
                            fw.write('{}\n'.format(json.dumps(json_dict)))

                    except IndexError:
                        pass
                    if not self.alive:
                        break
                else:
                    self.change_screen("out")

    def change_screen(self, name):
        logger.debug("screen_wait_search_keyword.py, SearchKeyword, change_screen()")

        app = App.get_running_app()
        app.sm.current = name

    def kill(self):
        logger.debug("screen_wait_search_keyword.py, SearchKeyword, kill()")
        self.alive = False
