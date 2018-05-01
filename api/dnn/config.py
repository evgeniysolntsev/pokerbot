# COMMON
NAMES = {

}
BOT_NAMES = {
    "generous", "greedy", "nihilist", "beginner", "cub", "alliner", "folder", "checker", "alien"
}
LOADING_MODEL = True
OUTPUT_IN_CONSOLE = True
RANGE_HAND = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# RANGE_HAND = [10, 11, 12, 13, 14]
# MODE
PREDICTING_MODE = False
LEARNING_MODE = False
PLAYING_MODE = True
# LEARNING
N_EPOCH = 10
VALIDATION_SET = 0.1
FIT_QUANTITY = 10000
SHOW_METRIC = True
# PLAYING
START_POINTS = 50

# BOT_NAMES = {
#     "generous", "greedy", "nihilist", "beginner", "cub", "alliner", "folder", "checker", "alien", "grown", "child"
# }
PATH_DNN = "C:\\Users\evgeniy\PycharmProjects\\pokerbot\saved_dnn\example"
N_PLAYERS = len(NAMES)
N_BOT_PLAYERS = len(BOT_NAMES)
N_ALL_PLAYERS = N_PLAYERS + N_BOT_PLAYERS
ALL_NAMES = []
ALL_NAMES.extend(NAMES)
ALL_NAMES.extend(BOT_NAMES)
MAX_LENGTH_NAME = max([len(name) for name in ALL_NAMES])
