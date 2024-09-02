# file: CNNModel.py
# description: Implements a CNN that can be used to analyze DICOM images
# author: María Victoria Anconetani
# date: 29/08/2024

import pydicom
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras import layers, models
from keras import layers

class MyCNN:
    def __init__(self, input_shape=(256, 256, 1), num_classes=2):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self.build_model()
        
    def build_model(self):
        model = models.Sequential()

        # First Convolutional Block
        model.add(layers.Conv2D(64, (3, 3), strides=2, padding='same', input_shape=self.input_shape))
        model.add(layers.BatchNormalization())
        model.add(layers.ReLU())

        # Second Convolutional Block
        model.add(layers.Conv2D(128, (3, 3), strides=2, padding='same'))
        model.add(layers.BatchNormalization())
        model.add(layers.ReLU())

        # Third Convolutional Block
        model.add(layers.Conv2D(256, (3, 3), strides=2, padding='same'))
        model.add(layers.BatchNormalization())
        model.add(layers.ReLU())

        # Fourth Convolutional Block
        model.add(layers.Conv2D(512, (3, 3), strides=2, padding='same'))
        model.add(layers.BatchNormalization())
        model.add(layers.ReLU())

        # Global Average Pooling
        model.add(layers.GlobalAveragePooling2D())

        # Dropout Layer
        model.add(layers.Dropout(0.2))

        # Fully Connected Layer
        model.add(layers.Dense(16, activation='relu'))

        # Output Layer
        model.add(layers.Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        
        return model

    def train(self, train_data, validation_data, epochs=10, batch_size=32):
        history = self.model.fit(
            train_data,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data
        )
        return history

    def save_model(self, filepath):
        self.model.save(filepath)

    def load_model(self, filepath):
        self.model = tf.keras.models.load_model(filepath)

    def evaluate(self, test_data):
        return self.model.evaluate(test_data)

    def predict(self, x):
        return self.model.predict(x)
