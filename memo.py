

class LimitScoreSearch:
    """閾値以上のScoreを探索する"""

    def worker(self, fr, fw):

        times = [0, 0, 0, 0]
        """
        times[0]: succeeded_times 
        times[1]: pos  
        times[2]: ignored_times
        times[3]: current_ignored_times

        """

        ignored_times = 0
        current_ignored_times = 0
        succeeded_times = 0

        for (i, line) in enumerate(fr):
            json_dict = json.loads(line)
            pos = config.threshold_len  # score[]のポジションを決める変数

            try:
                # キーワードが含まれているかを判別する
                if config.keyword not in json_dict["protein names"]:
                    continue

                scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]

                """
                score[pos]              : pos番目のscore値。
                config.threshold_val    : score値用の閾値。
                config.threshold_len    : 閾値以上が何回続けばよいかを決める変数。
                succeeded_times         : scores[pos] > config.threshold_val が True であった回数を保持する変数。

                whileループは　succeeded_times > threshold_len のときに抜ける。

                config.fill_gap         : 閾値以下を何回まで許すかを決める変数　
                                        　例）　score[ 1, 1, 0, 1, 1, 1 ], threshold_val = 0.5 とする。
                                                ---------------------------------------------
                                                for i in len(score):
                                                    if score[i] > threshold_val:
                                                        i += 1
                                                    elif score[i] < threshold_val
                                                        i = 0
                                                ---------------------------------------------    
                                                上記のように比較した場合の出力は、
                                                fill_gap == 0 -> 3
                                                fill_gap == 1 -> 5
                                                と違いがでる。
                                                このように、閾値以下をどれくらい許すのかを決める変数をfill_gapとする。

                ignored_times           : 無視した回数の合計を保持する変数。
                current_ignored_times   : 無視した連続回数を保持する変数。
                """

                while pos < len(scores):
                    if scores[pos] > config.threshold_val:
                        succeeded_times += 1
                        pos -= 1

                        ignored_times = 0  # 成功したため、連続でなくなる。
                    else:
                        if current_ignored_times < config.fill_gap:
                            # fill_gap の許容内なので次のポジションに移動する
                            pos -= 1

                            ignored_times += 1
                            current_ignored_times += 1
                        else:
                            succeeded_times = 0
                            pos += config.threshold_len

                            ignored_times = 0
                            current_ignored_times = 0

                    # 一回目は fill_gap により pos が Threshold_len を上回ることがあるため以下の記述が必要。
                    if pos < 0:
                        succeeded_times = 0
                        pos += 1 + config.threshold_len + ignored_times

                        ignored_times = 0
                        current_ignored_times = 0

                    # 成功が指定回数を超えたら書き込んで抜ける
                    if succeeded_times > config.threshold_len:
                        fw.write('{}\n'.format(json.dumps(json_dict)))
                        break

            except IndexError as e:
                # scoreが存在しないプロテインも存在するために記述
                print(e)



import json
import config

with open("disorder_add_protain.mjson", "r") as fr:
    for (i, line) in enumerate(fr):
        if i == 70009:
            json_dict = json.loads(line)
            break

    thru_total_count = 0
    count_score = 0  # 閾値以上のscoreが何個存在するかをカウントする変数
    count_fill_gap = 0  # 許容範囲内かをカウントする変数
    pos = config.threshold_len  # score[]のポジションを決める変数

    try:
        with open('make_sure.txt', 'w') as fw:
            scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
            fw.write("-----------------------------------------------------------------------------\n")

            fw.write(json_dict["protein names"] + "\n" +
                     str(scores) + "\n" +
                     "Threshold Value   : " + str(config.threshold_val) + "\n" +
                     "Threshold Lengs   : " + str(config.threshold_len) + "\n" +
                     "Fill Gap          : " + str(config.fill_gap) + "\n")

            fw.write("-----------------------------------------------------------------------------\n")

            # scoreが閾値を超えているか判定
            while pos < len(scores):
                if scores[pos] < config.threshold_val:  # False, Falseの回数が許容範囲かを判定する。
                    thru_total_count += 1
                    if count_fill_gap < config.fill_gap:
                        fw.write("1st Falure, 2nd Success" + "\n" +
                                 "Position      : " + str(pos) + "\n" +
                                 "Score         : " + str(scores[pos]) + "\n")
                        count_fill_gap += 1  # カウント
                        pos -= 1

                    else:
                        # 許容範囲を超えたため、カウントを0に戻しposを次の処理に移動する
                        fw.write("1st Falure, 2nd Falure" + "\n" +
                                 "Position      : " + str(pos) + "\n" +
                                 "Score         : " + str(scores[pos]) + "\n")
                        count_fill_gap = 0
                        thru_total_count = 0
                        count_score = 0
                        pos += config.threshold_len

                else:  # True
                    fw.write("1st Success" + "\n" +
                             "Position      : " + str(pos) + "\n" +
                             "Score         : " + str(scores[pos]) + "\n")

                    count_score += 1
                    count_fill_gap = 0
                    pos -= 1

                if pos < 0:
                    pos += 1 + config.threshold_len + thru_total_count
                    thru_total_count = 0
                    count_score = 0
                    count_fill_gap = 0

                fw.write("Success Count : " + str(count_score) + "\n" +
                         "Thru Count    : " + str(count_fill_gap) + "\n" +
                         "Thru Total Count    : " + str(thru_total_count) + "\n")

                fw.write("-----------------------------------------------------------------------------\n")

    except IndexError as e:
        # scoreが存在しないプロテインも存在するために記述
        print(e)
