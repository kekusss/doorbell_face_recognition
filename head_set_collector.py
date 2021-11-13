import cv2
import sys
import os

if len(sys.argv) != 2:
    print("You should enter person name. \n Exiting.")
    exit()

face_name = sys.argv[1]

camera = cv2.VideoCapture(0)
camera.set(3, 640) # video width
camera.set(4, 480) # video height

face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

count = photos = 0

def getNewID():
    path = 'Users'
    highest_id = 0
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

    for imagePath in imagePaths:
        id_and_name = os.path.split(imagePath)[-1].split("_")[1]
        current_id = int(id_and_name.split("-")[0])

        if highest_id < current_id:
            highest_id = current_id


    return highest_id + 1

id = getNewID()

while(True):
    ret, img = camera.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,     
        scaleFactor=1.3,
        minNeighbors=7,     
        minSize=(20, 20)
    )

    for (x,y,w,h) in faces:
        count += 1
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        
        if count % 10 == 0:
            photos += 1
            cv2.imwrite("Users/User_" + str(id) + "-" + str(face_name) + '_' + str(photos) + ".jpg", gray[y:y+h, x:x+w])
            # todo turn on red light


        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif photos >= 10: # Take 10 face sample and stop video
         break
        
camera.release()
cv2.destroyAllWindows()
#todo turn on green light for 5 secs