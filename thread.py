from bioservices import UniProt  # Uniprotのメソッドをインポート
import threading
import linecache
from time import sleep


def worker(leng, i):
    for s in (0, leng):
        query = linecache.getline(fr, int(s + leng * i))  # (現在の行) + (実行した行)
        result = service.search("id:" + query)
        fw.write(result + "\n")
        linecache.clearcache()
    return

if __name__ == '__main__':
    service = UniProt()

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:

            fr_line = fr.readlines()
            leng = int(len(fr_line))
            threads = []

        for i in range(10):

            t = threading.Thread(target=worker, args=(leng,i))
            threads.append(t)
            t.start()
            sleep(1)


        for thread in threads:
            thread.join()


    print("finish")



#         for offset, item in enumerate(fr_line):
#            query = item
#            t = threading.Thread(target=worker, args=(offset,))
#            threads.append(t)
#            t.start()

