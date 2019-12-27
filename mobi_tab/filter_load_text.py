import config
from logging import getLogger, StreamHandler, DEBUG

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Load:
    """
    app.sm.current == "search" 時の処理

    Methods
    ----------

    substitute_text(self, str = num)
        textから取得したデータは必ずstr型である。
        str型　→　float型に変換するときは、""を取り除く必要がある。

    Raises
    ------
    ValueError
    入力された文字が数字以外のときに発生。

    Notes
    ----------
    Button イベントは theme.ScreenSearchに記載。
    config.threshold_val, config.threshold_len, config.fill_gapの使い方は
    screen_wait_search.pyに記載。

    """

    def load_text(self, th_val, th_len, fill_gap):
        logger.debug("filter_load_text.py, Load, load_text()")

        try:
            config.threshold_val = self.substitute_text(th_val)
            config.threshold_len = int(self.substitute_text(th_len))
            config.fill_gap = int(self.substitute_text(fill_gap))

        except ValueError as e:
            print(e)

    def substitute_text(self, ss_text):
        logger.debug("filter_load_text.py, Load, substitute_text()")

        if ss_text == "":
            return 0
        else:
            return float(ss_text.replace('"', ''))