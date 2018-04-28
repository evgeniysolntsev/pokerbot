class ActionState:
    bank = None
    total_point = None
    all_in = False
    folded = False

    def __init__(self):
        self.bank = 0
        self.total_point = None
        self.all_in = False
        self.folded = False
