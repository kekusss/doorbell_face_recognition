
from flask import Flask, render_template, Response
from flask import jsonify
from doorbell_camera import DoorbellCamera
from action_listener import ActionListener
import imutils
from imutils.video import VideoStream
import threading
import time
import cv2
import datetime

app = Flask(__name__)

outputFrame = None
lock = threading.Lock()
stream = VideoStream(src=0).start()
time.sleep(2.0)

def listen():
    action_listener = ActionListener()
    action_listener.listen()

def recognize_face():
    frameCount = 30
    # grab global references to the video stream, output frame, and lock variables
    global stream, outputFrame, lock
    
    doorbell_camera = DoorbellCamera()
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = stream.read()
        frame = imutils.resize(frame, width=1024)
        
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        if total > frameCount:
            # detect face in the image
            doorbell_camera.recognize(frame)
        
        total += 1

        # acquire the lock, set the output frame, and release the lock
        with lock:
            outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():    
    return render_template('index.html')

@app.route("/snapshot")
def snapshot():
    global stream
    frame = stream.read()
    ts = int(time.time())
    fileName = str(ts) + '.jpg'

    cv2.imwrite('/home/pi/Pictures/Doorbell/' + fileName, frame)
    data = {'name': fileName}
    return jsonify(data), 200

@app.route("/camera")
def camera():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    # start a thread that will perform face recognition
    t = threading.Thread(target=recognize_face)
    t.daemon = True
    t.start()

    # start a thread that will listen for physical button pressed
    tl = threading.Thread(target=listen)
    tl.daemon = True
    tl.start()

    # start the flask app
    app.run(host='0.0.0.0', port=8999, debug=False, threaded=True, use_reloader=False)

# release the video stream pointer
stream.stop()
