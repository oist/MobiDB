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
    def search_info(self):
        ar = []
        with open('mobiDB_human.json', 'a') as fw:
            with open('mobiDB_human.mjson', 'r') as fr:
                for (i, line) in enumerate(fr):
                    try:
                        json_dict = json.loads(line)
                        # json_dict['protein_names'] = json_dict.pop("protein names")

                        fw.write('{}\n'.format(json.dumps(json_dict)))

                            # columnlist = 'keywords'
                            # result = service.search(json_dict["acc"], frmt='tab', columns=columnlist)
                            # result_s = result.splitlines()
                            # print(result_s)

                    except Exception as e:
                        print(e)
                        ar.append(i)

                print(ar)

        logger.debug('worker End')


if __name__ == '__main__':
    # データをDBに格納する
    with open('mobiDB_human.json', 'w'):
        pass

    logger.debug('main Begin')

    t1 = time.time()

    idn = InfoAddName()
    idn.search_info()

    t2 = time.time()
    elapsed_time = t2 - t1  # 処理にかかった時間を計算する
    print("経過時間：", elapsed_time)


