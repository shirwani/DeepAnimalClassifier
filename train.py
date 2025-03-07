import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from utils import *
import sys


def train_model(cfg):
    print("Initiating training...")
    data_file     = cfg['train']['data_file']
    learning_rate = cfg['train']['learning_rate']
    regularizer   = cfg['train']['regularizer']
    epochs        = cfg['train']['epochs']
    num_px        = cfg['image']['num_px']
    classes       = cfg['classes']

    X, y = load_data(data_file)

    X = X.reshape(X.shape[0], -1) / 255.
    y = np.reshape(y, (y.shape[0], 1))

    print('The shape of X is: ' + str(X.shape))
    print('The shape of y is: ' + str(y.shape))


    tf.random.set_seed(1234)  # for consistent results
    model = Sequential(
        [
            tf.keras.Input(shape=(num_px * num_px * 3,)),
            Dense(1000,         activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(regularizer)),
            Dense(500,          activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(regularizer)),
            Dense(100,          activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(regularizer)),
            Dense(len(classes), activation='linear', kernel_regularizer=tf.keras.regularizers.l2(regularizer))
        ])

    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # softmax: multi-class classification
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate)
    )

    model.fit(X, y, epochs=epochs)

    print(model)


    # Save the model
    modelname = 'm_' + get_date_time_str() + '.keras'
    model.save(os.path.join(os.getcwd(), 'models', modelname))


if __name__ == '__main__':
    dev = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '-dev' or sys.argv[1] == '--dev':
            dev = True

    train_model(get_configs(dev))

