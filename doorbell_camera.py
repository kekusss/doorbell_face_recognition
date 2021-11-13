import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

class DoorbellCamera(object):

    def getNames(self):
        path = 'Users'
        names = []
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

        for imagePath in imagePaths:
            id_and_name = os.path.split(imagePath)[-1].split("_")[1]
            names.append(id_and_name.split("-")[1])

        return names

    def __init__(self):
        self.video = cv2.VideoCapture(0)

        self.video.set(3, 640) # video widht
        self.video.set(4, 480) # video height

        # Define min window size to be recognized as a face
        self.minW = 0.1*self.video.get(3)
        self.minH = 0.1*self.video.get(4)

        self.names = self.getNames()
    
    def __del__(self):
        self.video.release()

    
    def get_frame(self):
        success, image = self.video.read()
        process_this_frame = True

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if process_this_frame:
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(self.minW), int(self.minH)),
            )

            for(x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    name = self.names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    name = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(image, str(name), (x+5,y-5), font, 1, (255, 0, 255), 2)
                cv2.putText(image, str(confidence), (x+5,y+h-5), font, 1, (255, 255, 0), 1)

        process_this_frame = not process_this_frame

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()