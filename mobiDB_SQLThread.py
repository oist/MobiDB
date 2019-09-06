from bioservices import UniProt  # Uniprotのメソッドをインポート
import logging
import threading
import time
import itertools
import MySQLdb

def worker(i, lengs):
    # Thread処理を行う

    logging.debug('start')
    start_num=i*lengs           # Thread処理の開始地点を計算する
    if (i < core):              #
        end_num=(i+1)*lengs-1
    else:
        end_num = i*lengs + remainder

    # print(start_num)
    # print(end_num)



    for query in itertools.islice(fr_line, start_num, end_num):
        result = service.search("id:" + query)
        fw.write(result + "\n")

    time.sleep(1)
    logging.debug('end')
    return

if __name__ == '__main__':
    t1 = time.time()
    threads = []
    service = UniProt()                             # Uniprotに接続
    core = 5                                        # Tgread数

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:
            fr_line = fr.readlines()
            lengs = int(len(fr_line)/core)          # Threadが担当する行数を指定
            remainder = int(len(fr_line) % core)    # ほとんどの場合あまりがでるため、あまり分を+1したThreadに処理させる。
            serial_num = []                         # 連番用の配列

            # print(lengs)
            # print(remainder)

            # 指定されたThreadを用意し、threadの番号を'worker'メソッドに渡す
            for i in range(core+1):
                t = threading.Thread(target=worker, args=(i, lengs,))
                t.start()
                threads.append(t)

            # Threadがすべて終了するまで待機
            for thread in threads:
                thread.join()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print(f"経過時間：{elapsed_time}")
