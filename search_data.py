from logging import getLogger, StreamHandler, DEBUG
import json
import config
import threading
from kivymd.app import MDApp
"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class SearchData(threading.Thread):
    """
    Parameters
    ----------
    fw : file = success_data.mjson
        config.threshold_val, config.threshold_len, config.fill_gapの全条件を満たすプロテインを記録するファイル
    fr : file = mobiDB_human.mjson
        原点となるjsonファイル。humanに含まれるプロテインの情報が記載されている。
    succeeded_times : int
        score[i] > config.threshold_val の連続回数を保持する。
    ignored_times : int
        score[i] < config.threshold_val を許容した回数を保持する。
    current_pos : int = config.threshold_len
        現在のスコアの位置を保持する。


    Methods
    ----------
    kill(self)
        スレッドを終了させる。
    compare_score(self)
        条件に応じて、値を代入する。
    run(self)
        scoreを比較し、条件に一致したものをsuccessed_data.mjsonに追加する


    Examples
    ----------
    検索アルゴリズムはBM法を参考にした。
    config.threshold_val　→　th_val
    config.threshold_len　→　th_len
    config.fill_gap       →　fill_gap

    1. score[current_pos]と th_valを末尾から比較(True-> successed_times++)。
    2. successed_timesが th_lenを上回れば記入。
    3. 検索に失敗した場合、その地点にth_lenとfill_gapを足して、再度末尾から検索する。

    以下の条件で検索を行うと、
    -------------------------------------
             0  1  2  3  4  5  6
    score = [1, 0, 0, 1, 0, 1, 1]
    config.threshold_val    = 0.5
    config.threshold_len    = 4
    config.fill_gap         = 1
    -------------------------------------

    current_pos = th_len
        score[3] True
        score[2] False, ignore_times 1
        score[1] False, ignore_times 2

    current_pos = current_pos + th_len + ignore_times
        core[6] True
        score[5] True
        score[4] Flase, ignore_times 1
        score[3] True

        と検索は成功し、jsonファイルに記入される。


    Examples
    ----------
    How to use config.threshold_val, config.threshold_len and config.fill_gap.
    scoreの範囲は 0 < x < 1である。
    以下のようなscoreをもったプロテインがあるとする。
        score = [1, 0, 0.8, 0,8, 0,8]

    また、閾値は以下の通りとする。
        config.threshold_val    = 0.5
        config.threshold_len    = 5
        config.fill_gap         = 0 or 1

    以下のプログラムを実行する。
        for i in len(score):
            if score[i] > threshold_val:
                i += 1
            elif score[i] < threshold_val
                i = 0

        if i >= config.threshold_len:
            print("successed")
        elif i < config.threshold_len:
            print("fail")

    出力は,
        fill_gap = 0 -> i == 3  fail
        fill_gap = 1 -> i == 5  successed


    Raises
    ------
    IndexError
    プロテインにスコアが存在しない場合に発生。


    Notes
    ----------
    config.threshold_val, config.threshold_len, config.fill_gapの詳細はconfig.pyに記載。

    """

    def __init__(self):
        logger.debug("search_data.py, SearchData, __init__()")
        super().__init__()
        self.alive = True

    def run(self):
        logger.debug("search_data.py, SearchData, run()")
        with open('success_data.json', 'w') as fw:
            with open("mobiDB_human.json", "r") as fr:
                for (i, line) in enumerate(fr):
                    json_dict = json.loads(line)
                    succeeded_times = 0
                    ignored_times = 0
                    current_pos = config.threshold_len

                    try:
                        # scoreを取得
                        print(config.threshold_len)

                        scores = json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
                        scores_len = len(scores)

                        while self.alive | current_pos < scores_len:
                            # scoreを比較
                            if scores[current_pos] > config.threshold_val:
                                succeeded_times += 1
                                current_pos -= 1
                                ignored_times = 0
                            else:
                                # fill_gapの処理を入れる
                                if config.fill_gap > ignored_times:
                                    succeeded_times += 1
                                    current_pos -= 1
                                    ignored_times += 1
                                else:
                                    succeeded_times = 0
                                    current_pos += config.threshold_len + ignored_times
                                    ignored_times = 0

                            # 成功したscoreデータの書き込み
                            if succeeded_times >= config.threshold_len:
                                fw.write('{}\n'.format(json.dumps(json_dict)))
                                break
                    except IndexError:
                        pass
                    if not self.alive:
                        break
                else:
                    app = MDApp.get_running_app()
                    app.show_toast()

        print("finish2")

    def kill(self):
        logger.debug("search_data.py, SearchData, kill()")
        self.alive = False
