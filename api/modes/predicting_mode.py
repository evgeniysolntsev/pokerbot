import config
from api.helpers.model import Model
from api.helpers.utils import get_array_from_stages_for_cards, get_array_from_stages_for_cards_and_action_bot
from api.poker.card import Card


class PredictingMode(object):
    @staticmethod
    def action():
        if config.NN_INPUTS_CARDS:
            Model.init_tf_model_with_input_cards(load=True)
        else:
            Model.init_tf_model_with_input_cards_and_bot_actions(load=True)

        pf0 = Card(14, 'd')
        pf1 = Card(12, 's')
        f0 = Card(4, 'c')
        f1 = Card(7, 'c')
        f2 = Card(5, 'd')
        t = Card(10, 'd')
        r = Card(9, 'd')

        if config.NN_INPUTS_CARDS:
            results = Model.dnn.predict([get_array_from_stages_for_cards(pf0, pf1, f0, f1, f2, t, r)])
        else:
            results = Model.dnn.predict([get_array_from_stages_for_cards_and_action_bot(pf0, pf1, f0, f1, f2, t, r)])
        for r in results:
            print("PREDICT={:5f}\n".format(r[0]))
