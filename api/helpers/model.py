import tensorflow as tf
from tensorflow.keras.layers import Dense

import config
from api.helpers.singleton import singleton


@singleton
class Model:
    dnn = {}

    def init_tf_model_with_input_cards_and_bot_actions(self, load=False):
        tf.reset_default_graph()
        model = tf.keras.Sequential()
        model.add(Dense(units=500, activation='relu', input_shape=[268, ]))
        model.add(Dense(units=250, activation='relu'))
        model.add(Dense(units=2, activation='softmax'))
        model.compile(optimizer=tf.train.GradientDescentOptimizer(0.01),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        self.dnn = model
        if load:
            self.dnn.load_weights(config.PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS)

    def init_tf_model_with_input_cards(self, load=False):
        tf.reset_default_graph()

        model = tf.keras.Sequential()
        model.add(Dense(units=500, activation='relu', input_shape=[68, ]))
        model.add(Dense(units=250, activation='relu'))
        model.add(Dense(units=2, activation='softmax'))
        model.compile(optimizer=tf.train.GradientDescentOptimizer(0.01),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        # model.save(config.PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS)
        self.dnn = model
        if load:
            self.dnn.load_weights(config.PATH_NN_INPUTS_CARDS)
