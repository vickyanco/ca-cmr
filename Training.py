# file: Training.py
# description: Trains the CNN with my data
# author: María Victoria Anconetani
# date: 29/08/2024

import pandas as pd
import tensorflow as tf
from PreProcessing import load_and_preprocess_image
from CNNModel import MyCNN

df = pd.read_csv('valid_dicom_files.csv')

train_df = df[(df['set'] == 'NegTrain') | (df['set'] == 'PosTrain')]
val_df = df[(df['set'] == 'NegVal') |(df['set'] == 'PosVal')]

# Create TensorFlow datasets
train_ds = tf.data.Dataset.from_tensor_slices((train_df['filepath'].values, train_df['label'].values))
train_ds = train_ds.map(load_and_preprocess_image).batch(32)

val_ds = tf.data.Dataset.from_tensor_slices((val_df['filepath'].values, val_df['label'].values))
val_ds = val_ds.map(load_and_preprocess_image).batch(32)

cnn_model = MyCNN(input_shape=(256, 256, 1), num_classes=2)
cnn_model.train(train_ds, val_ds, epochs=10)
cnn_model.save_model('my_cnn_model.h5')