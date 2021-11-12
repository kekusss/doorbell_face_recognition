import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'Users'
recognizer = cv2.face_LBPHFaceRecognizer.create()
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    names = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        name = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            names.append(name)

    return faceSamples ,names


print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,names = getImagesAndLabels(path)
recognizer.train(faces, np.array(names))

# Save the model into trainer/trainer.yml
recognizer.write('Trainer/trainer.yml')

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(names))))