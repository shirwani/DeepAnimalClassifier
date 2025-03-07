import json
import numpy as np
import h5py
from datetime import datetime
from PIL import Image
import os
import glob


def get_probs_for_all_classes(probabilities, classes):
    probabilities = probabilities[0, :]
    probs = dict()
    for i in range(len(probabilities)):
        animal = classes[i]
        prob = int(probabilities[i] * 10000)/100
        probs[animal] = prob

    probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    p = dict()
    for t in probs:
        p[t[0]] = str(t[1]) + '%'

    return p


def get_jpeg_files(folder_path):
    return glob.glob(os.path.join(folder_path, '*.jpeg'), recursive=False)


def get_configs(dev=False):
    with open('config.json', 'r') as f:
        full_cfg = json.load(f)

    if dev:
        cfg = full_cfg['dev']
    else:
        cfg = full_cfg['prod']

    return cfg


def get_date_time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def img_to_matrix(img_file_path, num_px):

    print(img_file_path)

    image = Image.open(img_file_path)
    resized_image = image.resize((num_px, num_px))
    image_array = np.array(resized_image).reshape(num_px, num_px, 3)
    return image_array


def load_data(data_file):
    dataset = h5py.File(data_file, "r")
    x = np.array(dataset["x"][:])
    y = np.array(dataset["y"][:])
    print("x.shape: " + str(x.shape))
    print("y.shape: " + str(y.shape))
    print("y: " + str(y))
    return x, y

