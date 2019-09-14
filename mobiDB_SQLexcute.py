# データベースへの接続とカーソルの生成
import MySQLdb
import logging
import time


class MySQL_Connection():
    """MySQL設定"""

    logging.debug('MySQL_Connection start')

    def __init__(self, **kwargs):
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

    logging.debug('MySQL_Connection end')

    def update_status(self):

        logging.debug('update_status start')

        self.f_Protain_name = True
        self.f_Length = False
        self.f_Mass = False

        logging.debug('update_status end')

    def field_excute(self):
        logging.debug('field_excute start')
        """
        if self.f_Protain_name :
            if self.f_Length:
                if self.f_mass:
                    
        
        else:"""

        # self.cur.execute("select * from mobidb_table where `Protein names` like 'integ%'")
        # self.cur.execute("""select `Entry name` from mobidb_table where mass >= 30""" )

        stmt = "select * from mobidb_table where `Protein names` like %s"
        self.cur.execute(stmt, ("integ" + "%",))


        self.con.commit()

        logging.debug('field_excute end')


    def result_print(self):
        logging.debug('result_print start')

        rows = self.cur.fetchall()
        for row in rows:
            print(row)

        logging.debug('result_print end')


if __name__ == '__main__':
    """main処理"""

    logging.debug('main start')
    t1 = time.time()

    # MySQLに接続する
    mysql = MySQL_Connection()

    mysql.update_status()   # 検索条件ステータスのアップデート
    mysql.field_excute()    # レコードの抽出
    mysql.result_print()    # 結果の出力

    mysql.con.close()       # MySQLを終了する

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("\n" + "経過時間：{%s}" % elapsed_time)
    logging.debug('main end')


"""
logging.debug('result_print start')
logging.debug('result_print end')
"""
