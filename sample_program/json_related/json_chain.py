from bioservices import UniProt  # Uniprotのメソッドをインポート
import pandas as pd
import io
from logging import getLogger, StreamHandler, DEBUG
import time
import json

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class InfoAddName:
    def __init__(self):
        logger.debug('IDN_init Begin')
        self.json_dict = []
        logger.debug('IDN_init End')

    def search_info(self):
        logger.debug('search_info Begin')
        # jsonファイル読み込み，条件比較を行う

        with open("disorder.mjson", 'r') as fr:
            for (i, line) in enumerate(fr):
                logger.debug('insert_protein_names Begin')

                try:

                    self.json_dict = []
                    self.json_dict = json.loads(line)
                    result = service.search(self.json_dict["acc"], frmt='tab', columns=columnlist)
                    result_s = result.splitlines()

                    a_dict = {'protein names': result_s[-1]}

                    self.json_dict.update(a_dict)
                except:
                    print("error")

                logger.debug('insert_protein_names End')

        with open('test.json', 'w') as fw:
            json.dump(self.json_dict, fw)

        logger.debug('search_info End')


if __name__ == '__main__':
    logger.debug('main Begin')

    service = UniProt()
    columnlist = 'protein names'

    idn = InfoAddName()
    idn.search_info()

    logger.debug('main End')