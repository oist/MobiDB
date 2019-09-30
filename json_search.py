import json
import logging
import time
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


class BM_Search:

    def __init__(self, **kwargs):
        logging.debug('BM_Search_init start')
        with open("disorder.mjson", 'r') as f:
            self.json_dict = {i: json.loads(line) for i, line in enumerate(f)}

        self.th_val = 0.5   # 閾値
        self.th_len = 40     # どれだけ連続で続くかを決める
        self.sucess_id = []        # 条件に当てはまったIDを格納する
        self.false_id = []
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。
        self.score = []

        logging.debug('BM_Search_init start')

    def get_scores(self):
        # scoreを取得するメソッド
        logging.debug('get_scores start')

        for i in range(0, 71725):
            # カウントとポジションを初期化する
            self.count = 0
            print("number :", i)

            self.pos_latest = self.th_len

            # カウント数がスレッショルドレングスを超える or ポジションがscoreの最大を超えるとループを抜ける
            while self.count < self.th_len:
                try:
                    self.score = self.json_dict[i]["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
                    if len(self.score) < self.th_len:
                        print("Nothing")
                        break

                except:
                    self.error_id.append(i)
                    break

                print("count", self.count)
                print("pos", self.pos_latest)
                try:
                    # scoreが小さい場合，カウントを0に戻し，th_len分移動する。th_lenを入れるのは末尾から比較するため
                    if self.score[self.pos_latest] < self.th_val:
                        self.pos_latest += self.th_len
                        self.count = 0
                    # scoreが大きい場合，カウントを+1し，一つ下げる移動する。
                    else:
                        self.count += 1
                        self.pos_latest -= 1

                    if self.pos_latest >= len(self.score):
                        print("Nothing")
                        break

                except:
                    self.error_id.append(i)
                    print("error")
                    break


            # 格納に成功したとき，表示する
            if self.count >= self.th_len:
                self.sucess_id.append(i)
            else:
                self.false_id.append(i)

        print("sucess :", self.sucess_id)
        print("false :", self.false_id)
        print("error", self.error_id)


        logging.debug('get_scores end')



if __name__ == '__main__':
    """main処理"""

    logging.debug('main start')
    t1 = time.time()

    bm_ser = BM_Search()      # インスタンスを作成する

    bm_ser.get_scores()     # 探索を行い，成功したidをまとめたid[]を受け取る


    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("\n" + "経過時間：{%s}" % elapsed_time)
    logging.debug('main end')