import cv2
import os
import subprocess

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

class DoorbellCamera(object):

    def getNames(self):
        path = 'Users'
        names = {}
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

        for imagePath in imagePaths:
            id_and_name = os.path.split(imagePath)[-1].split("_")[1]
            if not names.get(id_and_name.split("-")[0]):
                names.update({id_and_name.split("-")[0]: id_and_name.split("-")[1]})

        return names

    def __init__(self):

        # Define min window size to be recognized as a face
        self.minW = 200
        self.minH = 200

        self.names = self.getNames()
    
    def recognize(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(self.minW), int(self.minH)),
        )

        for(x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            confidence = round(100 - confidence)

            if(confidence > 30):
                command1 = subprocess.Popen(['./open.sh'])

            if (confidence > 30):
                name = self.names[str(id)]
                confidence = "  {0}%".format(confidence)
            else:
                name = "unknown"
                confidence = "  {0}%".format(confidence)
            
            cv2.putText(image, str(name), (x+5,y-5), font, 1, (255, 0, 255), 2)
            cv2.putText(image, str(confidence), (x+5,y+h-5), font, 1, (255, 255, 0), 1)