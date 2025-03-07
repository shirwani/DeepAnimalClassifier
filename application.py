from utils import *
from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
from PIL import Image
from io import BytesIO
import json
import sys
import tensorflow as tf
from keras.models import load_model


dev = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-dev' or sys.argv[1] == '--dev':
        dev = True

cfg = get_configs(dev)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run():
    model               = cfg['model']['file']
    icon_img            = cfg['flask-app']['icon_img']
    default_img_url     = cfg['flask-app']['default_img_url']
    test_images_folder  = cfg['flask-app']['test_images_folder']
    proj_location       = cfg['flask-app']['proj_location']

    test_images = get_jpeg_files(test_images_folder)

    return render_template("getUserInput.html",
                           default_img_url=default_img_url,
                           icon_img=icon_img,
                           model=model,
                           test_images=test_images,
                           proj_location=proj_location)

############
# Get result
############
@app.route('/result', methods=['GET', 'POST'])
def identify():
    model   = cfg['model']['file']
    num_px  = cfg['image']['num_px']
    classes = cfg['classes']

    img_url = request.json
    print(img_url)

    try:
        img_data = requests.get(img_url).content
    except:
        print("BAD_URL: " + img_url)
        return render_template("imageError.html")

    image = img_to_matrix(BytesIO(img_data), num_px)
    print(f"image.shape: {image.shape}")
    image = image.reshape((1, -1)) / 255.
    print(f"image.shape: {image.shape}")

    model = load_model(os.path.join(os.getcwd(), 'models', model))
    logits = model.predict(image)  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities
    prediction = np.argmax(probabilities)  # predicted value with largest probability
    confidence = str(int(probabilities[0, prediction] * 10000) / 100)
    obj = classes[int(np.squeeze(prediction))]

    probs = get_probs_for_all_classes(probabilities, classes)

    print(f"probabilities: {probabilities}")
    print(f"prediction: {prediction}")
    print(f"confidence: {confidence}%")
    print(f"obj: {obj}")

    return render_template("showResult.html",
                           prediction=prediction,
                           obj=obj,
                           confidence=confidence,
                           img_url=img_url,
                           probabilities=probs)


if __name__ == '__main__':
    port = cfg['flask-app']['port']
    app.run(debug=True, port=port)
