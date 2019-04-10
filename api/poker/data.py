import pandas as pd

from api.helpers.singleton import singleton


@singleton
class Data(object):
    df = {}

    def __init__(self):
        self.df = pd.read_csv("C:\\Users\\usr\\Documents\poker_comb.csv")

    def get_el(self):
        self.df
