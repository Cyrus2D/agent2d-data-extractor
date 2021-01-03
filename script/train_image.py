import numpy as np
import tensorflow.keras as keras
import tensorflow as tf
import matplotlib.pyplot as plt
x = np.load('/home/nader/data/fwm_fwm_unum/from_i_image/from_9_img.npy')
# x = x.reshape((15406, 50, 50, 3))
# x = x[:10000]
y = np.load('/home/nader/data/fwm_fwm_unum/from_i_image/from_9_label.npy')
# y = y[:10000]
print(x.shape)
size = y.shape[0]

x_train = x[:int(size * 0.9)]
print(x_train.shape)
y_train = y[:int(size * 0.9)]
x_test = x[int(size * 0.9):]
y_test = y[int(size * 0.9):]
del x
del y
y_train = keras.utils.to_categorical(y_train, num_classes=12)
y_test = keras.utils.to_categorical(y_test, num_classes=12)

network = keras.models.Sequential()
network.add(keras.layers.Conv2D(4, (2, 2), activation=keras.activations.relu, input_shape=(50, 50, 3), padding='SAME'))
network.add(keras.layers.Conv2D(4, (2, 2), activation=keras.activations.relu, padding='SAME'))
network.add(keras.layers.MaxPooling2D((2, 2)))
network.add(keras.layers.Dropout(0.1))
network.add(keras.layers.Conv2D(8, (2, 2), activation=keras.activations.relu, padding='SAME'))
network.add(keras.layers.Conv2D(8, (2, 2), activation=keras.activations.relu, padding='SAME'))
network.add(keras.layers.MaxPooling2D((2, 2)))
network.add(keras.layers.Dropout(0.1))
network.add(keras.layers.Conv2D(16, (2, 2), activation=keras.activations.relu, padding='SAME'))
network.add(keras.layers.Conv2D(16, (2, 2), activation=keras.activations.relu, padding='SAME'))
network.add(keras.layers.MaxPooling2D((2, 2)))
network.add(keras.layers.Dropout(0.1))
network.add(keras.layers.Flatten())
network.add(keras.layers.Dropout(0.1))
network.add(keras.layers.Dense(128, activation='relu'))
network.add(keras.layers.Dropout(0.1))
network.add(keras.layers.Dense(32, activation='relu'))
network.add(keras.layers.Dense(y_train.shape[1], activation=keras.activations.softmax))
network.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics='accuracy')
print(network.summary())
history = network.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))
print(history)

history_dict = history.history
print(history_dict)
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
# acc_values = history_dict['mean_squared_error']
# val_acc_values = history_dict['val_mean_squared_error']
acc1_values = history_dict['accuracy']
val_acc1_values = history_dict['val_accuracy']

epochs = range(len(loss_values))
plt.figure(1)
plt.subplot(211)
plt.plot(epochs, loss_values, 'r--', label='Training loss')
plt.plot(epochs, val_loss_values, 'b--', label='Validation loss')
plt.title("train/test loss")
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.subplot(212)
plt.plot(epochs, acc1_values, 'r--', label='Training mean_squared_error')
plt.plot(epochs, val_acc1_values, '--', label='Validation mean_squared_error')
plt.title("train/test acc")
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()
plt.show()


