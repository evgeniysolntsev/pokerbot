import config
from api.helpers import utils
from api.players.template_player import TemplatePlayer
from api.poker.bank import Bank


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
            print("{} bet {} call {} predict {}"
                  .format(self.id, self.bet_limit, self.call_limit, self.predict_result))
        self.result_percent = int(self.predict_result * 100)
        self.subtracted_result_percent = int(self.result_percent - self.call_limit)
        self.one_percent_score = self.points / 100
        if self.result_percent >= self.bet_limit:
            bet = self.one_percent_score * self.subtracted_result_percent
            self.do_bet(bet=bet)
        elif self.result_percent >= self.call_limit:
            if self.one_percent_score == 0 or self.subtracted_result_percent > int(Bank.bet / self.one_percent_score) \
                    or config.PLAYING_MODE:
                self.do_call()
            else:
                self.do_fold()
        else:
            from api.poker.core import Core
            max_score = max([p.get_cur_points_in_bank() if p.get_cur_points_in_bank() else 0 for p in Core.players])
            if max_score <= 1.0:
                self.do_call()
            else:
                self.do_fold()
