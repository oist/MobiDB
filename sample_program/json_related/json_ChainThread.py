from bioservices import UniProt  # Uniprotのメソッドをインポート
import MySQLdb
import logging
import threading
import time
import itertools

from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from logging import getLogger, StreamHandler, DEBUG
import time
import json

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class InfoAddName:
    def __init__(self):
        logger.debug('IDN_init Begin')
        self.json_dict = []



            pass

        logger.debug('IDN_init End')

    def search_info(self):
        with open('disorder.mjson', 'r') as fr:
            #with open('disorder.mjson', 'r') as fr:
            for (i, line) in enumerate(fr):
        for _ in range(3):  # 最大3回実行
            try:
                print(line)
                self.json_dict = []
                self.json_dict = json.loads(line)
                result = service.search(self.json_dict["acc"], frmt='tab', columns=columnlist)
                result_s = result.splitlines()

                a_dict = {"protein names": result_s[-1]}

                self.json_dict.update(a_dict)
                self.loop += 1
                print("loop :", self.loop)

                time.sleep(0.1)

                logger.debug('write Begin')
                #with open('disorder_add_protain.mjson', 'a') as fw:
                    #fw.write('{}\n'.format(json.dumps(self.json_dict)))
            except Exception as e:
                pass  # 必要であれば失敗時の処理
            else:
                break


        logging.debug('worker End')


if __name__ == '__main__':
    # データをDBに格納する

    logging.debug('main Begin')

    t1 = time.time()

    service = UniProt()
    columnlist = 'protein names'
    #columnlist = 'keywords'

    idn = InfoAddName()
    idn.search_info()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logging.debug('main End')


