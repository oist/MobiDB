from bioservices import UniProt  # Uniprotのメソッドをインポート
import MySQLdb
import logging
import threading
import time
import itertools

def worker(i):
    # thread の名前を取得

    logging.debug('worker start')

    start_num = i*lengs
    if (i < core):
        end_num = (i+1)*lengs
    else:
        end_num = i*lengs + remainder
    print(start_num)
    print(end_num)

    for query in itertools.islice(fr_line, start_num, end_num):
        try:
            result = service.search("id:" + query)
            result_s = result.strip("Entry	Entry name	Status	Protein names	Gene names	Organism	Length\n")
        except:
            None

        fw.write(result_s + "\n")

    logging.debug('worker end')


if __name__ == '__main__':
    # データをDBに格納する

    logging.debug('main start')

    t1 = time.time()
    threads = []
    service = UniProt()
    core = 9
    error = 0

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:
            fr_line = fr.readlines()
            lengs = int(len(fr_line)/core)
            remainder = int(len(fr_line) % core)

            # print(lengs)
            # print(remainder)

            for i in range(core+1):
                t = threading.Thread(target=worker, args=(i,))
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()

    print(error)
    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print(f"経過時間：{elapsed_time}")

    logging.debug('main end')















