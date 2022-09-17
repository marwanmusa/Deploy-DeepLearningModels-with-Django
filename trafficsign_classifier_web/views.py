from django.shortcuts import render
from django.core.files.storage import default_storage

# our home page view
def home(request):
    return render(request, 'index.html')


# custom method for generating predictions
def getPredictions(file_url):
     # Fundamental classes
        import numpy as np 
        import pandas as pd 
        import tensorflow
        import os

        # Image related
        import cv2
        from PIL import Image
        import pydot

        # For ploting
        import matplotlib.pyplot as plt

        # For the model and it's training
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split
        from tensorflow import keras
        from tensorflow.keras.utils import to_categorical, plot_model
        from tensorflow.keras.models import Sequential, load_model
        from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout

        # predicting with docker API
        import requests
        import json
        from tensorflow.python.ops.numpy_ops import np_config
        np_config.enable_numpy_behavior()
        #
        # Django image API
        #

        #
        # classes
        # Dictionary of each class
        classes = { 0:'Speed limit (20km/h)',
                    1:'Speed limit (30km/h)', 
                    2:'Speed limit (50km/h)', 
                    3:'Speed limit (60km/h)', 
                    4:'Speed limit (70km/h)', 
                    5:'Speed limit (80km/h)', 
                    6:'End of speed limit (80km/h)', 
                    7:'Speed limit (100km/h)', 
                    8:'Speed limit (120km/h)', 
                    9:'No passing', 
                    10:'No passing veh over 3.5 tons', 
                    11:'Right-of-way at intersection', 
                    12:'Priority road', 
                    13:'Yield', 
                    14:'Stop', 
                    15:'No vehicles', 
                    16:'Veh > 3.5 tons prohibited', 
                    17:'No entry', 
                    18:'General caution', 
                    19:'Dangerous curve left', 
                    20:'Dangerous curve right', 
                    21:'Double curve', 
                    22:'Bumpy road', 
                    23:'Slippery road', 
                    24:'Road narrows on the right', 
                    25:'Road work', 
                    26:'Traffic signals', 
                    27:'Pedestrians', 
                    28:'Children crossing', 
                    29:'Bicycles crossing', 
                    30:'Beware of ice/snow',
                    31:'Wild animals crossing', 
                    32:'End speed + passing limits', 
                    33:'Turn right ahead', 
                    34:'Turn left ahead', 
                    35:'Ahead only', 
                    36:'Go straight or right', 
                    37:'Go straight or left', 
                    38:'Keep right', 
                    39:'Keep left', 
                    40:'Roundabout mandatory', 
                    41:'End of no passing', 
                    42:'End no passing veh > 3.5 tons' }
        # loading
        img = keras.preprocessing.image.load_img(file_url, target_size=([30, 30]))

        # Processing
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tensorflow.expand_dims(img_array, 0)

        # json input
        input_data_json_img = json.dumps({
            "signature_name": "serving_default",
            "instances": img_array.tolist(),
        })

        # predicting
        URL = 'http://localhost:8501/v1/models/traffic_classifier:predict' # Rest API TensorFlow Serving with Docker
        response_img = requests.post(URL, data=input_data_json_img)
        response_img.raise_for_status() # raise an exception in case of error
        response_img = response_img.json()

        # predicting result
        score = tensorflow.nn.softmax(response_img['predictions'][0])
        destination_by_img = classes[np.argmax(score)]
        hbc = "This image most likely belongs to {}.".format(destination_by_img)
        PathImage = "/trafficsign_classifier_web/{}.png".format(np.argmax(score))

        return hbc, PathImage

def result(request):
    if request.method == "POST":

        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        Inputimg = "/media/{}".format(file_name)

        result, Pathimg = getPredictions(file_url)
        print(result)
        context ={
            'result' : result,
            'pathimg' : Pathimg,
            'tempfile' : Inputimg
        }
        return render(request, 'result.html', context)
    else:
        return render(request, "index.html")