# データベースへの接続とカーソルの生成
import MySQLdb
from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from sqlalchemy import create_engine
import sqlalchemy as sqa

if __name__ == '__main__':
    service = UniProt()
    c_host = 'localhost'
    c_user = 'root'
    c_passwd = ''
    c_db = 'mobidb'
    c_port = "3306"
    columnlist = "id, entry name, genes, protein names, length, mass, annotation score, sequence, keywords"


    connection = MySQLdb.connect(
        host=c_host,
        user=c_user,
        passwd=c_passwd,
        db=c_db,
        # テーブル内部で日本語を扱うために追加
        charset='utf8',
        local_infile=True
    )
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS mobiDB_table")
    cursor.execute("""CREATE TABLE mobiDB_table(
        id INT(255) AUTO_INCREMENT NOT NULL, 
        Entry VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
        `Entry name` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
        `Gene names` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
        `Protein names` VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
        length  INT(255) NOT NULL,
        mass VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci, 
        Annotation INT(255) NOT NULL,
        sequence VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
        keywords VARCHAR(255) NOT NULL COLLATE utf8mb4_unicode_ci,
        PRIMARY KEY (id)
        )""")
    connection.commit()




    with open("MobiDB_ID_small.txt") as fr:

        fr_line = fr.readlines()
        leng = len(fr_line)

    for line in fr_line:

        query = line

        result = service.search(query, frmt="tab", columns = columnlist)

        df = pd.read_table(io.StringIO(result))
        pd.set_option('display.max_rows', None)
        print(df)

        engine = create_engine('mysql://%s:%s@%s:%s/%s' % (c_user, c_passwd, c_host, c_port, c_db))

        with engine.begin() as con:
            df.to_sql('mobiDB_table', con=con, if_exists='append', index=False)
        connection.commit()

    cursor.execute("SELECT * FROM mobiDB_table")
    # 接続を閉じる
    connection.close()



    print("finish")


