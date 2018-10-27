import tensorflow
import tflearn

import config
from api.helpers.singleton import singleton


@singleton
class Model:
    def init_tf_model_with_input_cards_and_bot_actions(self, load=False):
        tensorflow.reset_default_graph()

        model = tflearn.input_data([None, 268])

        model = tflearn.fully_connected(model, 7000, activation="RElu")
        model = tflearn.fully_connected(model, 100, activation="RElu")
        model = tflearn.fully_connected(model, 2, activation="softmax")
        model = tflearn.regression(model, optimizer='Momentum', loss='mean_square', learning_rate=0.01)

        self.dnn = tflearn.DNN(model)
        if load:
            self.dnn.load(config.PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS)

    def init_tf_model_with_input_cards(self, load=False):
        tensorflow.reset_default_graph()

        model = tflearn.input_data([None, 68])

        model = tflearn.fully_connected(model, 1800, activation="RElu")
        model = tflearn.fully_connected(model, 100, activation="RElu")
        model = tflearn.fully_connected(model, 2, activation="softmax")
        model = tflearn.regression(model, optimizer='Momentum', loss='mean_square', learning_rate=0.01)

        self.dnn = tflearn.DNN(model)
        if load:
            self.dnn.load(config.PATH_NN_INPUTS_CARDS)
