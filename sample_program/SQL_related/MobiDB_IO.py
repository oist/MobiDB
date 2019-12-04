from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io

if __name__ == '__main__':
    service = UniProt()

    with open("result.txt", "w") as fw:
        with open("MobiDB_ID_small.txt") as fr:

            fr_line = fr.readlines()
            leng = len(fr_line)

        for line in fr_line:

            query = line
            columnlist = "id,entry name,length,mass,go(cellular component)"
            result = service.search(query, frmt="tab", columns = columnlist)

            df = pd.read_table(io.StringIO(result))




    print("finish")


