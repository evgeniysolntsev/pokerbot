from api.dnn import config
from api.dnn.model import Model
from api.helpers import config_util
from api.helpers.utils import get_array_from_player
from api.poker.bank import Bank
from api.poker.template_player import TemplatePlayer


class Bot(TemplatePlayer):
    def __init__(self):
        super().__init__()
        name = config.BOT_NAMES.pop()
        if len(name) < config_util.MAX_LENGTH_NAME:
            while len(name) != config_util.MAX_LENGTH_NAME:
                name = name + " "
        self.id = name
        self.predict_result = 0
        self.result_percent = 0
        self.subtracted_result_percent = 0
        self.bet_limit = 0.75
        self.call_limit = 0.5
        self.one_percent_score = 0
        self.subtraction_percent = int(self.call_limit * 100)

    def do_action(self):
        self.did_action = True
        if self.is_next():
            return 0
        self.predict_result = Model.dnn.predict([get_array_from_player(self)])[0][0]
        self.result_percent = int(self.predict_result * 100)
        self.subtracted_result_percent = self.result_percent - self.subtraction_percent
        self.one_percent_score = self.points / 100
        if self.predict_result > self.bet_limit:
            bet = self.one_percent_score * self.subtracted_result_percent
            self.do_bet(bet=bet)
        elif self.call_limit < self.predict_result < self.bet_limit:
            if self.one_percent_score == 0:
                self.do_fold()
            elif self.subtracted_result_percent > int(Bank.bet / self.one_percent_score):
                self.do_call()
            else:
                self.do_fold()
        else:
            self.do_fold()
