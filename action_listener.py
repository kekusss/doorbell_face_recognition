import RPi.GPIO as GPIO
import time
from api_controller import ApiController


class ActionListener(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(12, GPIO.OUT)
        self.p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
        self.api_controller = ApiController()

    def listen(self):
        self.p.start(0)

        try:
            while 1:
                input_state = GPIO.input(18)
                if input_state == False:
                    print('Button Pressed')
                    self.api_controller.send_notify()

                    for i in range(0,10):
                        for dc in range(0, 101, 5):
                            self.p.ChangeDutyCycle(dc)
                            time.sleep(0.05)
                        for dc in range(100, -1, -5):
                            self.p.ChangeDutyCycle(dc)
                            time.sleep(0.05)

        except KeyboardInterrupt:
            pass
        self.p.stop()

    def __del__(self):
        GPIO.cleanup()
