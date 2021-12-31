"""
jonasnet.py

Model to classify via Convolutional Neural Network

Als Beispiel wie man das integriert -> model2
"""

import tensorflow.keras as keras
import tensorflow as tf
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.utils import class_weight
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from utils.preprocessing import prepare_tweet

class JonasNetClassifier:

    def __init__(self, model_dir, x_train, x_val, y_train, y_val, build=True):
        self.model = None
        self.output_dir = model_dir + '/assets/models/jonasnet/'

        self.x_train = x_train
        self.x_val = x_val
        self.y_train = y_train
        self.y_val = y_val
        self.tokenizer = self._create_tokenizer(x_train)

        self._build_model()

        print('------------------------------------------------')
        print('Build == ', build)
        print('------------------------------------------------')

        if build == False:
            print('------------------------------------------------')
            print('Loading weights')
            print('------------------------------------------------')
            self.model.load_weights(self.output_dir + 'model_init.hdf5')
        else:
            print('------------------------------------------------')
            print('Model training')
            print('------------------------------------------------')
            self.fit()
            self.model.save_weights(self.output_dir + 'model_init.hdf5')
            print('Model succesfully trained')
        


    def _build_model(self):

        print('Model is getting build.')

        self.model = keras.Sequential()

        self.model.add(keras.layers.Embedding(input_dim = (len(self.tokenizer.word_counts) + 1), output_dim = 128, input_length = 27))
        self.model.add(keras.layers.Conv1D(128, 5, activation='relu'))
        self.model.add(keras.layers.GlobalAveragePooling1D())
        self.model.add(keras.layers.Dropout(0.7))
        self.model.add(keras.layers.Dense(128, activation='relu'))
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(3, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', 
            patience=5, restore_best_weights=True)
        # reduceLR = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', 
        #     patience = 4, factor=0.7)


        file_path = self.output_dir+'best_model.hdf5'

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss', 
            save_best_only=True)

        self.callbacks = [
            # reduceLR,
            earlyStop, 
            model_checkpoint
        ]


    def fit(self):

        print('Model is getting fitted.')

        train_tweet = self.x_train
        test_tweet = self.x_val

        train_tweet = self.tokenizer.texts_to_sequences(train_tweet)
        test_tweet = self.tokenizer.texts_to_sequences(test_tweet)

        #Not every Tweet has the same legnth. The longest Tweet defines the size of the dataframe. 
        #Every Tweet, which is shorter, gets paddings in the empty cells
        train_tweet = pad_sequences(train_tweet, maxlen=27)
        test_tweet = pad_sequences(test_tweet, maxlen=27)

        encoder = LabelEncoder()

        y_train_categorical = encoder.fit_transform(self.y_train)
        y_train_categorical = to_categorical(self.y_train) 

        y_test_categorical = encoder.fit_transform(self.y_val)
        y_test_categorical = to_categorical(self.y_val) 

        custom_weights = class_weight.compute_class_weight(class_weight = 'balanced', classes=np.unique(self.y_train), y=self.y_train)

        def custom_weights_to_dictionary(weights):
            dic = {}
            for i in range(len(weights)):
                dic[i] = weights[i]
            return dic

        weights = custom_weights_to_dictionary(custom_weights)

        nb_epochs = 50

        self.hist = self.model.fit(
            train_tweet,
            y_train_categorical,
            validation_split=0.2,
            class_weight=weights,
            epochs= nb_epochs,
            shuffle=True,
            callbacks=self.callbacks)

        self.model.save(self.output_dir + 'last_model.hdf5')

        self.model = keras.models.load_model(self.output_dir + 'best_model.hdf5')

        keras.backend.clear_session()


    def _create_tokenizer(self, x_train):
        tokenizer = Tokenizer(lower=False)
        tokenizer.fit_on_texts(x_train)
        return tokenizer

    def predict(self, tweet):
        
        model_path = self.output_dir + 'best_model.hdf5'
        self.model = keras.models.load_model(model_path)

        prepared_tweet = prepare_tweet(tweet)

        sequenced_tweet = self.tokenizer.texts_to_sequences(np.array([prepared_tweet]))
        # print('sequenced ', sequenced_tweet)

        tokenized_tweet = pad_sequences(sequenced_tweet, maxlen=27)
        # print('tokenized shape ', tokenized_tweet.shape)
        # print('tokenized ', tokenized_tweet)

        y_predict = self.model.predict(tokenized_tweet)
        # print('y_predict shape ', y_predict.shape)
        # print('y_predict ', y_predict)

        return y_predict[0]