from api.players.template_bot import TemplateBot


class BotAlwaysSkip(TemplateBot):
    def __init__(self):
        super().__init__()

    def do_action(self):
        self.did_action = True
