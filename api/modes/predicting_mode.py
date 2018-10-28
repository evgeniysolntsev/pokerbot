from api.helpers.model import Model
from api.helpers.utils import get_array_inputs_cards
from api.poker.card import Card


class PredictingMode(object):
    @staticmethod
    def action():
        c_map0 = {
            'pf0': Card(14, 'd'),
            'pf1': Card(12, 's'),
            'f0': Card(4, 'd'),
            'f1': Card(7, 'c'),
            'f2': Card(5, 'd'),
            't': Card(10, 'd'),
            'r': Card(9, 'd')
        }
        results = Model.dnn.predict([get_array_inputs_cards(c_map0)])
        for r in results:
            print("PREDICT={:5f}\n".format(r[0]))
