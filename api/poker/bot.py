import config
from api.helpers import utils
from api.helpers.model import Model
from api.poker.template_bot import TemplateBot


class Bot(TemplateBot):
    def __init__(self):
        super().__init__()

    def do_action(self):
        if super().is_skip():
            return 0
        if self.hand[0].rank < 10 or self.hand[1].rank < 10:
            self.predict_result = 0
            if config.TEST_INFO and config.OUTPUT_IN_CONSOLE:
                print('rank < 10')
        else:
            for i in range(50, 100):
                for j in range(i, 100):
                    predicting_result = Model.dnn.predict(
                        [utils.get_array_from_mode(bot=self, call_limit=i, bet_limit=j)])[0][0]
                    if predicting_result > self.predict_result:
                        self.bet_limit = j
                        self.call_limit = i
                        self.predict_result = predicting_result
        super().do_action()
