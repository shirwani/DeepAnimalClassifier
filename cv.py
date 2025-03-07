from utils import *
import os
import sys
import tensorflow as tf
from keras.models import load_model


def cross_validation(cfg):
    print("Initiating cross-validation")
    data_file = cfg['cv']['data_file']
    model = cfg['model']['file']

    print(f"Model: {model}")

    dataset = h5py.File(data_file, "r")
    X = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])

    X = X.reshape(X.shape[0], -1) / 255.
    y = np.reshape(y, (y.shape[0], 1))

    model = load_model(os.path.join(os.getcwd(), 'models', model))

    logits = model.predict(X)  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    i = 0
    misses = 0
    for p in probabilities:
        yhat = np.argmax(p)
        if y[i][0] != yhat:
            misses += 1
            print(f" Expected: {y[i][0]} -- Predicted: {yhat} -- Confidence: {int(p[yhat] * 10000) / 100}%")

        i += 1

    accuracy = round((i - misses)/i * 10000)/100
    print(f"Accuracy: {accuracy}")


if __name__ == '__main__':
    dev = True
    if len(sys.argv) > 1:
        if sys.argv[1] == '-dev' or sys.argv[1] == '--dev':
            dev = True

    cross_validation(get_configs(dev))
