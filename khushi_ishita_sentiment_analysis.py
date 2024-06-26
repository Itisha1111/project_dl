# -*- coding: utf-8 -*-
"""Khushi_Ishita_Sentiment analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vv4pCCBJ-q4BieqCtmemUHjtz_9RruIc
"""

import tensorflow as tf
import tensorflow_datasets as tfds

# Load the IMDb reviews dataset
train_ds, test_ds = tfds.load('imdb_reviews', split=['train', 'test'], with_info=False)

# Initialize lists to store x_train, x_test, y_train, and y_test
x_train = []
y_train = []
x_test = []
y_test = []

# Initialize a list to store positive reviews
positive_reviews = []

# Iterate over the train dataset and extract text and labels
for example in train_ds:
    text = example['text'].numpy().decode('utf-8')
    label = example['label'].numpy()
    if label == 1:  # Positive sentiment
        positive_reviews.append(text)

    x_train.append(text)
    y_train.append(label)

# Iterate over the test dataset and extract text and labels
for example in test_ds:
    text = example['text'].numpy().decode('utf-8')
    label = example['label'].numpy()
    x_test.append(text)
    y_test.append(label)

"""#Data Pre-processing"""

# Join all positive reviews into a single string
positive_reviews_text = ' '.join(positive_reviews)

#Positive Sentiment word cloud

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width = 480, height = 480,
                background_color = 'black',
                stopwords = None,
                min_font_size = 10).generate(positive_reviews_text)

# Display the word cloud
plt.figure(figsize = (6, 6), facecolor = None)
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis("off")
plt.margins(x=0, y=0)
plt.title('Positive Sentiment Word Cloud')

# Show plot
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Combine the training and testing labels
all_labels = np.concatenate((y_train, y_test), axis=0)

# Count the occurrences of each sentiment label
unique, counts = np.unique(all_labels, return_counts=True)
sentiment_counts = dict(zip(unique, counts))

# Plot the bar chat
plt.figure(figsize=(8,4))
plt.subplot(1,1,1)
plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['blue', 'red'])
plt.xticks(list(sentiment_counts.keys()), ['Negative', 'Positive'])
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Sentiments in Imdb Dataset using Bar Plot')
plt.show()




