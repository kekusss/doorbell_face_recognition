
from flask import Flask, render_template, Response, request
from doorbell_camera import DoorbellCamera
# import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        return render_template('index.html', res_str=result)
                        
    return render_template('index.html')


def generate_frame(doorbell_camera):
    while True:
        frame = doorbell_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/camera')
def camera():
    return Response(generate_frame(DoorbellCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999, debug=False, threaded=True)
