import MySQLdb



connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='sptotsfvi',
    db='mobi_db',
    # テーブル内部で日本語を扱うために追加
    charset='utf8',
    local_infile=True
)
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS mobiDB_table")
cursor.execute("""CREATE TABLE mobiDB_table(
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

cursor.execute("""load data local infile 'mobiDB_all.csv' INTO table mobiDB_table FIELDS terminated by ',' enclosed by '"' escaped by '"'""")

connection.commit()
cursor.execute("SELECT * FROM mobiDB_table")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 接続を閉じる
connection.close()

print("finish")

# データベースへの接続とカーソルの生成
