from api.helpers.singleton import singleton
from api.poker.computer_action import ComputerAction


@singleton
class GamingMode(object):
    def __init__(self):
        ComputerAction.playing()
