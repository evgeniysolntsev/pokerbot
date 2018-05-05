import config

N_PLAYERS = len(config.NAMES)
N_BOT_PLAYERS = len(config.BOT_NAMES)
N_ALL_PLAYERS = N_PLAYERS + N_BOT_PLAYERS
ALL_NAMES = []
ALL_NAMES.extend(config.NAMES)
ALL_NAMES.extend(config.BOT_NAMES)
MAX_LENGTH_NAME = max([len(name) for name in ALL_NAMES])
TEMP_NAMES = []
TEMP_BOT_NAMES = []
for name in config.NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_NAMES.append(name)
config.NAMES = TEMP_NAMES
for name in config.BOT_NAMES:
    if len(name) < MAX_LENGTH_NAME:
        while len(name) != MAX_LENGTH_NAME:
            name = name + " "
    TEMP_BOT_NAMES.append(name)
config.BOT_NAMES = TEMP_BOT_NAMES
ALL_NAMES = []
ALL_NAMES.extend(config.NAMES)
ALL_NAMES.extend(config.BOT_NAMES)
