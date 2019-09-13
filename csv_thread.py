import logging
import threading
import time
import itertools
import csv
import re

def worker(i):

    # thread の名前を取得
    logging.debug('start')
    # print(type(i))
    start_num=i*lengs
    if (i < core):
        end_num=(i+1)*lengs
    else:
        end_num = i*lengs + remainder

    print(start_num)
    print(end_num)


    o = csv.writer(fw, delimiter='\t')

    for row in itertools.islice(fr_line, start_num, end_num):
        o.writerow(row.split())

    logging.debug('end')
    return

if __name__ == '__main__':
    t1 = time.time()
    threads = []
    rows1 = []
    core = 9

    with open("mobiDB_small.csv", "w") as fw:
        with open("result.txt") as fr:
            fr_line = fr.readlines()
            lengs = int(len(fr_line)/core)
            remainder = int(len(fr_line) % core)


            for i in range(core+1):
                t = threading.Thread(target=worker, args=(i,))
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()


    print("finish")
    t2 = time.time()
    # 測定終了
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print(f"経過時間：{elapsed_time}")
















