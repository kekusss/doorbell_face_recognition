import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
# cascadePath = "Cascades/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

def getNames():
    path = 'Users'
    names = {}
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

    for imagePath in imagePaths:
        id_and_name = os.path.split(imagePath)[-1].split("_")[1]
        if not names.get(id_and_name.split("-")[0]):
            names.update({id_and_name.split("-")[0]: id_and_name.split("-")[1]})

    return names

#iniciate id counter
id = 0

names = getNames()

# Initialize and start realtime video capture
camera = cv2.VideoCapture(0)
camera.set(3, 1024) # video widht
camera.set(4, 768) # video height

# Define min window size to be recognized as a face
minW = 0.1*camera.get(3)
minH = 0.1*camera.get(4)

while True:
    ret, img = camera.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            name = names.get(str(id))
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(name), (x+5,y-5), font, 1, (255, 0, 255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255, 255, 0), 1)  
    
    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    

camera.release()
cv2.destroyAllWindows()
