class ActionState:
    points_in_bank = None
    all_in = False
    action = None
    predict = 0
    combination_str = None
    total_point = 0

    def __init__(self):
        self.comb_level = 0
        self.total_point = 0
        self.points_in_bank = 0
        self.all_in = False
        self.action = 'nope'
        self.folded = False
        self.predict = 0
        self.combination_str = None
