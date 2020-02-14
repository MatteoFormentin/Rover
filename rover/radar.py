import time
import RPi.GPIO as GPIO


HC_TRIGGER_RIGHT = 17
HC_ECHO_RIGHT = 27
HC_TRIGGER_CENTER = 18
HC_ECHO_CENTER = 22
HC_TRIGGER_LEFT = 23
HC_ECHO_LEFT = 24

REFRESH_RATE = 0.01  # Seconds


class Radar:
    def __init__(self):
        GPIO.setup(HC_TRIGGER_RIGHT, GPIO.OUT)
        GPIO.setup(HC_ECHO_RIGHT, GPIO.IN)
        GPIO.setup(HC_TRIGGER_CENTER, GPIO.OUT)
        GPIO.setup(HC_ECHO_CENTER, GPIO.IN)
        GPIO.setup(HC_TRIGGER_LEFT, GPIO.OUT)
        GPIO.setup(HC_ECHO_LEFT, GPIO.IN)

        self.right = 0
        self.center = 0
        self.left = 0

        self.last_measure = time.time()

    def update(self):
        if time.time() - self.last_measure > REFRESH_RATE:
            self.right = self.getSensorDistance(
                HC_TRIGGER_RIGHT, HC_ECHO_RIGHT)
            self.center = self.getSensorDistance(
                HC_TRIGGER_CENTER, HC_ECHO_CENTER)
            self.left = self.getSensorDistance(
                HC_TRIGGER_LEFT, HC_ECHO_LEFT)

    def getDistances(self):
        distances = []
        distances.append(self.right)
        distances.append(self.center)
        distances.append(self.left)
        return distances

    def getSensorDistance(self, trigger, echo):
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        start_time = time.time()
        end_time = time.time()
        while GPIO.input(echo) == 0:
            start_time = time.time()
        while GPIO.input(echo) == 1:
            if time.time() - start_time > 0.006:  # Limit to 100 cm
                return 100
            end_time = time.time()

        distance = int((end_time - start_time) * 34300 / 2)
        return distance
