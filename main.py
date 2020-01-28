from kivy.core.window import Window
from kivy.lang import Builder
from application import MobiApp
from logging import getLogger, StreamHandler, DEBUG


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


if __name__ == "__main__":
    logger.debug("main.py, mai"
                 "n")

    # kvファイルをstring型としてload
    with open("./theme.kv", "r", encoding="utf8") as f:
        Builder.load_string(f.read())

    Window.size = (728, 450)
    MobiApp().run()