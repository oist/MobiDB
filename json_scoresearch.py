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

        self.th_val = 0.5  # 閾値
        self.th_len = 40  # どれだけ連続で続くかを決める
        self.success_id = []  # 条件に当てはまったIDを格納する
        self.false_id = []
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。

        logger.debug('LSS_init End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う

        with open("disorder.mjson", 'r') as f:
            for (i, line) in enumerate(f):
                json_dict = json.loads(line)
                count = 0
                pos = self.th_len

                scores = self.load_scores(json_dict, i)
                # print(scores)
                if scores is None:
                    pass
                else:
                    while count < self.th_len and pos < len(scores):
                        if scores[pos] < self.th_val:
                            count = 0
                            pos += self.th_len
                        else:
                            count += 1
                            pos -= 1

                    if count >= self.th_len:
                        self.success_id.append(i)
                    else:
                        self.false_id.append(i)

        print("success :", self.success_id)
        print("false :", self.false_id)
        print("error", self.error_id)

        logger.debug('search_info End')

    def load_scores(self, json_dict, i):
        logger.debug('load_scores Begin')

        try:
            return json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

        except IndexError as e:
            print("load_scores IndexError: {}".format(e))
            self.error_id.append(i)

        logger.debug('load_scores End')


if __name__ == '__main__':
    logger.debug('main Begin')

    t1 = time.time()

    # main処理
    lss = LimitScoreSearch()  # インスタンスを作成する
    lss.search_info()  # 探索を行い，成功したidをまとめたid[]を受け取る

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logger.debug('main End')
