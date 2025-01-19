from termcolor import colored

import config
from api.helpers import utils
from api.players.template_player import TemplatePlayer


class TemplateBot(TemplatePlayer):
    def __init__(self):
        super().__init__()
        self.id = utils.TEMP_BOT_NAMES.pop()
        self.predict_result = 0
        self.result_percent = 0
        self.subtracted_result_percent = 0
        self.bet_limit = 0
        self.call_limit = 0
        self.one_percent_score = 0

    def do_action(self):
        if config.TEST_INFO and config.OUTPUT_IN_CONSOLE:
            print(colored("[{}] bet {} call {} predict [{}]"
                          .format(self.id, self.bet_limit, self.call_limit, self.predict_result), 'red'))
        self.result_percent = int(self.predict_result * 100)
        self.subtracted_result_percent = int(self.result_percent - self.call_limit)
        self.one_percent_score = self.points / 100
        self.get_current_action().predict = self.get_max_total_point()
        if self.result_percent >= self.bet_limit:
            bet = self.one_percent_score * self.subtracted_result_percent
            if self.result_percent == 1:
                self.get_current_action().action = 'allin'
                self.do_bet(bet=self.points)
            else:
                self.get_current_action().action = 'bet'
                self.do_bet(bet=bet)

        elif self.result_percent >= self.call_limit:
            self.do_call()
            self.get_current_action().action = 'call'
        else:
            if self.do_fold() == 0:
                self.get_current_action().action = 'check'
            else:
                self.get_current_action().action = 'fold'
