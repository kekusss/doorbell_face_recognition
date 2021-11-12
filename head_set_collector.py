import cv2
import sys

if len(sys.argv) != 2:
    print("You should enter person name. \n Exiting.")
    exit()

face_name = sys.argv[1]

camera = cv2.VideoCapture(0)
camera.set(3, 640) # video width
camera.set(4, 480) # video height

face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

count = photos = 0

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
            cv2.imwrite("Users/User_" + str(face_name) + '_' + str(photos) + ".jpg", gray[y:y+h, x:x+w])


        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif photos >= 10: # Take 10 face sample and stop video
         break
        
camera.release()
cv2.destroyAllWindows()