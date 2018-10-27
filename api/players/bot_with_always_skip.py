import random

from api.players.template_bot import TemplateBot


class BotWithAlwaysSkip(TemplateBot):
    def __init__(self):
        super().__init__()
        self.bet_limit = random.randint(0, 100)
        self.call_limit = random.randint(0, self.bet_limit)

    def do_action(self):
        return 0
