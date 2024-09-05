# file: Training.py
# description: Trains the CNN with my data
# author: María Victoria Anconetani
# date: 29/08/2024

import numpy as np
import tensorflow as tf

from PreProcessing import preprocess_from_csv
from CNNModel import MyCNN

# Load and preprocess training, validation, and test sets
train_images_pos, train_labels_pos = preprocess_from_csv('valid_dicom_files.csv', subset='PosTrain')
train_images_neg, train_labels_neg = preprocess_from_csv('valid_dicom_files.csv', subset='NegTrain')

val_images_pos, val_labels_pos = preprocess_from_csv('valid_dicom_files.csv', subset='PosVal')
val_images_neg, val_labels_neg = preprocess_from_csv('valid_dicom_files.csv', subset='NegVal')

test_images_pos, test_labels_pos = preprocess_from_csv('valid_dicom_files.csv', subset='PosTest')
test_images_neg, test_labels_neg = preprocess_from_csv('valid_dicom_files.csv', subset='NegTest')

# Combine positive and negative images and labels
train_images_combined = np.concatenate([train_images_pos, train_images_neg], axis=0)
train_labels_combined = np.concatenate([train_labels_pos, train_labels_neg], axis=0)

val_images_combined = np.concatenate([val_images_pos, val_images_neg], axis=0)
val_labels_combined = np.concatenate([val_labels_pos, val_labels_neg], axis=0)

test_images_combined = np.concatenate([test_images_pos, test_images_neg], axis=0)
test_labels_combined = np.concatenate([test_labels_pos, test_labels_neg], axis=0)

# Convert to TensorFlow tensors
train_dataset = tf.data.Dataset.from_tensor_slices((tf.convert_to_tensor(train_images_combined, dtype=tf.float32), tf.convert_to_tensor(train_labels_combined, dtype=tf.int32)))
val_dataset = tf.data.Dataset.from_tensor_slices((tf.convert_to_tensor(val_images_combined, dtype=tf.float32), tf.convert_to_tensor(val_labels_combined, dtype=tf.int32)))
test_dataset = tf.data.Dataset.from_tensor_slices((tf.convert_to_tensor(test_images_combined, dtype=tf.float32), tf.convert_to_tensor(test_labels_combined, dtype=tf.int32)))

# Shuffle and batch the datasets
train_dataset = train_dataset.shuffle(len(train_images_combined)).batch(32)
val_dataset = val_dataset.batch(32)
test_dataset = test_dataset.batch(32)

# Create and train the CNN model
cnn_model = MyCNN(input_shape=(256, 256, 1), num_classes=2)
cnn_model.train(train_dataset, val_dataset, epochs=10)

# Save the trained model
cnn_model.save_model('my_cnn_model.h5')

# Evaluate the model on the test dataset
cnn_model.evaluate(test_dataset)