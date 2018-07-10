import tensorflow
import tflearn

import config
from api.helpers.singleton import singleton


@singleton
class Model:
    @staticmethod
    def init_net_bot_mode():
        net = tflearn.input_data([None, 268])
        net = tflearn.fully_connected(net, 7000, activation="RElu")
        net = tflearn.fully_connected(net, 100, activation="RElu")
        net = tflearn.fully_connected(net, 2, activation="softmax")
        net = tflearn.regression(net, optimizer='Momentum', loss='mean_square', learning_rate=0.01)
        return net

    @staticmethod
    def init_net_mode():
        net = tflearn.input_data([None, 68])
        net = tflearn.fully_connected(net, 1800, activation="RElu")
        net = tflearn.fully_connected(net, 100, activation="RElu")
        net = tflearn.fully_connected(net, 2, activation="softmax")
        net = tflearn.regression(net, optimizer='Momentum', loss='mean_square', learning_rate=0.01)
        return net

    def __init__(self):
        tensorflow.reset_default_graph()
        simple = None
        simple_exp = config.CUSTOM_BOT or config.RANDOM_BOT
        first_exp = config.PLAYING_MODE and simple_exp
        second_exp = config.SIMPLE_NN and simple_exp and not config.EXTENDED_NN
        third_exp = (config.PLAYING_MODE and not simple_exp) or config.EXTENDED_NN
        if first_exp or second_exp:
            net = self.init_net_mode()
            simple = True
        elif third_exp:
            net = self.init_net_bot_mode()
            simple = False
        else:
            exit("bad config: except correct mode - custom and random for simple")
        dnn = tflearn.DNN(net)
        self.dnn = dnn
        if config.LOADING_MODEL:
            if simple:
                path = config.PATH_SIMPLE_NN
            else:
                path = config.PATH_EXTENDED_NN
            self.load(path)

    def init_learning_bot_mode(self):
        tensorflow.reset_default_graph()
        dnn = tflearn.DNN(self.init_net_bot_mode())
        self.dnn = dnn

    def load(self, path=None):
        self.dnn.load(path)
