# linear regression feature importance
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot

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


save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/wm_fwm_x_pass_cl1/new_pas_0.csv'
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

# define dataset
# define the model
model = RandomForestClassifier(max_depth=50)
# fit the model
model.fit(x_train, y_train)
# get importance
importance = model.feature_importances_
# summarize feature importance
print(importance)
f = open('randomf.csv', 'w')
for i, v in enumerate(importance):
    print(header_x[i], 'Score: %.5f' % (v))
    f.write(header_x[i] + ',' + str(v) + '\n')

# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()
y = model.predict(x_test)
from sklearn.metrics import accuracy_score
ac = accuracy_score(y_test, y)
print(ac)