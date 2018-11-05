from termcolor import colored

from api.helpers.model import Model
from api.helpers.utils import *
from api.poker.card import Card


class PredictingMode(object):
    @staticmethod
    def action():
        pd = config.PREDICTING_DATA
        pd_len = pd.__len__()
        if pd and pd_len % 2 == 0:
            if config.NN_INPUTS_CARDS:
                Model.init_tf_model_with_input_cards(load=True)
            else:
                Model.init_tf_model_with_input_cards_and_bot_actions(load=True)

            pf0 = Card(pd[0], pd[1]).validate_string() if pd_len > 1 else None
            pf1 = Card(pd[2], pd[3]).validate_string() if pd_len > 3 else None
            f0 = Card(pd[4], pd[5]).validate_string() if pd_len > 5 else None
            f1 = Card(pd[6], pd[7]).validate_string() if pd_len > 7 else None
            f2 = Card(pd[8], pd[9]).validate_string() if pd_len > 9 else None
            t = Card(pd[10], pd[11]).validate_string() if pd_len > 11 else None
            r = Card(pd[12], pd[13]).validate_string() if pd_len > 13 else None

            if config.NN_INPUTS_CARDS:
                results = Model.dnn.predict([get_array_from_stages_for_cards(pf0, pf1, f0, f1, f2, t, r)])
            else:
                results = Model.dnn.predict(
                    [get_array_from_stages_for_cards_and_action_bot(pf0, pf1, f0, f1, f2, t, r)])
            for r in results:
                print(colored("\t\tModel predict = {:5f}\n".format(r[0]), "green"))
        else:
            print_error("Count cards need multiple two")
