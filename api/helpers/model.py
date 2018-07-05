import tensorflow
import tflearn

import config
from api.helpers.singleton import singleton


@singleton
class Model:
    def __init__(self):
        tensorflow.reset_default_graph()
        if config.LEARNING_MODE:
            net = self.init_net_mode()
        elif config.LEARNING_BOT_MODE or config.PLAYING_MODE:
            net = self.init_net_bot_mode()
        dnn = tflearn.DNN(net)
        self.dnn = dnn
        if config.LOADING_MODEL:
            self.load(config.PATH_DNN)

    def init_learning_bot_mode(self):
        tensorflow.reset_default_graph()
        dnn = tflearn.DNN(self.init_net_bot_mode())
        self.dnn = dnn

    @staticmethod
    def init_net_bot_mode():
        net = tflearn.input_data([None, 268])
        net = tflearn.fully_connected(net, 3000, activation="RElu")
        net = tflearn.fully_connected(net, 500, activation="RElu")
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

    def load(self, path=None):
        self.dnn.load(path)
