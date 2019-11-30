import config
from logging import getLogger, StreamHandler, DEBUG


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def init():
    logger.debug("init.py, init()")
    config.keyword = ''
    config.threshold_val = 0.0
    config.threshold_len = 0
    config.fill_gap = 0

