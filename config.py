# ======================================================================================================================
#               1st. When is defined winner, then game will start from the beginning, so to eternal
#               2nd. After player losing game, he gets again start points
ETERNAL_MODE = True
ETERNAL_MODE_AFTER_LOSING_PLAYER_ADDING_POINTS = False
# ======================================================================================================================
#               If enable need define type nn with count inputs, its boolean variables below
#               NN_WITH_INPUTS_ONLY_CARDS, NN_INPUTS_WITH_CARDS_AND_BOT_ACTION
#               *Only one variable may be equals true
LEARNING_MODE = True
PREDICTING_MODE = False
PLAYING_MODE = False
# ======================================================================================================================
#               Start point on hand when game beginning
# ======================================================================================================================
START_POINTS = 50
# ======================================================================================================================
#               For example, AsAdQdQsKs4s5d
#               AsAd on hand
#               QdQsKs on flop
#               4s on turn
#               5d on river
PREDICTING_DATA = 'AsAdQdQsKs4s5d'
# ======================================================================================================================
#               Types of neural network - only one variable may be equals true
#               *Only one variable may be equals true
NN_INPUTS_CARDS = True
NN_INPUTS_CARDS_AND_BOT_ACTIONS = False
# ======================================================================================================================
#               Names count equally player count, auto generate
HUMAN_NAMES = {
}
BOT_NAMES = {
    "bot", "botVasiliy"
}
# ======================================================================================================================
#               Additional info in console
OUTPUT_IN_CONSOLE = False
TEST_INFO = True
# ======================================================================================================================
#               10-14 equally T-A cards
RANGE_CARDS_ON_HAND = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# ======================================================================================================================
#               Variables of fitting neural network
N_EPOCH = 80
VALIDATION_SET = 0.1
FIT_QUANTITY = 3000000
SHOW_METRIC = True
# ======================================================================================================================

ABSOLUTE_PATH_TO_FOLDER_SAVED_DNN = "C:\\Users\\usr\PycharmProjects\pokerbot\saved_tensorflow_models\\"
PATH_NN_INPUTS_CARDS = ABSOLUTE_PATH_TO_FOLDER_SAVED_DNN + "saved_model_inputs_cards"
PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS = ABSOLUTE_PATH_TO_FOLDER_SAVED_DNN + "saved_model_inputs_cards_and_bot_actions"
