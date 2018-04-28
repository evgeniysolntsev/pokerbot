from api.dnn import config
from api.helpers.singleton import singleton


@singleton
class Bank:
    bank = 0
    bet = 0
    step = config.START_POINTS / 100

    def set_bank(self, bank=None):
        self.bank = bank

    def add_to_bank(self, points=None):
        self.bank = self.bank + points

    def set_sb(self):
        self.bank = self.bank + (self.step / 2)

    def set_bb(self):
        self.bet = self.step
        self.bank = self.bank + self.step

    def set_bet(self, bet=None):
        self.bet = bet

    # def action_nn(self):
    #     map_state_nn = sub_action_nn(c_map=c_map, model=model, betEnemy=game.get('bet_'))
    #     game.__setitem__('bet_nn', map_state_nn.get('bet'))
    #     if map_state_nn.get('fold'):
    #         game.__setitem__('point_', game.get('point_') + game.get('bank'))
    #         print('saved_dnn fold')
    #         return True
    #     elif map_state_nn.get('call'):
    #         if game.get('bet_'):
    #             game.__setitem__('point_nn', game.get('point_nn') - game.get('bet_'))
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_'))
    #             print('saved_dnn call {}'.format(game.get('bet_')))
    #     elif map_state_nn.get('check'):
    #         print('saved_dnn check')
    #     elif game.get('bet_nn'):
    #         game.__setitem__('bet_nn', float(map_state_nn.get('bet')))
    #         if (game.get('point_nn') - game.get('bet_nn')) < 0:
    #             game.__setitem__('bank', game.get('bank') + game.get('point_nn'))
    #             game.__setitem__('point_nn', 0)
    #             game.__setitem__('all_in', True)
    #             print('saved_dnn all in {}'.format(game.get('point_nn')))
    #         else:
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_nn'))
    #             game.__setitem__('point_nn', game.get('point_nn') - game.get('bet_nn'))
    #             print('saved_dnn bet on {}'.format(game.get('bet_nn')))
    #     else:
    #         Exception('illegal saved_dnn')
    #     return False
    #
    # def sub_action_nn(c_map=None, model=None, betEnemy=None):
    #     predict_data = create_data(c_map=c_map)
    #     predict_points = model.predict(predict_data)
    #
    #     map_state = {
    #         'fold': False,
    #         'check': False,
    #         'call': False,
    #         'bet': None
    #     }
    #
    #     if differentPoint > 0.75:
    #         if betEnemy:
    #             if is_calling(betEnemy=betEnemy, differentPoint=differentPoint):
    #                 map_state.__setitem__('call', True)
    #             else:
    #                 map_state.__setitem__('fold', True)
    #         else:
    #             procent_of_max_bet = 0.25
    #             procent_win = int(differentPoint * 100)
    #             betPoint = procent_win * procent_of_max_bet
    #             map_state.__setitem__('bet', betPoint)
    #     elif differentPoint > 0.5:
    #         if betEnemy:
    #             if is_calling(betEnemy=betEnemy, differentPoint=differentPoint):
    #                 map_state.__setitem__('call', True)
    #             else:
    #                 map_state.__setitem__('fold', True)
    #         else:
    #             map_state.__setitem__('check', True)
    #     else:
    #         if betEnemy:
    #             map_state.__setitem__('fold', True)
    #         else:
    #             map_state.__setitem__('check', True)
    #     return map_state
    #
    # def is_calling(betEnemy=None, differentPoint=None):
    #     procent_of_max_bet = 0.25
    #     procent_win = int(differentPoint * 100)
    #     betPoint = procent_win * procent_of_max_bet
    #     return betPoint > betEnemy
    #
    # def playing_on_stage(pre_flop=False, c_map=None, model=None):
    #     print('----------------------')
    #     print('point_ {}'.format(game.get('point_')))
    #     print('point_nn {}'.format(game.get('point_nn')))
    #     print('----------------------')
    #     if game.get('all_in'):
    #         return False
    #     if game.get('dealer_nn'):
    #         if pre_flop:
    #             game.__setitem__('point_nn', game.get('point_nn') - .5)
    #             game.__setitem__('bank', game.get('bank') + .5)
    #         if action_nn(c_map=c_map, model=model):
    #             return True
    #         if action_():
    #             return True
    #         if game.get('bet_') and game.get('bet_') > 0:
    #             if action_nn(c_map=c_map, model=model):
    #                 return True
    #     else:
    #         if pre_flop:
    #             game.__setitem__('point_', game.get('point_') - .5)
    #             game.__setitem__('bank', game.get('bank') + .5)
    #         if action_():
    #             return True
    #         if action_nn(c_map=c_map, model=model):
    #             return True
    #         if game.get('bet_nn') and game.get('bet_nn') > 0:
    #             if action_():
    #                 return True
    #     game.__setitem__('bet_', None)
    #     game.__setitem__('bet_nn', None)
    #
    #     return False
    #
    # def playing(model=None, g=None):
    #     while True:
    #         if game.get('point_') <= 0:
    #             print('NN win')
    #             break
    #         elif game.get('point_nn') <= 0:
    #             print('_ win')
    #             break
    #         game.__setitem__('bank', 0)
    #         game.__setitem__('bet_', None)
    #         game.__setitem__('bet_nn', None)
    #
    #         g.pre_flop()
    #         c_map0, c_map1 = update_hands(g)
    #         game.__setitem__('dealer_nn', not game.get('dealer_nn'))
    #
    #         if playing_on_stage(pre_flop=True, c_map=c_map1, model=model):
    #             continue
    #
    #         g.flop()
    #         c_map0, c_map1 = update_hands(g)
    #
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         g.turn()
    #         c_map0, c_map1 = update_hands(g)
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         g.river()
    #         c_map0, c_map1 = update_hands(g)
    #
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         if g.get_index_winner() == 0:
    #             game.__setitem__('point_', game.get('point_') + game.get('bank'))
    #         else:
    #             game.__setitem__('point_nn', game.get('point_nn') + game.get('bank'))
    #
    # def action_():
    #     state = input('your action:')
    #     word = re.findall(r'\w*', state)[0]
    #     if word == 'fold':
    #         game.__setitem__('point_nn', game.get('point_nn') + game.get('bank'))
    #         print('_ fold')
    #         return True
    #     elif word == 'call':
    #         if game.get('bet_nn'):
    #             game.__setitem__('point_', game.get('point_') - game.get('bet_nn'))
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_nn'))
    #             print('_ call {}'.format(game.get('bet_nn')))
    #     elif word == 'check':
    #         print('check')
    #     elif word == 'bet':
    #         game.__setitem__('bet_', float(re.findall(r'\d{1,3}', state)[0]))
    #         if (game.get('point_') - game.get('bet_')) < .0:
    #             game.__setitem__('bank', game.get('bank') + game.get('point_'))
    #             game.__setitem__('point_', 0)
    #             game.__setitem__('all_in', True)
    #             print('_ all in {}'.format(game.get('point_')))
    #         else:
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_'))
    #             game.__setitem__('point_', game.get('point_') - game.get('bet_'))
    #             print('_ bet on {}'.format(game.get('bet_')))
    #     else:
    #         Exception('illegal input')
    #     return False
    #
    #
    # def action_nn(c_map=None, model=None):
    #     map_state_nn = sub_action_nn(c_map=c_map, model=model, betEnemy=game.get('bet_'))
    #     game.__setitem__('bet_nn', map_state_nn.get('bet'))
    #     if map_state_nn.get('fold'):
    #         game.__setitem__('point_', game.get('point_') + game.get('bank'))
    #         print('saved_dnn fold')
    #         return True
    #     elif map_state_nn.get('call'):
    #         if game.get('bet_'):
    #             game.__setitem__('point_nn', game.get('point_nn') - game.get('bet_'))
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_'))
    #             print('saved_dnn call {}'.format(game.get('bet_')))
    #     elif map_state_nn.get('check'):
    #         print('saved_dnn check')
    #     elif game.get('bet_nn'):
    #         game.__setitem__('bet_nn', float(map_state_nn.get('bet')))
    #         if (game.get('point_nn') - game.get('bet_nn')) < 0:
    #             game.__setitem__('bank', game.get('bank') + game.get('point_nn'))
    #             game.__setitem__('point_nn', 0)
    #             game.__setitem__('all_in', True)
    #             print('saved_dnn all in {}'.format(game.get('point_nn')))
    #         else:
    #             game.__setitem__('bank', game.get('bank') + game.get('bet_nn'))
    #             game.__setitem__('point_nn', game.get('point_nn') - game.get('bet_nn'))
    #             print('saved_dnn bet on {}'.format(game.get('bet_nn')))
    #     else:
    #         Exception('illegal saved_dnn')
    #     return False
    #
    #
    # def playing_on_stage(pre_flop=False, c_map=None, model=None):
    #     print('----------------------')
    #     print('point_ {}'.format(game.get('point_')))
    #     print('point_nn {}'.format(game.get('point_nn')))
    #     print('----------------------')
    #     if game.get('all_in'):
    #         return False
    #     if game.get('dealer_nn'):
    #         if pre_flop:
    #             game.__setitem__('point_nn', game.get('point_nn') - .5)
    #             game.__setitem__('bank', game.get('bank') + .5)
    #         if action_nn(c_map=c_map, model=model):
    #             return True
    #         if action_():
    #             return True
    #         if game.get('bet_') and game.get('bet_') > 0:
    #             if action_nn(c_map=c_map, model=model):
    #                 return True
    #     else:
    #         if pre_flop:
    #             game.__setitem__('point_', game.get('point_') - .5)
    #             game.__setitem__('bank', game.get('bank') + .5)
    #         if action_():
    #             return True
    #         if action_nn(c_map=c_map, model=model):
    #             return True
    #         if game.get('bet_nn') and game.get('bet_nn') > 0:
    #             if action_():
    #                 return True
    #     game.__setitem__('bet_', None)
    #     game.__setitem__('bet_nn', None)
    #
    #     return False
    #
    #
    # def playing(model=None, g=None):
    #     while True:
    #         if game.get('point_') <= 0:
    #             print('NN win')
    #             break
    #         elif game.get('point_nn') <= 0:
    #             print('_ win')
    #             break
    #         game.__setitem__('bank', 0)
    #         game.__setitem__('bet_', None)
    #         game.__setitem__('bet_nn', None)
    #
    #         g.pre_flop()
    #         c_map0, c_map1 = update_hands(g)
    #         game.__setitem__('dealer_nn', not game.get('dealer_nn'))
    #
    #         if playing_on_stage(pre_flop=True, c_map=c_map1, model=model):
    #             continue
    #
    #         g.flop()
    #         c_map0, c_map1 = update_hands(g)
    #
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         g.turn()
    #         c_map0, c_map1 = update_hands(g)
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         g.river()
    #         c_map0, c_map1 = update_hands(g)
    #
    #         if playing_on_stage(c_map=c_map1, model=model):
    #             continue
    #
    #         if g.get_index_winner() == 0:
    #             game.__setitem__('point_', game.get('point_') + game.get('bank'))
    #         else:
    #             game.__setitem__('point_nn', game.get('point_nn') + game.get('bank'))
