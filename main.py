from api.dnn import config
from api.modes.gaming_mode import GamingMode
from api.modes.learning_mode import LearningMode

if __name__ == '__main__':
    if config.LEARNING_MODE:
        LearningMode()
    elif config.PLAYING_MODE:
        GamingMode()
