#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image
import re
# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.createLBPHFaceRecognizer()
base = "photos"
# images will contains face images
images = []
# labels will contains the label that is assigned to the image
labels = []
imageFiles = []
for person in os.listdir('photos'):
    for image in [f for f in os.listdir('photos/'+person) if re.match(r'[0-9]+.*\.jpg', f)][1:]:
        print image
        imageFiles.append({
            "name":int(person),
            "file":person+"/"+image
        })

for imageFile in imageFiles:
    img = cv2.imread(base+"/"+imageFile['file'])
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert the image format into numpy array
    faces = faceCascade.detectMultiScale(image, 1.3, 5, minSize=(80, 80))
    print "{} faces in {}".format(len(faces),imageFile['file'])
    for (x, y, w, h) in faces:
        images.append(image[y: y + h, x: x + w])
        labels.append(imageFile['name'])
cv2.destroyAllWindows()

# Perform the tranining
recognizer.train(images, np.array(labels))
recognizer.save("mod")
predict_image_pil = Image.open(base+"/5/2.jpg").convert('L')
predict_image = np.array(predict_image_pil, 'uint8')
faces = faceCascade.detectMultiScale(predict_image, 1.3, 5, minSize=(80, 80))
print "{} faces".format(len(faces))
for (x, y, w, h) in faces:
    nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
    print "Recognized as {}".format(nbr_predicted)
    print "{} confg".format(conf)
    cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
    cv2.waitKey(1000)
input()
cv2.destroyAllWindows()
