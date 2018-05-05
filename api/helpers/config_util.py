import config

N_PLAYERS = len(config.NAMES)
N_BOT_PLAYERS = len(config.BOT_NAMES)
N_ALL_PLAYERS = N_PLAYERS + N_BOT_PLAYERS
ALL_NAMES = []
ALL_NAMES.extend(config.NAMES)
ALL_NAMES.extend(config.BOT_NAMES)
MAX_LENGTH_NAME = max([len(name) for name in ALL_NAMES])