# Plot the pie chart
plt.subplot(1, 2, 2)
plt.pie(sentiment_counts.values(), labels=['Negative', 'Positive'], colors=['blue', 'red'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Distribution of Sentiments in IMDb Dataset using Pie Chart')
plt.tight_layout()
plt.show()

x_train[:4]

import tensorflow as tf
import re
import string
from IPython.display import display

def standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    no_tag = tf.strings.regex_replace(lowercase, "<[^>]+>", "")
    output = tf.strings.regex_replace(no_tag, "[%s]" % re.escape(string.punctuation), "")
    return output

# Convert to eager tensor
x_train_eager = tf.constant(x_train)

# Apply standardization
training = standardization(x_train_eager)

# Convert eager tensor to list of strings
training_list = [str(sentence, 'utf-8') for sentence in training.numpy()]

display(training_list[:5])
print(type(training_list))

vocab_size = 10000
embedding_dim = 16
max_length = 200
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_list)
word_index = tokenizer.word_index
training_sequences = tokenizer.texts_to_sequences(training_list)
training_padded = pad_sequences(training_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

testing_sequences = tokenizer.texts_to_sequences(x_test)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

print("Word index:\n", word_index)
print("\nTraining sequence:\n", training_padded)
print("\nTest sequence:\n", testing_padded)

print("x_train shape:", training_padded.shape)
print("x_test shape:", testing_padded.shape)

print(type(training_padded))
print(type(y_train))
print(type(testing_padded))
print(type(y_test))
print(type(training_list))

import tensorflow as tf

training_padded = tf.convert_to_tensor(training_padded)
y_train = tf.convert_to_tensor(y_train)
testing_padded = tf.convert_to_tensor(testing_padded)
y_test = tf.convert_to_tensor(y_test)

import tensorflow as tf### models
import numpy as np### math computations
import matplotlib.pyplot as plt### plotting bar chart
import sklearn### machine learning library
import cv2## image processing
from sklearn.metrics import confusion_matrix, roc_curve### metrics
import seaborn as sns### visualizations
import datetime
import pathlib
import io
import os
import re
import string
import time
from numpy import random
import gensim.downloader as api
from PIL import Image
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
from tensorflow.keras.models import Model , Sequential
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import (Dense,Flatten,SimpleRNN,InputLayer,Conv1D,Bidirectional,GRU,LSTM,BatchNormalization,Dropout,Input, Embedding,TextVectorization)
from tensorflow.keras.losses import BinaryCrossentropy,CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.metrics import Accuracy,TopKCategoricalAccuracy, CategoricalAccuracy, SparseCategoricalAccuracy
from tensorflow.keras.optimizers import Adam
from google.colab import drive
from google.colab import files
from tensorboard.plugins import projector

"""#Simple RNN"""

model=tf.keras.models.Sequential([
    Input(shape=(max_length,)),
    Embedding(vocab_size,embedding_dim),
    SimpleRNN(32, activation='tanh',
                        return_sequences=False),
    Dense(1,activation='sigmoid'),
])
model.summary()

checkpoint_filepath = '/content/drive/MyDrive/nlp/sentiment_analysis/rnn.h5'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history=model.fit(
    training_padded, y_train, validation_data=(testing_padded, y_test),
    epochs=10,
    callbacks=[])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('model_accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#Simple RNN
loss, accuracy = model.evaluate(testing_padded, y_test)
print("Loss:", loss)
print("Accuracy:", accuracy)

"""#LSTM"""

model=tf.keras.models.Sequential([
    Input(shape=(max_length,)),
    Embedding(vocab_size,embedding_dim),

    LSTM(64,return_sequences=True),
    LSTM(32),

    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1,activation='sigmoid'),
])
model.summary()

model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

checkpoint_filepath = '/content/drive/MyDrive/nlp/sentiment_analysis/rnn.h5'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

history= model.fit(
    training_padded, y_train, validation_data=(testing_padded, y_test),
    epochs=10,
    callbacks=[model_checkpoint_callback])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('model_accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#LSTM
loss, accuracy = model.evaluate(testing_padded, y_test)
print("Loss:", loss)
print("Accuracy:", accuracy)

"""##GRU"""

model=tf.keras.models.Sequential([
    Input(shape=(max_length,)),
    Embedding(vocab_size,embedding_dim),

    Bidirectional(GRU(64,return_sequences=True)),
    Bidirectional(GRU(32)),

    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1,activation='sigmoid'),
])
model.summary()

model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history=model.fit(
    training_padded, y_train, validation_data=(testing_padded, y_test),
    epochs=10,
    callbacks=[])

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('model_accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#GRU
loss, accuracy = model.evaluate(testing_padded, y_test)
print("Loss:", loss)
print("Accuracy:", accuracy)

#GRU
loss, accuracy = model.evaluate(training_padded, y_train)
print("Loss:", loss)
print("Accuracy:", accuracy)

# Using the model to predict a review
reviews = ['I love this phone', 'I hate spaghetti',
                'Everything was cold',
                'Everything was hot exactly as I wanted',
                'Everything was green',
                'the host seated us immediately',
                'they gave us free chocolate cake',
                'not sure about the wilted flowers on the table',
                'only works when I stand on tippy toes',
                'does not work when I stand on my head']

print(reviews)

# Creating the sequences
padding_type='post'
sample_sequences = tokenizer.texts_to_sequences(reviews)
padded = pad_sequences(sample_sequences, padding=padding_type, maxlen=max_length)

classes = model.predict(padded)

for x in range(len(reviews)):
  print(reviews[x])
  print(classes[x])
  print('\n')

#Confusion Matrix
from sklearn.metrics import confusion_matrix
import numpy as np
import itertools

# Make predictions on the test set
# Make predictions on the test set
y_pred_prob = model.predict(testing_padded).flatten()
y_pred = (y_pred_prob > 0.5).astype(int)


# Create confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.get_cmap('Blues'))
plt.title('Confusion matrix')
plt.colorbar()

# Add labels to the plot
classes = ['Negative', 'Positive']
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

# Add numbers to the plot
thresh = conf_matrix.max() / 2.
for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
    plt.text(j, i, format(conf_matrix[i, j], 'd'),
             horizontalalignment="center",
             color="white" if conf_matrix[i, j] > thresh else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()

"""#Embedding Projector ( Visualizing the network )
The code below will download two files for visualizing how your network "sees" the sentiment related to each word. Head to http://projector.tensorflow.org/ and load these files, then click the checkbox to "sphereize" the data.
"""

# First get the weights of the embedding layer
e = model.layers[0]
weights = e.get_weights()[0]
print(weights.shape)

import io

# Create the reverse word index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Write out the embedding vectors and metadata
out_v = io.open('vecs.tsv', 'w', encoding='utf-8')
out_m = io.open('meta.tsv', 'w', encoding='utf-8')
for word_num in range(1, vocab_size):
  word = reverse_word_index[word_num]
  embeddings = weights[word_num]
  out_m.write(word + "\n")
  out_v.write('\t'.join([str(x) for x in embeddings]) + "\n")
out_v.close()
out_m.close()

# Download the files
try:
  from google.colab import files
except ImportError:
  pass
else:
  files.download('vecs.tsv')
  files.download('meta.tsv')