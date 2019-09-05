from bioservices import UniProt  # Uniprotのメソッドをインポート
if __name__ == '__main__':
    service = UniProt()

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:

            fr_line = fr.readlines()
            leng = len(fr_line)

        for line in fr_line:

            query = line
            print(line)
            result = service.search("id:" + query)
            fw.write(result + "\n")


    print("finish")


