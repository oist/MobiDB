# データベースへの接続とカーソルの生成
import MySQLdb
import logging
import time
from MySQLdb.cursors import DictCursor


class MySQL_Connection():
    """MySQL設定"""

    def __init__(self, **kwargs):
        logging.debug('init_MySQL_Connection start')
        # MySQLに接続する

        self.con = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='',
            db='mobi_db',
            charset='utf8',
            local_infile=True
        )
        self.cur = self.con.cursor()
        # 条件文のプログラム

        # [ Protain_name, Length, Mass ]
        self.f_list = ['integrin', 10, 10]

        logging.debug('init_MySQL_Connection end')


    def field_excute(self):
        logging.debug('field_excute start')


        # 探索用の配列を用意する
        self.con.commit()

        logging.debug('field_excute end')


    def result_print(self):
        logging.debug('result_print start')

        self.cur.execute("""select j_load from json_load""")
        rows = self.cur.fetchall()
        print(rows[79])


        logging.debug('result_print end')


if __name__ == '__main__':
    """main処理"""

    logging.debug('main start')
    t1 = time.time()

    # MySQLに接続する
    mysql = MySQL_Connection()

    mysql.field_excute()    # 処理の実行
    mysql.result_print()    # 結果の出力

    mysql.con.close()       # MySQLを終了する

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("\n" + "経過時間：{%s}" % elapsed_time)
    logging.debug('main end')


"""
logging.debug('result_print start')
logging.debug('result_print end')

    def update_status(self):

        logging.debug('update_status start')

        self.f_Protain_name = True
        self.f_Length = False
        self.f_Mass = False

        logging.debug('update_status end')
"""

# self.cur.execute("""select * from json_load where JSON_CONTAINS(j_load, '[ 1, 42, "D" ], [ 100, 110, "D" ], [ 150, 157, "D" ], [ 327, 333, "D" ]', '$.mobidb_consensus.disorder.predictors.regions')""")
# self.cur.execute("""select * from json_load where JSON_CONTAINS(j_load, '"Q8IU80"', '$.acc')""")
# select * from json_load where JSON_CONTAINS(j_load, '0', '$.mobidb_consensus.disorder.predictors[1].scores[1]')

# scoresのネスト　$.mobidb_consensus.disorder.predictors[1].scores[1]

# self.cur.execute("select * from mobidb_table where `Protein names` like 'integ%'")
# self.cur.execute("""select `Entry name` from mobidb_table where mass >= 30""" )
# stmt = "select * from mobidb_table where `Protein names` like %s"
# self.cur.execute(stmt, ("integ" + "%",))
# core = object.getInt("scores")

