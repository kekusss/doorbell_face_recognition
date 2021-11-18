import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'Users'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")
# detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_alt2.xml")

# function to get the images and label data
def getDataSet(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id_and_name = os.path.split(imagePath)[-1].split("_")[1]
        id = int(id_and_name.split("-")[0])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples, ids


print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids = getDataSet(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('Trainer/trainer.yml')

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))