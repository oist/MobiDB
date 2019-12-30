
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import threading
import json
from logging import getLogger, StreamHandler, DEBUG
import time

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class LimitScoreSearch:
    def __init__(self):
        logger.debug('LSS_init Begin')

        self.th_val = 0.7  # 閾値
        self.th_len = 40  # どれだけ連続で続くかを決める
        self.success_id = []  # 条件に当てはまったIDを格納する
        self.false_id = []
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。

        logger.debug('LSS_init End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う
        with open('success_data.mjson', 'w') as fw:
            with open('error_data.mjson', 'w') as fw2:
                with open("disorder.mjson", 'r') as f:
                    for (i, line) in enumerate(f):
                        json_dict = json.loads(line)
                        try:
                            a = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
                            fw.write('{}\n'.format(json.dumps(json_dict, indent=4)))

                        except IndexError as e:
                            fw2.write('{}\n'.format(json.dumps(json_dict, indent=4)))


        logger.debug('search_info End')



if __name__ == '__main__':
    logger.debug('main Begin')
    t1 = time.time()

    lss = LimitScoreSearch()  # インスタンスを作成する
    lss.search_info()
    print(lss.success_id)
    print(lss.false_id)
    print(lss.error_id)

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logger.debug('main End')
