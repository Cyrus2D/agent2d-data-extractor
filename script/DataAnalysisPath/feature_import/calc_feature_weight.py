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

use_binary = False

features_number = 783
dataset = numpy.loadtxt('/home/nader/data/robo_data/test_pass.csv', delimiter=",")
print(dataset.shape)
X = dataset[:, 0:features_number]
Y = dataset[:, 783]

if use_binary:
    for y in range(len(Y)):
        if Y[y] == 1:
            Y[y] = 0
        elif Y[y] == 2:
            Y[y]=1
else:
    Y = to_categorical(Y)


def create_model():
    model = Sequential()
    model.add(Dense(100, input_dim=features_number, activation='relu'))
    model.add(Dense(25, activation='relu'))
    if use_binary:
        model.add(Dense(1, activation='sigmoid'))
    else:
        model.add(Dense(Y.shape[1], activation='sigmoid'))
        model.add(Dense(Y.shape[1], activation=activations.softmax))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


create_model()
head = open('/home/nader/workspace/robo/cyrus/script/DataAnalysisPath/feature_import/head').readlines()[0][:-2].split(',')[:features_number]
# create model
train_epoch_number = 20
model = KerasClassifier(build_fn=create_model, epochs=train_epoch_number, batch_size=10, verbose=1)

# if use_new_model:
model.fit(X, Y)
perm = PermutationImportance(model, random_state=1).fit(X,Y)

a = eli5.explain_weights(perm, feature_names=head, top=features_number)
fi = a.feature_importances.importances
nnfeatures = open('feature_import/nn_out_desc.csv', 'w')
for f in fi:
    nnfeatures.write(f.feature + ',' + str(f.weight) + '\n')
    print(f.feature, f.weight, f.std, f.value)
print(len(fi))
