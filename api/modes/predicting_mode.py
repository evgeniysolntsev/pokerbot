from termcolor import colored

from api.helpers.utils import *
from api.poker.card import Card


class PredictingMode(object):

    @staticmethod
    def action():
        def validate_string(c):
            converted_map = {
                'A': 14,
                'K': 13,
                'Q': 12,
                'J': 11,
                'T': 10,
                '14': 14,
                '13': 13,
                '12': 12,
                '11': 11,
                '10': 10,
                '9': 9,
                '8': 8,
                '7': 7,
                '6': 6,
                '5': 5,
                '4': 4,
                '3': 3,
                '2': 2,
                's': 's',
                'h': 'h',
                'd': 'd',
                'c': 'c'
            }
            rank = converted_map.get(c.rank)
            suit = converted_map.get(c.suit)
            if rank and suit:
                c.rank = rank
                c.suit = suit
                return c
            else:
                print_error("Invalid card format")

        pd = config.PREDICTING_DATA
        pd_len = pd.__len__()
        if pd and pd_len % 2 == 0:
            # if config.NN_INPUTS_CARDS:
            #     Model.init_tf_model_with_input_cards(load=True)
            # else:
            #     Model.init_tf_model_with_input_cards_and_bot_actions(load=True)

            pf0 = validate_string(Card(pd[0], pd[1])) if pd_len > 1 else None
            pf1 = validate_string(Card(pd[2], pd[3])) if pd_len > 3 else None
            f0 = validate_string(Card(pd[4], pd[5])) if pd_len > 5 else None
            f1 = validate_string(Card(pd[6], pd[7])) if pd_len > 7 else None
            f2 = validate_string(Card(pd[8], pd[9])) if pd_len > 9 else None
            t = validate_string(Card(pd[10], pd[11])) if pd_len > 11 else None
            r = validate_string(Card(pd[12], pd[13])) if pd_len > 13 else None

            if config.NN_INPUTS_CARDS:
                results = Model.dnn.predict([get_array_from_stages_for_cards(pf0, pf1, f0, f1, f2, t, r)])
            else:
                results = Model.dnn.predict(
                    [get_array_from_stages_for_cards_and_action_bot(pf0, pf1, f0, f1, f2, t, r)])
            for r in results:
                print(colored("\t\tModel predict = {:5f}\n".format(r[0]), "green"))
        else:
            print_error("Count cards need multiple two")
