from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from os import listdir
from os.path import isdir
from PIL import Image
from numpy import asarray, savez_compressed
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import cv2
from tensorflow.keras.models import load_model
import numpy as np

from numpy import load
from numpy import expand_dims
from numpy import asarray
from numpy import savez_compressed
from keras.models import load_model
from keras.preprocessing.image import load_img



def extract_face(filename, required_size=(160, 160)):
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = asarray(image)
    try:
        detector = MTCNN()
        results = detector.detect_faces(pixels)
        x1, y1, width, height = results[0]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array
    except Exception as e:
        return e


def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]


def compare(path):
    face = extract_face(path)
    model = load_model('/home/ashok/PycharmProjects/face/mysite/facenet.h5')
    y = get_embedding(model, face)
    m = 10 ** 5
    xyz = []
    x=Criminal.objects.all()
    for i in x:
        if i.name=="temp":
            continue
        pixels=np.array(list(map(float,i.embedding.split(','))))
        temp=np.sum(np.abs(y-pixels))
        if temp<m:
            j=i
            m=temp
    if m<=70:
        return j
    return "Not found"




def index(request):
    if request.method=="POST":
        file=request.FILES['photo']
        temp=Criminal.objects.get(name="temp")
        temp.photo=file
        temp.save()
        temp=Criminal.objects.get(name="temp")
        path='/home/ashok/PycharmProjects/face/mysite/media/'+str(temp.photo)
        x=compare(path)
        return render(request,'test.html',{"x":x})

    return render(request,'test.html',{})


def add(request):
    if request.method=='POST':
        file=request.FILES['photo']
        #file.save(file.filename)
        #return HttpResponse(" ".join(dir(file)))
        name=request.POST['name']
        city = request.POST['city']
        crime = request.POST['crime']
        c=Criminal(name=name,city=city,crime=crime,photo=file)
        c.save()
        id=c.id
        c=Criminal.objects.get(id=id)
        pixels = extract_face('/home/ashok/PycharmProjects/face/mysite/media/'+str(c.photo))
        model = load_model('/home/ashok/PycharmProjects/face/mysite/facenet.h5')
        temp=get_embedding(model,pixels)
        c.embedding=",".join(map(str,temp))
        c.save()
    return render(request,'add.html',{})

def all(request):
    y=Criminal.objects.all()
    x=[]
    for i in y:
        if i.name!="temp":
            #i.photo="/home/ashok/PycharmProjects/face/mysite/"+str(i.photo)
            x.append(i)
    return render(request,'all.html',{'x':x})

