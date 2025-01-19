import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from tensorflow.python.framework import ops

import config
from api.helpers.singleton import singleton


@singleton
class Model:
    dnn = {}

    def init_tf_model_with_input_cards(self, load=False):
        ops.reset_default_graph()

        model = tf.keras.Sequential()
        model.add(Dense(units=68, activation='elu', input_shape=[68, ]))
        model.add(Dense(units=34, activation='elu'))
        model.add(Dense(units=17, activation='elu'))
        model.add(Dense(units=2, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        # model.save(config.PATH_NN_INPUTS_CARDS_AND_BOT_ACTIONS)
        self.dnn = model
        if load:
            self.dnn.load_weights(config.PATH_NN_INPUTS_CARDS)

    def fit_tf_model_with_input_cards(self, x=None, y=None):
        self.dnn.fit(
            x=np.array(x),
            y=to_categorical(y, 2),
            epochs=config.N_EPOCH,
            batch_size=config.BATCH_SIZE,
            steps_per_epoch=config.STEPS_PER_EPOCH,
            validation_split=config.VALIDATION_SET,
            callbacks=[ModelCheckpoint(filepath='saved_tensorflow_models/saved_model_inputs_cards{epoch:03d}')]
        )
        self.dnn.save(config.PATH_NN_INPUTS_CARDS)
