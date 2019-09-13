# データベースへの接続とカーソルの生成
import MySQLdb
from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from sqlalchemy import create_engine


if __name__ == '__main__':
    service = UniProt()
    c_host = 'localhost'
    c_user = 'root'
    c_db = 'mobidb'
    c_port = "3306"

    connection = MySQLdb.connect(
        host=c_host,
        user=c_user,
        passwd='',
        db=c_db,
        # テーブル内部で日本語を扱うために追加
        charset='utf8',
        local_infile=True
    )
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS mobiDB_table")
    cursor.execute("""CREATE TABLE mobiDB_table(
        id INT(255) AUTO_INCREMENT NOT NULL, 
        Entry_name VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
        length  INT(255) NOT NULL,
        mass VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
        go_cellular_component VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
        PRIMARY KEY (id)
        )""")
    connection.commit()


    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:

            fr_line = fr.readlines()
            leng = len(fr_line)

        for line in fr_line:

            query = line
            columnlist = "id, entry name,length,mass,go(cellular component)"
            result = service.search(query, frmt="tab", columns = columnlist)

            df = pd.read_table(io.StringIO(result))

            engine = create_engine('mysql://%s:%s@%s:%s/%s' % (c_user, "", c_host, c_port, schema))
            with engine.begin() as con:
                df.to_sql('mobiDB_table', con=connection, if_exists='append', index=False)
            connection.commit()

    cursor.execute("SELECT * FROM mobiDB_table")
    # 接続を閉じる
    connection.close()



    print("finish")


