import re

import config
from api.helpers import utils
from api.poker.template_player import TemplatePlayer


class Player(TemplatePlayer):
    def __init__(self):
        super().__init__()
        self.id = utils.TEMP_NAMES.pop()

    def do_action(self):
        self.did_action = True
        if self.is_next():
            return 0
        while True:
            type = input('{} type action: '.format(self.id))
            word = re.findall(r'\w*', type)[0]
            if word == 'fold':
                self.do_fold()
            elif word == 'call':
                self.do_call()
            elif word == 'check' and config.OUTPUT_IN_CONSOLE:
                print("{} check".format(self.id))
            elif word == 'bet':
                self.do_bet(bet=re.findall(r'\d{1,3}', type)[0])
            else:
                print('unknown command {}'.format(type))
                continue
            break
