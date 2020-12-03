from keras import layers, models, activations, losses, metrics, optimizers
# MLP for Pima Indians Dataset with 10-fold cross validation via sklearn
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import numpy
from sklearn.model_selection import GridSearchCV
from eli5.sklearn import PermutationImportance
import eli5
from keras.utils import to_categorical
import keras.backend as K
import pandas as pd
import random
import copy


save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/pass_data_full_history.csv'
# save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/temp.csv'
model = 'pass_unum_history_full.h5'
df = pd.read_csv(save_file_path, dtype=float)
df = df[df['out_category'] == 2]
# df = df[df.index < 1000]
df.reset_index()
# del df['index']
header = df.columns
header_x = []
header_y = []
for h in header:
    header_name = h.strip()
    if header_name.startswith('out_'):
        header_y.append(h)
    else:
        header_x.append(h)
header_y = ['out_unum']

for h in copy.copy(header_x):
    # if h.find('history') >= 0:
    #     header_x.remove(h)
    #     continue
    # elif h.find('pos_x') == -1 and h.find('pos_y') == -1:
    #     header_x.remove(h)
    #     continue
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


use_binary = False
features_number = len(header_x)

# if use_binary:
#     for y in range(len(Y)):
#         if Y[y] == 1:
#             Y[y] = 0
#         elif Y[y] == 2:
#             Y[y]=1
# else:
size = x.shape[0]
train_size = int(0.95 * size)
x_train = x[:train_size]
y_train = y[:train_size]
y_train = to_categorical(y_train)
x_test = x[train_size:]
y_test = y[train_size:]
y_test = to_categorical(y_test)

def create_model():
    model = Sequential()
    model.add(Dense(64, input_dim=features_number, activation='relu'))
    model.add(Dense(32, activation='relu'))
    if use_binary:
        model.add(Dense(1, activation='sigmoid'))
    else:
        model.add(Dense(y_train.shape[1], activation=activations.softmax))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


create_model()
head = header_x
# create model
train_epoch_number = 20
model = KerasClassifier(build_fn=create_model, epochs=train_epoch_number, batch_size=10, verbose=1)

# if use_new_model:
model.fit(x_train, y_train)


# perm = PermutationImportance(model, random_state=1).fit(x_test,y_test)
perm = PermutationImportance(model, random_state=1).fit(x_train[:size - train_size],y_train[:size - train_size])

a = eli5.explain_weights(perm, feature_names=head, top=len(header_x))
fi = a.feature_importances.importances
nnfeatures = open('nn_out_desc3.csv', 'w')
for f in fi:
    nnfeatures.write(f.feature + ',' + str(f.weight) + '\n')
    print(f.feature, f.weight, f.std, f.value)
nnfeatures.close()
print(len(fi))
