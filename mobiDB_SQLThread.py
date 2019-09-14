from bioservices import UniProt  # Uniprotのメソッドをインポート
import MySQLdb
import logging
import threading
import time
import itertools

def connect_SQL():
    # MySQLに接続するメソッド

    logging.debug('connect_SQL start')

    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='sptotsfvi',
        db='mobi_db',
        # テーブル内部で日本語を扱うために追加
        charset='utf8'
    )

    logging.debug('connect_SQL end')
    return connection


def worker(i):
    # thread 取得

    logging.debug('worker start')

    start_num = i*lengs

    if (i < core):
        end_num = (i+1)*lengs
    else:
        end_num = i*lengs + remainder

    if(serial_num[i] == [0]):
        serial_num[i] = serial_num[i] + start_num
        print(serial_num[i])


    for query in itertools.islice(fr_line, start_num, end_num):
        try:
            result = service.search("id:" + query)
            result_s = result.strip("Entry	Entry name	Status	Protein names	Gene names	Organism	Length\n")
            re = result_s.split('\t')

            cursor.execute("""INSERT INTO mobiDB_SQL (id, Entry, Entry_name, Status, Protain_name, Gene_name, Organism, Length)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                           (serial_num[i], re[0], re[1], re[2], re[3], re[4], re[5], re[6]))
            # 保存を実行
            connect_SQL().commit()
        except:
            None

        fw.write(result_s + "\n")

    logging.debug('worker end')


if __name__ == '__main__':
    # データをDBに格納する

    logging.debug('main start')

    t1 = time.time()
    core = 9
    serial_num = [0]*(core+1)
    threads = []
    service = UniProt()



    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:
            fr_line = fr.readlines()
            lengs = int(len(fr_line)/core)
            remainder = int(len(fr_line) % core)

            # print(lengs)
            # print(remainder)

            cursor = connect_SQL().cursor()
            cursor.execute("DROP TABLE IF EXISTS mobiDB_SQL")
            cursor.execute("""CREATE TABLE mobiDB_SQL(
                            id INT(255) AUTO_INCREMENT NOT NULL, 
                            Entry VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Entry_name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Status VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Protain_name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Gene_name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Organism VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
                            Length INT(255) NOT NULL,
                            PRIMARY KEY (id)
                            )""")
            # 保存を実行
            connect_SQL().commit()

            for i in range(core+1):
                t = threading.Thread(target=worker, args=(i,))
                t.start()

                threads.append(t)
            for thread in threads:
                thread.join()

    cursor.execute("SELECT * FROM mobiDB_SQL")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # 接続を閉じる
    connect_SQL().close()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：{elapsed_time}")

    logging.debug('main end')















