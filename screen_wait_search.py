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


class SearchScore(threading.Thread):
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
        super().__init__()
        self.alive = True

        self.json_dict = dict()
        self.succeeded_times = 0
        self.ignored_times = 0
        self.current_pos = config.threshold_len

    def run(self):
        logger.debug("screen_wait_search, SearchScore, search_score()")

        with open('success_data.mjson', 'w') as fw:
            with open("mobiDB_human.mjson", "r") as fr:

                for (i, line) in enumerate(fr):
                    print(i)
                    self.json_dict = json.loads(line)

                    try:
                        # scoreを取得

                        scores = self.json_dict["mobidb_consensus"]["disorder"]["predictors"][1]["scores"]
                        scores_len = len(scores)

                        while self.alive:

                            if self.current_pos < scores_len:
                                break

                            # scoreを比較
                            self.compare_score(scores)

                            # 成功したscoreデータの書き込み
                            if self.succeeded_times >= self.current_pos:
                                fw.write('{}\n'.format(json.dumps(self.json_dict)))
                                break
                    except IndexError:
                        pass
                    #
                    if not self.alive:
                        break

                else:
                    self.change_screen("out")

    def change_screen(self, name):
        logger.debug("screen_wait_main.py, ScreenWait, change_screen()")

        app = App.get_running_app()
        app.sm.current = name

    def kill(self):
        logger.debug("screen_wait_main.py, ScreenWait, kill()")
        self.alive = False

    def compare_score(self, scores):
        logger.debug("screen_wait_main.py, ScreenWait, compare_score()")
        # scoreが閾値を超えているか判定
        if scores[self.current_pos] > config.threshold_val:
            self.succeeded_times += 1
            self.current_pos -= 1
            self.ignored_times = 0
        else:
            # fill_gapの処理を入れる
            if config.fill_gap > self.ignored_times:
                self.succeeded_times += 1
                self.current_pos -= 1
                self.ignored_times += 1
            else:
                self.succeeded_times = 0
                self.current_pos += self.current_pos + self.ignored_times
                self.ignored_times = 0
