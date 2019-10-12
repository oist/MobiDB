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
        self.len = 0
        self.remainder = 0
        self.loop = 0

        with open('disorder2.mjson', 'w') as fw:
            pass

        logger.debug('IDN_init End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う

        with open("disorder.mjson", 'r') as fr:
            self.fr_line = fr.readlines()
            self.len = int(len(self.fr_line) / core)
            self.remainder = int(len(self.fr_line) % core)

            for i in range(core+1):
                t = threading.Thread(target=self.worker, args=(i,))
                t.start()

                threads.append(t)
            for thread in threads:
                thread.join()

            logger.debug('insert_protein_names End')

        logger.debug('search_info End')

    def worker(self, i):
        # thread 取得

        logging.debug('worker Begin')

        start_num = i * self.len

        if i < core:
            end_num = (i + 1) * self.len
        else:
            end_num = i * self.len + self.remainder

        if serial_num[i] == [0]:
            serial_num[i] = serial_num[i] + start_num
        print("i:", i)
        print("lengs:", self.len)
        print("start_num:", start_num)
        print("end_num:", end_num)

        for (k, line) in enumerate(itertools.islice(self.fr_line, start_num, end_num)):
            for _ in range(5):  # 最大3回実行
                try:
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
                    with open('disorder_add_protain.mjson', 'a') as fw:
                        fw.write('{}\n'.format(json.dumps(self.json_dict)))
                except Exception as e:
                    pass  # 必要であれば失敗時の処理
                else:
                    break
            else:
                print("write false:", k)

        logging.debug('worker End')


if __name__ == '__main__':
    # データをDBに格納する

    logging.debug('main Begin')

    t1 = time.time()
    core = 10
    serial_num = [0]*(core+1)
    threads = []
    service = UniProt()
    columnlist = 'protein names'
    # columnlist = 'keywords'

    idn = InfoAddName()
    idn.search_info()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)

    logging.debug('main End')


