from logging import getLogger, StreamHandler, DEBUG
from kivy.uix.screenmanager import Screen
import matplotlib.pyplot as plt
import json
import webbrowser
from screen_out_plot import ScorePlot


"""デバック"""
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


