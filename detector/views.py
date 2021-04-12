from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ImageForm
from django.core.files.storage import FileSystemStorage
from .models import ImageUploader
import mysite.settings as settings
import os
import base64
import glob
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

# Create your views here.
img_path = "Hello"
def image_post(request): 
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 
        if form.is_valid():  
            file_upload_dir = os.path.join(settings.MEDIA_ROOT)
            # for removing the files in the upload directory
            if os.path.exists(file_upload_dir):
                import shutil
                shutil.rmtree(file_upload_dir)
            image = request.FILES['image']
            context = {}
            fs = FileSystemStorage()
            name = fs.save(image.name,image)
            path = fs.path(name)
            
            im = Image.open(path)
            im.save('media/new_image.png')
        
            context['url'] = fs.url(name)
            context['prediction'] = class_predictor()
            tf.keras.backend.clear_session()
            return render(request,'home.html', context)
    else:
        form = ImageForm() 
    return render(request, 'home.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse("Succefully uploaded")

# processing the input image


# Dictionary for mapping labels to names of classes
dictionary = {0: 'Baby Potato', 1: 'Beetroot', 2: 'Bitter gourd',
     3: 'Bottle gourd', 4: 'Brocolli', 5: 'Cabbage',
     6: 'Capsicum-Green', 7: 'Capsicum-Red',
     8: 'Capsicum-Yellow', 9: 'Cauliflower',
     10: 'Garlic', 11: 'Ladies finger', 12: 'Mushroom-button',
     13: 'Onion', 14: 'Onion-Sambhar', 15: 'Potato', 16: 'Spring Onion',
     17: 'Sweet Potato', 18: 'Zucchini-Green', 19: 'Lemon'}

# Determining the base directory of the classifier model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR,'classifier_model.h5')
model = tf.keras.models.load_model(model_path)

# Class Prediction
def class_predictor():
    image_path = 'media/' + os.listdir('media')[1]
    path = os.path.join(BASE_DIR,image_path) 
    image = plt.imread(path)
    resized_image = tf.image.resize(tf.constant(image),(256,256))
    probabilities = model.predict(np.reshape(resized_image,(1,256,256,3)))
    out = (-probabilities).argsort()[:1]
    prediction = dictionary[out[0][0]]
    print(out)
    print(prediction)
    return prediction