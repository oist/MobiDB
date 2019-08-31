from bioservices import UniProt  # Uniprotのメソッドをインポート
if __name__ == '__main__':
    service = UniProt()

    with open("MobiDB_ID.txt") as fr:
        for s_line in fr:
            s_line = fr.readline()
            query = s_line
            result = service.search(query)

            with open("result.txt", mode='w') as fw:
                fw.write(result + "\n")

    print("finish")

