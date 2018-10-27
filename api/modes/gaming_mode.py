import config
from api.helpers.model import Model
from api.helpers.singleton import singleton
from api.poker.core_action import CoreAction


@singleton
class GamingMode(object):

    @staticmethod
    def action():
        if config.NN_INPUTS_CARDS:
            Model.init_tf_model_with_input_cards(load=True)
        else:
            Model.init_tf_model_with_input_cards_and_bot_actions(load=True)
        CoreAction.playing()
