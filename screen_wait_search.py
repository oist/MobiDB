from logging import getLogger, StreamHandler, DEBUG
import time
import json
import config


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class SearchScore:
    def search_score(self):
        logger.debug("screen_wait_search, SearchScore, search_score()")
        
        # jsonファイル読み込み，条件比較を行う
        with open('success_data.mjson', 'w') as fw:
            with open("disorder_add_protain.mjson", "r") as fr:
                t1 = time.time()

                for (i, line) in enumerate(fr):
                    json_dict = json.loads(line)

                    succeeded_times = 0
                    ignored_times = 0
                    pos = config.threshold_len

                    try:
                        # keywordが含まれているか判定
                        if config.keyword not in json_dict["protein names"]:
                            continue

                        scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

                        while pos < len(scores):

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

                    except IndexError:
                        pass

                t2 = time.time()
                elapsed_time = t2 - t1  # 処理にかかった時間を計算する
                print("経過時間：", elapsed_time)

        """
        score[pos]              : pos番目のscore値。
        config.threshold_val    : score値用の閾値。
        config.threshold_len    : 閾値以上が何回続けばよいかを決める変数。
        succeeded_times         : scores[pos] > config.threshold_val が True であった回数を保持する変数。

        whileループは　succeeded_times > threshold_len のときに抜ける。

        config.fill_gap         : 閾値以下を何回まで許すかを決める変数　
                                  例）　score[ 1, 1, 0, 0, 1, 1 ], threshold_val = 0.5 とする。
                                     ---------------------------------------------
                                        for i in len(score):
                                            if score[i] > threshold_val:
                                                i += 1
                                            elif score[i] < threshold_val
                                                i = 0
                                     ---------------------------------------------
                                     上記のように比較した場合の出力は、
                                        fill_gap == 1 -> 2
                                        fill_gap == 2 -> 6
                                     と違いがでる。
                                     このように、閾値以下を何回許すかを決める変数をfill_gapとする。

        ignored_times           : 無視した回数の合計を保持する変数。
        """