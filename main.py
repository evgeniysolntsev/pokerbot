import config
from api.modes.gaming_mode import GamingMode
from api.modes.learning_mode import LearningModeInputsCards
from api.modes.predicting_mode import PredictingMode

if __name__ == '__main__':
    if config.PLAYING_MODE:
        GamingMode.action()
    elif config.LEARNING_MODE and config.NN_INPUTS_CARDS:
        LearningModeInputsCards.action()
    elif config.PREDICTING_MODE:
        PredictingMode.action()
