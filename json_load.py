import json
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


class BM_Search:
    """MySQL設定"""

    def __init__(self, **kwargs):
        logging.debug('BM_Search_init start')
        with open("disorder.mjson", 'r') as f:
            self.json_dict = {i: json.loads(line) for i, line in enumerate(f)}

        self.th_val = 0.5   # 閾値
        self.th_len = 40     # どれだけ連続で続くかを決める
        self.key = []        # 条件に当てはまったIDを格納する
        self.error_id = []  # scoreがそもそも存在しなかった情報を格納する。
        self.score = []
        self.pos_latest = self.th_len-1
        self.count = 0

        logging.debug('BM_Search_init start')

    def compere_scores(self):
        logging.debug('compere_scores start')

        # 末尾が閾値以下か判定する
        print(self.pos_latest)
        print(len(self.score))
        if self.score[self.pos_latest] < 0.5:
            if self.pos_latest + self.th_len > len(self.score):
                self.pos_latest = len(self.score)
            else:
                self.pos_latest += self.th_len
            count = 0
        else:
            self.count += 1
            self.pos_latest -= 1

            if self.count == self.th_len:
                return True

        if self.count != self.th_len and self.pos_latest == len(self.score):
            return False
        else:
            self.compere_scores()

        logging.debug('compere_scores start')

    def get_scores(self):
        # scoreを取得するメソッド
        logging.debug('get_scores start')

        for i in range(1, 10):
            self.score = self.json_dict[i]["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

            if self.compere_scores():  # posは再帰するときにデータが上書きされるのを防ぐため
                self.key.append(i)

            else:
                print("2")



        logging.debug('get_scores end')



    def show_result(self):
        for k in self.key:
            print(self.key[k])
        print(self.error_id)


if __name__ == '__main__':
    """main処理"""

    logging.debug('main start')
    t1 = time.time()

    bm_ser = BM_Search()      # インスタンスを作成する

    bm_ser.get_scores()     # 探索を行い，成功したidをまとめたid[]を受け取る
    bm_ser.show_result()    # 結果を出力する

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("\n" + "経過時間：{%s}" % elapsed_time)
    logging.debug('main end')