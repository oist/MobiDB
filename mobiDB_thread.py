import logging
import threading
import time
import MySQLdb
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import Error
from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from sqlalchemy import create_engine
import itertools
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from IPython.display import display


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

dbconfig = {
    "host":"localhost",
    "user":"root",
    "passwd":"",
    "db":"mobidb",
    # テーブル内部で日本語を扱うために追加
    "charset":"utf8",
}
def worker1(i, connection, columnlist):
    # thread の名前を取得
    logging.debug('start')
    # print(type(i))
    connection = mysql.connector.connect(**dbconfig)
    connection.autocommit = True



    start_num = i * lengs
    if (i < core):
        end_num = (i + 1) * lengs
    else:
        end_num = i * lengs + remainder

    print(start_num)
    print(end_num)

    for query in itertools.islice(fr_line, start_num, end_num):
        result = service.search(query, frmt="tab", columns=columnlist)

        df = pd.read_table(io.StringIO(result))
        df = df.fillna("")
        #
        #
        #
        #
        #
        # print(df[['Gene names']].head())



        engine = create_engine('mysql://%s:%s@%s:%s/%s' % ('root', '', 'localhost', '3306', 'mobidb'))


        with engine.begin() as con:
            df.to_sql('mobiDB_table', con=con, if_exists='append', index=False)

    connection.close()


    logging.debug('end')
    return

if __name__ == '__main__':
    t1 = time.time()
    threads = []
    service = UniProt()
    core = 9

    columnlist = "id, entry name, genes, protein names, length, mass, sequence, keywords"

    connection = mysql.connector.connect(**dbconfig)
    connection.autocommit = True



    cursor = connection.cursor()


    cursor.execute("set global max_connections = 100000")
    cursor.execute("DROP TABLE IF EXISTS mobiDB_table")
    cursor.execute("""CREATE TABLE mobiDB_table(
            id INT(255) AUTO_INCREMENT NOT NULL, 
            Entry VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
            `Entry name` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
            `Gene names` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
            `Protein names` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
            length  INT(255) NOT NULL,
            mass VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
            sequence VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
            keywords VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
            PRIMARY KEY (id)
            )""")
    connection.close()


    #  with open("mobiDB_all.txt", "w") as fw:
    with open("MobiDB_ID.txt") as fr:
        fr_line = fr.readlines()
        lengs = int(len(fr_line) / core)        # 1Threadあたりの仕事量
        remainder = int(len(fr_line) % core)    # 余った仕事

        print(lengs)
        print(remainder)

        for i in range(core + 1):
            t = threading.Thread(target=worker1, args=(i, connection, columnlist))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

    t2 = time.time()
    # 測定終了
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print(f"経過時間：{elapsed_time}")



    print("finish")