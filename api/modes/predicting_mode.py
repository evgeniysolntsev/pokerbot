from api.helpers.model import Model
from api.helpers.utils import get_array_inputs_cards
from api.poker import core
from api.poker.core import Core


# todo
class PredictingMode(object):
    def __init__(self):
        test = []
        c_map0 = {
            'pf0': core.Card(14, 'd'),
            'pf1': core.Card(12, 's'),
            'f0': core.Card(4, 'd'),
            'f1': core.Card(7, 'c'),
            'f2': core.Card(5, 'd'),
            't': core.Card(10, 'd'),
            'r': core.Card(9, 'd')
        }

    @staticmethod
    def action():
        results = Model.dnn.predict([get_array_inputs_cards(Core.players[0])])
        for r in results:
            print("PREDICT={:5f}\n".format(r[0]))
