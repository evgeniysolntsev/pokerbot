import re

from termcolor import colored

import config
from api.helpers import utils
from api.players.template_player import TemplatePlayer


class Player(TemplatePlayer):
    def __init__(self):
        super().__init__()
        self.id = utils.TEMP_NAMES.pop()

    def do_action(self):
        self.did_action = True
        if self.is_next():
            return 0
        while True:
            type = input(colored('{} type action: '.format(self.id), 'green'))
            word = re.findall(r'\w*', type)[0]
            if word == 'fold':
                self.do_fold()
            elif word == 'call':
                self.do_call()
            elif word == 'check' and config.OUTPUT_IN_CONSOLE:
                from api.poker.core import Core
                my_score = self.get_cur_points_in_bank()
                max_score = max([p.get_cur_points_in_bank() if p.get_cur_points_in_bank() else 0 for p in Core.players])
                if my_score >= max_score:
                    print("{} check".format(self.id))
                else:
                    print(colored("{} you need call or bet".format(self.id), 'red'))
                    continue
            elif word == 'bet':
                findall = re.findall(r'\d{1,3}', type)
                if findall:
                    findall = findall[0]
                else:
                    print('unknown command {}'.format(type))
                    continue
                self.do_bet(bet=findall)
            else:
                print('unknown command {}'.format(type))
                continue
            break
