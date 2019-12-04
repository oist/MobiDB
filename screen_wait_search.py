from logging import getLogger, StreamHandler, DEBUG
import time
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


class SearchScore(threading.Thread):
    def run(self):
        logger.debug("screen_wait_search, SearchScore, search_score()")

        # jsonファイル読み込み，条件比較を行う
        with open('success_data.mjson', 'w') as fw:
            with open("mobiDB_human.mjson", "r") as fr:
                t1 = time.time()

                for (i, line) in enumerate(fr):
                    succeeded_times = 0
                    ignored_times = 0
                    pos = config.threshold_len

                    json_dict = json.loads(line)
                    try:
                        scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
                        scores_len = len(scores)
                    except IndexError:
                        scores_len = 0

                    """
                            Examples
    ----------
    scoreの範囲は 0 < x < 1である。
    以下のようなscoreをもったプロテインがあるとする。
        score = [1, 0, 0.8, 0,8, 0,8]

    また、閾値は以下の通りとする。
        config.threshold_val    = 0.5
        config.threshold_len    = 5
        config.fill_gap         = 0 or 1

    ------------------------
        for i in len(score):
            if score[i] > threshold_val:
                i += 1
            elif score[i] < threshold_val
                i = 0

        if i >= config.threshold_len:
            print("successed")
        elif i < config.threshold_len:
            print("fail")
    ------------------------

    上記のように比較した場合の i は,
    fill_gap == 0 -> 3  fail
    fill_gap == 1 -> 5  successed
    
    と表示される
                            """
                    while pos < scores_len:

                        # scoreが閾値を超えているか判定
                        if scores[pos] > config.threshold_val:
                            succeeded_times += 1
                            pos -= 1
                            ignored_times = 0
                        else:
                            # fill_gapの処理を入れる
                            if config.fill_gap > ignored_times:
                                succeeded_times += 1
                                pos -= 1
                                ignored_times += 1
                            else:
                                succeeded_times = 0
                                pos += config.threshold_len + ignored_times
                                ignored_times = 0

                        if succeeded_times >= config.threshold_len:
                            fw.write('{}\n'.format(json.dumps(json_dict)))
                            break

                self.change_screen("out")

                t2 = time.time()
                elapsed_time = t2 - t1  # 処理にかかった時間を計算する
                print("経過時間：", elapsed_time)


    def change_screen(self, name):
        logger.debug("screen_wait_main.py, ScreenWait, change_screen()")

        app = App.get_running_app()
        app.sm.current = name

