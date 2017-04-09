#!/usr/bin/python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, os
import numpy as np
# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('mod')
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
from socketIO_client import SocketIO, LoggingNamespace

with SocketIO('localhost', 8080, LoggingNamespace) as socketIO:
    while True:
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        bwimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(bwimage, 1.3, 5, minSize=(80, 80))
        output = []
        for (x, y, w, h) in faces:
            predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
            print "face {} guessed with confidence {}".format(predicted,conf)
            output.append({"id":predict,"conf":conf})
        
        socketIO.emit('faces',output)
