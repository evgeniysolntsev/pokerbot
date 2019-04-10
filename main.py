import config
from api.modes.gaming_mode import GamingMode
from api.modes.learning_mode_inputs_cards import LearningModeInputsCards
from api.modes.learning_mode_inputs_cards_and_bot_actions import LearningModeInputsCardsAndBotActions
from api.modes.predicting_mode import PredictingMode

if __name__ == '__main__':
    if config.PLAYING_MODE:
        GamingMode.action()
    elif config.LEARNING_MODE and config.NN_INPUTS_CARDS:
        LearningModeInputsCards.do_play()
    elif config.LEARNING_MODE and config.NN_INPUTS_CARDS_AND_BOT_ACTIONS:
        LearningModeInputsCardsAndBotActions.action()
    elif config.PREDICTING_MODE:
        PredictingMode.action()
