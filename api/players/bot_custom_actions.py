from api.players.template_bot import TemplateBot


class BotCustomActions(TemplateBot):
    def __init__(self):
        super().__init__()
        self.bet_limit = 80
        self.call_limit = 30

    def do_action(self):
        if super().is_skip():
            return 0
        # self.predict_result = Model.dnn.predict(np.array([utils.get_array_inputs_cards(self)]))[0][1]
        self.set_predict()
        super().do_action()

    def set_predict(self):
        self.predict_result = 0
        if self.get_current_state() == 'PreFlop':
            self.set_predict_pre_flop()
        else:
            self.set_predict_flop()

    def set_predict_flop(self):
        all_comb = self.compute_points_by_other()
        self.compute_points_by_self()
        max_total = self.get_max_total_point()
        if all_comb.count(max_total) > 0:
            max_index = all_comb.index(max_total)
            if max_index == 1:
                self.predict_result = 0.5
            elif max_index == 2:
                self.predict_result = 0.4
            else:
                self.predict_result = 0
        elif max_total > max(all_comb):
            self.predict_result = 1
        else:
            self.predict_result = 0

    def set_predict_pre_flop(self):
        if self.hand[0].rank > 10 and self.hand[1].rank > 10:
            if self.get_max_comb_level() == 2:
                if self.hand[0].rank == 13:
                    self.predict_result = 0.8
                elif self.hand[0].rank == 14:
                    self.predict_result = 1
                else:
                    self.predict_result = 0.5
            else:
                if self.hand[0].suit == self.hand[1].suit:
                    self.predict_result = 0.4
                else:
                    self.predict_result = 0.3
