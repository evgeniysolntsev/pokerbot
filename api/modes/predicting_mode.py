from api.helpers.model import Model
from api.helpers.utils import get_array_from_player
from api.poker import computer
from api.poker.computer import Computer


class PredictingMode(object):
    def __init__(self):
        test = []
        c_map0 = {
            'pf0': computer.Card(14, 'd'),
            'pf1': computer.Card(12, 's'),
            'f0': computer.Card(4, 'd'),
            'f1': computer.Card(7, 'c'),
            'f2': computer.Card(5, 'd'),
            't': computer.Card(10, 'd'),
            'r': computer.Card(9, 'd')
        }

        results = Model.dnn.predict([get_array_from_player(Computer.players[0])])
        for r in results:
            print("PREDICT={:5f}\n".format(r[0]))
