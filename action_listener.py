import RPi.GPIO as GPIO
import time
from api_controller import ApiController


class ActionListener(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # ustawienie portów w tryby wejścia (18) i wyjścia (12, 21)
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

        self.api_controller = ApiController()

    def listen(self):
        while 1:
            input_state = GPIO.input(18)  # odczyt stanu na porcie 18
            if input_state == False:
                print('Button Pressed')
                self.api_controller.send_notify()  # wysłanie powiadomienia

                # sekwencja zmiany stanów dwóch diód i brzęczyka trwająca 10s
                for i in range(10):
                    GPIO.output(12, GPIO.HIGH)
                    GPIO.output(21, GPIO.LOW)
                    time.sleep(0.5)
                    GPIO.output(12, GPIO.LOW)
                    GPIO.output(21, GPIO.HIGH)
                    time.sleep(0.5)

                GPIO.output(21, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()  # przywraca użyte porty w tryb odczytu
