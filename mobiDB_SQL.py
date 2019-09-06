import MySQLdb
from bioservices import UniProt  # Uniprotのメソッドをインポート
if __name__ == '__main__':
    service = UniProt()

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:

            fr_line = fr.readlines()
            leng = len(fr_line)


        for line in fr_line:

            query = line

            result = service.search("id:" + query)
            result_s = result.strip("Entry	Entry name	Status	Protein names	Gene names	Organism	Length\n")

            re = result_s.split('\t')
            connection = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='sptotsfvi',
                db='mobi_db',
                # テーブル内部で日本語を扱うために追加
                charset='utf8'
            )
            cursor = connection.cursor()
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

            cursor.execute("""INSERT INTO mobiDB_SQL (id, Entry, Entry_name, Status, Protain_name, Gene_name, Organism, Length)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                           (re[0], re[1], re[2], re[3], re[4], re[5], re[6]))

            # ここに実行したいコードを入力します
            cursor.execute("SELECT * FROM mobiDB_SQL")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            # 保存を実行
            connection.commit()

            # 接続を閉じる
            connection.close()
            fw.write(result )


    print("finish")

# データベースへの接続とカーソルの生成
