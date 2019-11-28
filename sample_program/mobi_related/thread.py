import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def worker1():
    # thread の名前を取得
    logging.debug('start')
    time.sleep(5)
    logging.debug('end')

if __name__ == '__main__':
    threads = []
    # スレッドを 5 個つくる
    for _ in range(5):
        t = threading.Thread(target=worker1)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()