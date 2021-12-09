"""
jonasnet.py

Model to classify via Convolutional Neural Network

Als Beispiel wie man das integriert -> model2
"""

import tensorflow.keras as keras
import tensorflow as tf
import numpy as np


class JonasNetClassifier:

    def __init__(self, output_dir, input_shape,
                 nb_labels, build=True, load_weights=False):
        self.model = None
        self.output_dir = '../assets/models/' + 'jonasnet/'

        if build == True:
            self.model = self.build_model(input_shape, nb_labels)
            self.model.save_weights(self.output_dir + 'model_init.hdf5')


    def build_model(self, input_shape, nb_labels):

        self.model = keras.Sequential()

        self.model.add(keras.layers.Embedding(nb_labels, 16))
        self.model.add(keras.layers.Conv1D(128, 5, activation='relu'))
        self.model.add(keras.layers.GlobalAveragePooling1D())
        self.model.add(keras.layers.Dropout(0.5))
        self.model.add(keras.layers.Dense(16, activation="relu"))
        self.model.add(keras.layers.Dense(16, activation="relu"))
        self.model.add(keras.layers.Dense(16, activation="relu"))
        self.model.add(keras.layers.Dense(16, activation="relu"))

        self.model.add(keras.layers.Dense(1, activation = "sigmoid"))

        self.model.compile(optimizer="adam", loss=tf.keras.losses.CategoricalCrossentropy(), metrics=["accuracy"])


        # ist nur beispielhaft also nicht angepasst & debugged





    def fit(self, x_train, y_train, x_val, y_val):

        batch_size = 16
        nb_epochs = 10

        mini_batch_size = int(min(x_train.shape[0]/10, batch_size))

        hist = self.model.fit(x_train,
                              y_train,
                              batch_size=mini_batch_size,
                              verbose=False,
                              validatioon_data=(x_val, y_val))

        self.model.save(self.output_dir + 'last_model.hdf5')

        self.model = keras.models.load_model(self.output_dir + 'best_model.hdf5')

        y_predict = self.mode.validate(x_val)
        y_predict = np.argmax(y_predict, axis=1) # conversion to integer (from binary)

        # Ergebnisse y_predict können dann gesaved werden etc.

        keras.backend.clear_session()



    def validate(self, x_train, y_train, x_val, y_val):
        pass # ...


    def predict(self, x_predict, y_predict):

        model_path = self.output_dir + 'best_model.hdf5'
        self.model = keras.models.load_model(model_path)

        y_predict = self.model.predict(x_predict)
        return y_predict