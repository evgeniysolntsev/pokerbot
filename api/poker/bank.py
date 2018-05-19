import config
from api.helpers.singleton import singleton


@singleton
class Bank:
    bank = 0
    bet = 0
    step = config.START_POINTS / 100

    def set_bank(self, bank=None):
        self.bank = bank

    def add_to_bank(self, points=None):
        self.bank = self.bank + points

    def set_sb(self):
        self.bank = self.bank + (self.step / 2)

    def set_bb(self):
        self.bet = self.step
        self.bank = self.bank + self.step

    def set_bet(self, bet=None):
        if bet > self.bet:
            self.bet = bet
