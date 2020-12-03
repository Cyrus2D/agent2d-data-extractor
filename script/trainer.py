import pandas as pd
import numpy as np
import random
import keras
from keras import layers, models, activations, losses, metrics, optimizers
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import copy


save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/pass_data_full_history.csv'
# save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/temp.csv'
model = 'pass_unum_history_full_small.h5'
df = pd.read_csv(save_file_path, dtype=float)
just_test = False
# df = df[df.index < 10000]
use_hold = False
use_dribble = False
use_pass = True
df_hold = df[df['out_category'] == 0]
df_dribble = df[df['out_category'] == 1]
df_pass = df[df['out_category'] == 2]
dfs = []
if use_hold:
    dfs.append(df_hold)
if use_dribble:
    dfs.append(df_dribble)
if use_pass:
    dfs.append(df_pass)
df = pd.concat(dfs).reset_index()
del df['index']
del df_pass
del df_dribble
del df_hold
header = df.columns
header_x = []
header_y = []
for h in header:
    header_name = h.strip()
    if header_name.startswith('out_'):
        header_y.append(h)
    else:
        header_x.append(h)
        # if header_name.find('p_l_') >= 0:
        #     if header_name.find('_rx') > 0 or \
        #             header_name.find('_ry') > 0 or \
        #             header_name.find('_r') > 0 or \
        #             header_name.find('_px') > 0 or \
        #             header_name.find('_py') > 0 or \
        #             header_name.find('_dpassdist') > 0 or \
        #             header_name.find('_nearoppdist') > 0 or \
        #             header_name.find('_poscount') > 0 or \
        #             header_name.find('_velcount') > 0 or \
        #             header_name.find('_iskicker') > 0 or \
        #             header_name.find('_kicking') > 0 or \
        #             header_name.find('_player_type_effort_min') > 0 or \
        #             header_name.find('_player_type_effort_max') > 0 or \
        #             header_name.find('_player_type_margin') > 0 or \
        #             header_name.find('_tackling') > 0:
        #         header_x.append(h)
        # elif header_name.find('p_r_') >= 0:
        #     if header_name.find('_rx') > 0 or \
        #             header_name.find('_ry') > 0 or \
        #             header_name.find('_r') > 0 or \
        #             header_name.find('_px') > 0 or \
        #             header_name.find('_py') > 0 or \
        #             header_name.find('_poscount') > 0 or \
        #             header_name.find('_player_type_decay') > 0 or \
        #             header_name.find('_player_type_speed_max') > 0 or \
        #             header_name.find('_player_type_effort_min') > 0 or \
        #             header_name.find('_player_type_effort_max') > 0 or \
        #             header_name.find('_velcount') > 0:
        #         header_x.append(h)
        # elif header_name.find('ball') >= 0:
        #     if header_name.find('ballvy') > 0 or \
        #             header_name.find('bally') > 0 or \
        #             header_name.find('ballvx') > 0 or \
        #             header_name.find('ballvr') > 0:
        #         header_x.append(h)
        # elif header_name.find('drible_angle') > 0:
        #     pass
        # else:
        #     pass
header_y = ['out_unum']
# header_y = ['out_category']

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
y = df_y.to_numpy()
del df_x
del df_y

shuffle = list(range(0, x.shape[0]))
random.shuffle(shuffle)
x = x[shuffle]
y = y[shuffle]
size = x.shape[0]
train_size = 0 if just_test else int(0.95 * size)
if not just_test:
    x_train = x[:train_size]
    y_train = y[:train_size]
    y_train = to_categorical(y_train)
x_test = x[train_size:]
y_test = y[train_size:]
y_test = to_categorical(y_test)

del x
del y


def accuracy1(y_true, y_pred):
    y_true = K.cast(y_true, y_pred.dtype)
    y_true = K.argmax(y_true)
    res = K.in_top_k(y_pred, y_true, 1)
    return res


def accuracy2(y_true, y_pred):
    y_true = K.cast(y_true, y_pred.dtype)
    y_true = K.argmax(y_true)
    res = K.in_top_k(y_pred, y_true, 2)
    return res


def validation():
    network = keras.models.load_model(model, custom_objects={'accuracy1': accuracy1, 'accuracy2': accuracy2})
    # test_loss, test_acc = network.evaluate(x_test, y_test)
    for i in range(50):
        inp = np.array(x_test[i])
        inp = inp.reshape((1, x_test.shape[1],))
        max_index_col = np.argmax(y_test[i], axis=0)
        per = network.predict(inp)
        # max_index_per = np.argmax(per[0], axis=0)
        max_index_per1 = per[0].argsort()[-1]
        max_index_per2 = per[0].argsort()[-2]
        max_prob_per1 = per[0][per[0].argsort()[-1]]
        max_prob_per2 = per[0][per[0].argsort()[-2]]
        print(max_index_col, {max_index_per1: max_prob_per1, max_index_per2: max_prob_per2},
              '' if not max_index_col in [max_index_per1, max_index_per2] else 'yes')
    # print(test_loss, test_acc)


import keras.backend as K


def train():
    network = models.Sequential()
    network.add(layers.Dense(32, activation=activations.relu, input_shape=(x_train.shape[1],)))
    # network.add(layers.Dense(128, activation=activations.relu))
    # network.add(layers.Dense(64, activation=activations.relu))
    network.add(layers.Dense(32, activation=activations.relu))
    network.add(layers.Dense(y_train.shape[1], activation=activations.softmax))
    network.compile(optimizer=optimizers.adam(), loss=losses.categorical_crossentropy, metrics=[accuracy1, accuracy2])
    history = network.fit(x_train, y_train, epochs=200, batch_size=32, validation_data=(x_test, y_test))
    res = network.evaluate(x_test, y_test)
    print(res)
    history_dict = history.history
    print(history_dict)
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    # acc_values = history_dict['mean_squared_error']
    # val_acc_values = history_dict['val_mean_squared_error']
    acc1_values = history_dict['accuracy1']
    val_acc1_values = history_dict['val_accuracy1']
    acc2_values = history_dict['accuracy2']
    val_acc2_values = history_dict['val_accuracy2']

    epochs = range(len(loss_values))
    plt.figure(1)
    plt.subplot(311)
    plt.plot(epochs, loss_values, 'r--', label='Training loss')
    plt.plot(epochs, val_loss_values, 'b--', label='Validation loss')
    plt.title("train/test loss")
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.subplot(312)
    plt.plot(epochs, acc1_values, 'r--', label='Training mean_squared_error')
    plt.plot(epochs, val_acc1_values, '--', label='Validation mean_squared_error')
    plt.title("train/test acc")
    plt.xlabel('Epochs')
    plt.ylabel('Acc')
    plt.legend()
    plt.subplot(313)
    plt.plot(epochs, acc2_values, 'r--', label='Training mean_squared_error')
    plt.plot(epochs, val_acc2_values, '--', label='Validation mean_squared_error')
    plt.title("train/test acc2")
    plt.xlabel('Epochs')
    plt.ylabel('Acc2')
    plt.legend()
    plt.show()
    network.save(model)


if not just_test:
    train()
validation()
