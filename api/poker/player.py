import re

from api.dnn import config
from api.poker.template_player import TemplatePlayer


class Player(TemplatePlayer):
    def __init__(self):
        super().__init__()
        name = config.NAMES.pop()
        if len(name) < config.MAX_LENGTH_NAME:
            while len(name) != config.MAX_LENGTH_NAME:
                name = name + " "
        self.id = name

    def do_action(self):
        self.did_action = True
        if self.is_next():
            return 0
        while True:
            state = input('{} type action: '.format(self.id))
            word = re.findall(r'\w*', state)[0]
            if word == 'fold':
                self.do_fold()
            elif word == 'call':
                self.do_call()
            elif word == 'check' and config.OUTPUT_IN_CONSOLE:
                print("{} check".format(self.id))
            elif word == 'bet':
                self.do_bet(bet=float(re.findall(r'\d{1,3}', state)[0]))
            else:
                print('failed...')
                continue
            break
