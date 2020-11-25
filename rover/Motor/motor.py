import RPi.GPIO as GPIO
import time
from Motor.encoder import *
from PID import *

RIGHT_IN1 = 6  # 31
RIGHT_IN2 = 13  # 33
LEFT_IN3 = 19  # 35
LEFT_IN4 = 26  # 37
RIGHT_PWM_ENA = 16  # 36
RIGHT_PWM_ENB = 20  # 38
COMP_SPEED_R = 0
COMP_SPEED_L = 0
STALL_SPEED = 10

LEFT_ENCODER = 25
RIGHT_ENCODER = 8


class Motor:
    def __init__(self):

        self.right_speed = 0
        self.left_speed = 0

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RIGHT_IN1, GPIO.OUT)
        GPIO.setup(RIGHT_IN2, GPIO.OUT)
        GPIO.setup(LEFT_IN3, GPIO.OUT)
        GPIO.setup(LEFT_IN4, GPIO.OUT)
        GPIO.setup(RIGHT_PWM_ENA, GPIO.OUT)
        GPIO.setup(RIGHT_PWM_ENB, GPIO.OUT)

        self.pwm_right = GPIO.PWM(RIGHT_PWM_ENA, 50)
        self.pwm_left = GPIO.PWM(RIGHT_PWM_ENB, 50)

        # Start pwm with 0 duty cycle
        self.pwm_right.start(0)
        self.pwm_left.start(0)

        self.enc = Encoder()
        self.enc.start()

        #self.motorPID = PID(2, 2, 0, 0, 100)

    '''def update(self):
        rpm_avg = int((self.enc.left_rpm + self.enc.left_rpm) / 2)
        speed = self.motorPID.computeOutput(
            rpm_avg, int(self.right_speed * 150/100))
        print("OUT:"+str(speed) + " MEASURED:" + str(rpm_avg) +
              " TARGET:" + str(int(self.right_speed * 150/100))+"            ", end='\r')
        self.setRightMotorRealSpeed(speed)
        self.setLeftMotorRealSpeed(speed)'''

    def getLeftTick(self):
        return self.enc.left_tick

    def getRightTick(self):
        return self.enc.right_tick

    def getLeftRPM(self):
        return self.enc.left_rpm

    def getRightRPM(self):
        return self.enc.right_rpm

    def handleShutdown(self):
        self.pwm_right.stop()
        self.pwm_left.stop()

        self.right_speed = 0
        self.left_speed = 0

        GPIO.cleanup()

    def setRightMotorDirection(self, dir):
        if dir == 0:
            GPIO.output(RIGHT_IN1, 1)
            GPIO.output(RIGHT_IN2, 0)

        if dir == 1:
            GPIO.output(RIGHT_IN1, 0)
            GPIO.output(RIGHT_IN2, 1)

    def setLeftMotorDirection(self, dir):
        if dir == 0:
            GPIO.output(LEFT_IN3, 1)
            GPIO.output(LEFT_IN4, 0)

        if dir == 1:
            GPIO.output(LEFT_IN3, 0)
            GPIO.output(LEFT_IN4, 1)

    def setRightMotorSpeed(self, speed):
        if speed - COMP_SPEED_R > STALL_SPEED:
            self.pwm_right.ChangeDutyCycle(speed - COMP_SPEED_R)

        else:
            self.pwm_right.ChangeDutyCycle(0)

    def setLeftMotorSpeed(self, speed):
        if speed - COMP_SPEED_L > STALL_SPEED:
            self.pwm_left.ChangeDutyCycle(speed - COMP_SPEED_L)

        else:
            self.pwm_left.ChangeDutyCycle(0)

    def getRightMotorSpeed(self):
        return self.right_speed

    def getLeftMotorSpeed(self):
        return self.left_speed

    def motorStop(self):
        self.pwm_right.ChangeDutyCycle(0)
        self.pwm_left.ChangeDutyCycle(0)

    def goForward(self, speed):
        self.setRightMotorDirection(0)
        self.setLeftMotorDirection(0)
        self.setRightMotorSpeed(speed)
        self.setLeftMotorSpeed(speed)

    def goBackward(self, speed):
        self.setRightMotorDirection(1)
        self.setLeftMotorDirection(1)
        self.setRightMotorSpeed(speed)
        self.setLeftMotorSpeed(speed)

    def rotateLeft(self, speed):
        self.setRightMotorDirection(0)
        self.setLeftMotorDirection(1)
        self.setRightMotorSpeed(speed)
        self.setLeftMotorSpeed(speed)

    def rotateRight(self, speed):
        self.setRightMotorDirection(1)
        self.setLeftMotorDirection(0)
        self.setRightMotorSpeed(speed)
        self.setLeftMotorSpeed(speed)
