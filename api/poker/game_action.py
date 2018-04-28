from api.poker.computer_action import ComputerAction
from api.utils.singleton import singleton


@singleton
class GameAction(object):
    def __init__(self):
        ComputerAction.random_dealer()
        while ComputerAction.is_end_game():
            first = ComputerAction.do_default_state()
            for stage in range(4):
                ComputerAction.play_stage()
                player = first
                while ComputerAction.is_continue() and ComputerAction.is_all_did_action():
                    if not player.did_action:
                        player.do_action()
                    player = player.get_next()
                ComputerAction.end_stage()
                if ComputerAction.is_new_game():
                    break
            ComputerAction.set_points_winner()
