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
    def search_info(self):
        ar = []
        with open('disorder_add_protain.mjson', 'a') as fw:
            with open('disorder.mjson', 'r') as fr:
                # with open('disorder.mjson', 'r') as fr:
                for (i, line) in enumerate(fr):
                    print(i)
                    try:
                        json_dict = json.loads(line)
                        result = service.search(json_dict["acc"], frmt='tab', columns=columnlist)
                        result_s = result.splitlines()

                        a_dict = {"protein names": result_s[1]}
                        json_dict.update(a_dict)

                        fw.write('{}\n'.format(json.dumps(json_dict)))

                            # columnlist = 'keywords'
                            # result = service.search(json_dict["acc"], frmt='tab', columns=columnlist)
                            # result_s = result.splitlines()
                            # print(result_s)

                    except Exception as e:
                        print(e)
                        ar.append(i)

                print(ar)

        logging.debug('worker End')


if __name__ == '__main__':
    # データをDBに格納する
    with open('disorder_add_protain.mjson', 'w'):
        pass

    logging.debug('main Begin')

    t1 = time.time()

    service = UniProt()
    columnlist = 'protein names'
    # columnlist = 'keywords'

    idn = InfoAddName()
    idn.search_info()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logging.debug('main End')


