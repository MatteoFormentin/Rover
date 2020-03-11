import RPi.GPIO as GPIO
from threading import Thread
import time


LEFT_ENCODER = 25
RIGHT_ENCODER = 8


class Encoder(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.left_tick = 0
        self.right_tick = 0

        self.previous_left_tick = 0
        self.previous_right_tick = 0

        self.left_status = False
        self.right_status = False

        self.left_rpm = 0
        self.right_rpm = 0

        GPIO.setup(LEFT_ENCODER, GPIO.IN)
        GPIO.setup(RIGHT_ENCODER, GPIO.IN)

        self.run_thread = True

    def run(self):
        self.last_reset = time.time()
        while self.run_thread:
            if GPIO.input(RIGHT_ENCODER) == 0 and self.right_status == True:
                self.right_status = False
            if GPIO.input(RIGHT_ENCODER) == 1 and self.right_status == False:
                self.right_status = True
                self.right_tick += 1

            if GPIO.input(LEFT_ENCODER) == 0 and self.left_status == True:
                self.left_status = False
            if GPIO.input(LEFT_ENCODER) == 1 and self.left_status == False:
                self.left_status = True
                self.left_tick += 1

            delta = time.time() - self.last_reset
            if delta > 0.1:

                # 50 tick / round
                self.right_rpm = int(((self.right_tick -
                                   self.previous_right_tick) / delta) * (60/75))
                self.left_rpm = int(((self.left_tick -
                                  self.previous_left_tick) / delta) * (60/75))

                self.previous_left_tick = self.left_tick
                self.previous_right_tick = self.right_tick
                self.last_reset = time.time()

    def stop(self):
        self.run_thread = False
