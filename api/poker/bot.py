from api.helpers import utils
from api.helpers.model import Model
from api.poker.bank import Bank
from api.poker.template_player import TemplatePlayer


class Bot(TemplatePlayer):
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
        self.did_action = True
        if self.is_next():
            return 0
        predict_array = []
        for b_index in range(0, 100):
            for c_index in range(0, 100):
                self.bet_limit = b_index
                self.call_limit = c_index
                self.predict_result = Model.dnn.predict([utils.get_array_from_mode(self)])[0][0]
                predict_array.append(self)
        max_predict = 0
        for p_a in predict_array:
            if p_a.predict_result > max_predict:
                self.bet_limit = p_a.bet_limit
                self.call_limit = p_a.call_limit
        self.result_percent = int(self.predict_result * 100)
        self.subtracted_result_percent = int(self.result_percent - self.call_limit)
        self.one_percent_score = self.points / 100
        if self.result_percent > self.bet_limit:
            bet = self.one_percent_score * self.subtracted_result_percent
            self.do_bet(bet=bet)
        elif self.call_limit < self.result_percent < self.bet_limit:
            if self.one_percent_score == 0 or self.subtracted_result_percent > int(Bank.bet / self.one_percent_score):
                self.do_call()
            else:
                self.do_fold()
        else:
            self.do_fold()
