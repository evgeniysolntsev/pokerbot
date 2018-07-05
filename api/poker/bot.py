from api.helpers import utils
from api.helpers.model import Model
from api.poker.bank import Bank
from api.poker.template_player import TemplatePlayer


class Bot(TemplatePlayer):
    def __init__(self):
        super().__init__()
        self.id = utils.TEMP_BOT_NAMES.pop()
        self.best_predict_result = 0
        self.result_percent = 0
        self.subtracted_result_percent = 0
        self.bet_limit = 0
        self.best_bet_limit = 0
        self.call_limit = 0
        self.best_call_limit = 0
        self.one_percent_score = 0

    def do_action(self):
        self.did_action = True
        if self.is_next():
            return 0
        for c_index in range(0, 100):
            for b_index in range(0, 100):
                if b_index > c_index:
                    self.bet_limit = b_index
                    self.call_limit = c_index
                    predicting_result = Model.dnn.predict([utils.get_array_from_mode(self)])[0][0]
                    if predicting_result > self.best_predict_result:
                        self.best_bet_limit = b_index
                        self.best_call_limit = c_index
                        self.best_predict_result = predicting_result
        print("bet {} call {} predict {}"
              .format(self.best_bet_limit, self.best_call_limit, self.best_predict_result))
        self.result_percent = int(self.best_predict_result * 100)
        self.subtracted_result_percent = int(self.result_percent - self.best_call_limit)
        self.one_percent_score = self.points / 100
        print(self.result_percent)
        if self.result_percent > self.best_bet_limit:
            bet = self.one_percent_score * self.subtracted_result_percent
            self.do_bet(bet=bet)
        elif self.best_call_limit < self.result_percent < self.best_bet_limit:
            if self.one_percent_score == 0 or self.subtracted_result_percent > int(Bank.bet / self.one_percent_score):
                self.do_call()
            else:
                self.do_fold()
        else:
            self.do_fold()
