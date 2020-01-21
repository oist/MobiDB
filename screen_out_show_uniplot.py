from logging import getLogger, StreamHandler, DEBUG
import json
import webbrowser

"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class ShowUniplot:
    """
    指定されたidのスコアをプロットする

    Parameters
    ----------
    """
    def __init__(self, value):
        logger.debug("screen_out_access_uniplot.py, ShowUniplot, __init__()")
        self.protein_id = value

    def run(self):
        logger.debug("screen_out_access_uniplot.py, ShowUniplot, __init__()")
        with open('success_data.json', 'r') as fr:
            for (k, line) in enumerate(fr):
                if k == self.protein_id:
                    json_dict = json.loads(line)
                    break

        url = 'https://www.uniprot.org/uniprot/' + json_dict["acc"]
        webbrowser.open_new_tab(url)
