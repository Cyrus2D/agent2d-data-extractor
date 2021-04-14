import pandas as pd
import numpy as np
import random
import tensorflow.keras as keras
import keras.backend as K
import matplotlib.pyplot as plt
import copy
import sys
from tensorflow.keras.callbacks import ModelCheckpoint


print ('Argument List:', str(sys.argv))
input_data_type = sys.argv[1]
output_data_type = sys.argv[2]
file_index = sys.argv[3]
label = output_data_type
path = f'/home/nader/data/robo_data/{input_data_type}/'
model = f'{input_data_type}__{output_data_type}__{file_index}.h5'


def read_date(read_path):
    df = pd.read_csv(read_path, dtype=float)
    df.dropna(inplace=True)
    just_test = False
    try:
        del df['index']
    except:
        pass
    header = df.columns
    header_x = []
    header_y = []

    for h in header:
        header_name = h.strip()
        if header_name.startswith('out_'):
            header_y.append(h)
        else:
            # if h in good_f:
            if h.endswith('_pos_x') or h.endswith('_pos_y'):
                header_x.append(h)
    header_y = [label]
    for h in copy.copy(header_x):
        if h.find('history') >= 0:
            header_x.remove(h)
            continue
        if h.find('Unnamed') >= 0:
            header_x.remove(h)
            continue
    df_x = df[header_x]
    df_y = df[header_y]
    del df
    try:
        del df_x['Unnamed: 0']
        del df_x['Unnamed: 0.1']
    except:
        pass
    x = df_x.to_numpy()
    del df_x
    y = df_y.to_numpy()
    del df_y

    shuffle = list(range(0, x.shape[0]))
    random.shuffle(shuffle)
    x = x[shuffle]
    y = y[shuffle]
    y = keras.utils.to_categorical(y, num_classes=13)
    return x, y


x_train, y_train = read_date(path + 'train.csv')
x_test, y_test = read_date(path + 'test.csv')


def accuracy1(y_true, y_pred):
    y_true = K.cast(y_true, y_pred.dtype)
    y_true = K.argmax(y_true)
    res = K.in_top_k(y_pred, y_true, 1)
    return res


def train():
    network = keras.models.Sequential()
    network.add(keras.layers.Dense(1024, activation=keras.activations.sigmoid, input_shape=(x_train.shape[1],)))
    network.add(keras.layers.Dropout(0.1))
    network.add(keras.layers.Dense(512, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(256, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(64, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(32, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(y_train.shape[1], activation=keras.activations.softmax))
    network.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=[accuracy1])
    metric = 'val_accuracy1'
    callback = [ModelCheckpoint(filepath=model, monitor=metric, verbose=1, save_best_only=True, mode='max')]
    history = network.fit(x_train,
                          y_train,
                          epochs=100,
                          batch_size=1024,
                          validation_data=(x_test, y_test),
                          callbacks=callback,
                          verbose=0)
    res = network.evaluate(x_test, y_test)
    history_dict = history.history
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    acc1_values = history_dict['accuracy1']
    val_acc1_values = history_dict['val_accuracy1']
    print(model, 'best val:', max(val_acc1_values))
    # epochs = range(len(loss_values))
    # plt.figure(1)
    # plt.subplot(311)
    # plt.plot(epochs, loss_values, 'r--', label='Training loss')
    # plt.plot(epochs, val_loss_values, 'b--', label='Validation loss')
    # plt.title("train/test loss")
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.legend()
    # plt.subplot(312)
    # plt.plot(epochs, acc1_values, 'r--', label='Training mean_squared_error')
    # plt.plot(epochs, val_acc1_values, '--', label='Validation mean_squared_error')
    # plt.title("train/test acc")
    # plt.xlabel('Epochs')
    # plt.ylabel('Acc')
    # plt.legend()
    # plt.show()
    # network.save(model)

train()