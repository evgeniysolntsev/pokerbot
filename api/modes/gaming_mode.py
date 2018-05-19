from api.helpers.singleton import singleton
from api.poker.computer_action import ComputerAction


@singleton
class GamingMode(object):

    @staticmethod
    def action():
        ComputerAction.playing()
