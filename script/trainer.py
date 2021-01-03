import pandas as pd
import numpy as np
import random
# import keras
import tensorflow.keras as keras

# from keras import layers, models, activations, losses, metrics, optimizers
# from keras.utils import to_categorical
import matplotlib.pyplot as plt
import copy
import re
import time
import os, psutil


# save_file_path = '/home/nader/data/robo_data/fwm_fwm_unum_all_cl4/pass/pass_100.csv'
save_file_path = '/home/nader/data/fwm_fwm_unum/from_i/from_9_200000.csv'
# save_file_path = '/home/nader/data/robo_data/wm_fwm_x_pass_cl1/test.csv'
# save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/temp.csv'
model = 'pass_unum_history_full_small.h5'
df = pd.read_csv(save_file_path, dtype=float)
df.dropna(inplace=True)
print('file was read', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
just_test = False
# df = df[df.index < 10000]
# use_hold = False
# use_dribble = False
# use_pass = True
# df_hold = df[df['out_category'] == 0]
# df_dribble = df[df['out_category'] == 1]
# df_pass = df[df['out_category'] == 2]
# dfs = []
# if use_hold:
#     dfs.append(df_hold)
# if use_dribble:
#     dfs.append(df_dribble)
# if use_pass:
#     dfs.append(df_pass)
# df = pd.concat(dfs).reset_index()
try:
    del df['index']
except:
    pass
print('index was removed', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
# del df_pass
# del df_dribble
# del df_hold
# df = df[df['out_unum'] <= 8]
# df = df[df['out_unum'] > 5]
header = df.columns
header_x = []
header_y = []

# good_f = []
# f = open('DataAnalysisPath/feature_import/f_f_pass_unum_history_full_l4_randomf_new_5.csv', 'r')
# all_f = []
# for l in f.readlines():
#     k = l.split(',')[0]
#     w = float(l.split(',')[1])
#     all_f.append((k, w))
# all_f.sort(key=lambda a: a[1], reverse=True)
# for f in all_f[:]:
#     good_f.append(f[0])
for h in header:
    header_name = h.strip()
    if header_name.startswith('out_'):
        header_y.append(h)
    else:
        # if h in good_f:
        header_x.append(h)
print(len(header_x))
print(header_x)
print(header_y)
header_y = ['out_unum_index']
# header_y = ['out_category']

for h in copy.copy(header_x):
    if h.find('history') >= 0:
        header_x.remove(h)
        continue
    if h.find('Unnamed') >= 0:
        header_x.remove(h)
        continue
    # if not re.search('(_pos_[xy]$)|(is_kicker)', h):
    # if not re.search('(goal_center)|(pass)|(is_kicker)', h):
    # if h.find('_pos_') == -1:
    #     header_x.remove(h)
    #     continue
# print(header_x)
# exit()
df_x = df[header_x]
print('df x', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
df_y = df[header_y]
print('df y', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
del df
print('delete df', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
try:
    del df_x['Unnamed: 0']
    del df_x['Unnamed: 0.1']
except:
    pass
print(df_x.shape)
x = df_x.to_numpy()
print('x', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
del df_x
y = df_y.to_numpy()
print('y', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
del df_y

shuffle = list(range(0, x.shape[0]))
random.shuffle(shuffle)
x = x[shuffle]
print('shuffle x', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
y = y[shuffle]
print('shuffle y', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
print(y)
print(max(y))
print(min(y))
print(np.unique(y))
y = keras.utils.to_categorical(y, num_classes=13)
size = x.shape[0]
train_size = 0 if just_test else int(0.90 * size)
if not just_test:
    x_train = x[:train_size]
    y_train = y[:train_size]
    print('xtrain ytrain', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
x_test = x[train_size:]
y_test = y[train_size:]

del x
del y
print('del x y', psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

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


def valid_unum():
    network = keras.models.load_model(model, custom_objects={'accuracy1': accuracy1, 'accuracy2': accuracy2})
    y = network.predict(x_test)
    res = {i: [0, 0] for i in range(12)}
    count = 0
    for i in range(len(y_test)):
        count += 1
        res[y_test[i].argsort()[-1]][0] += 1
        if y_test[i].argsort()[-1] == y[i].argsort()[-1]:
            res[y_test[i].argsort()[-1]][1] += 1
    for k in res:
        print(k, res[k], res[k][0] / count * 100, res[k][1] / res[k][0] * 100 if res[k][0] > 0 else 0)

def valid():
    network = keras.models.load_model(model, custom_objects={'accuracy1': accuracy1, 'accuracy2': accuracy2})
    a = network.evaluate(x_test, y_test)
    print(a)
import keras.backend as K


def train():
    network = keras.models.Sequential()
    network.add(keras.layers.Dense(1024, activation=keras.activations.sigmoid, input_shape=(x_train.shape[1],)))
    network.add(keras.layers.Dropout(0.1))
    network.add(keras.layers.Dense(512, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(256, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(64, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(32, activation=keras.activations.sigmoid))
    network.add(keras.layers.Dense(y_train.shape[1], activation=keras.activations.softmax))
    network.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=[accuracy1, accuracy2])
    print(x_train.shape)
    xx = time.time()
    history = network.fit(x_train, y_train, epochs=100, batch_size=1024, validation_data=(x_test, y_test))
    yy = time.time()
    print('fit', yy - xx)
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
# validation()
# valid()
valid_unum()