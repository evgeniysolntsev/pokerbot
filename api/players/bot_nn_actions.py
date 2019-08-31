from api.players.template_bot import TemplateBot


class BotNNActions(TemplateBot):
    def __init__(self):
        super().__init__()

    def do_action(self):
        if super().is_skip():
            return 0
        # todo may be in future
        super().do_action()
