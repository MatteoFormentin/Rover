import RPi.GPIO as GPIO
import time


class Motor:
    def __init__(self):
        self.RIGHT_IN1 = 6  # 31
        self.RIGHT_IN2 = 13  # 33
        self.LEFT_IN3 = 19  # 35
        self.LEFT_IN4 = 26  # 37
        self.RIGHT_PWM_ENA = 16  # 36
        self.RIGHT_PWM_ENB = 20  # 38
        self.COMP_SPEED_R = 0
        self.COMP_SPEED_L = 0

        self.LEFT_ENCODER = 25
        self.RIGHT_ENCODER = 8

        self.left_tick = 0
        self.right_tick = 0

        self.delta_left_tick = 0
        self.delta_right_tick = 0

        self.left_rpm = 0
        self.right_rpm = 0

        self.left_status = False
        self.right_status = False

        self.last_reset = time.time()

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.RIGHT_IN1, GPIO.OUT)
        GPIO.setup(self.RIGHT_IN2, GPIO.OUT)
        GPIO.setup(self.LEFT_IN3, GPIO.OUT)
        GPIO.setup(self.LEFT_IN4, GPIO.OUT)
        GPIO.setup(self.RIGHT_PWM_ENA, GPIO.OUT)
        GPIO.setup(self.RIGHT_PWM_ENB, GPIO.OUT)

        GPIO.setup(self.LEFT_ENCODER, GPIO.IN)
        GPIO.setup(self.RIGHT_ENCODER, GPIO.IN)

        self.pwm_right = GPIO.PWM(self.RIGHT_PWM_ENA, 50)
        self.pwm_left = GPIO.PWM(self.RIGHT_PWM_ENB, 50)

        # Start pwm with 0 duty cycle
        self.pwm_right.start(0)
        self.pwm_left.start(0)

        self.right_speed = 0
        self.left_speed = 0

        print("motor okay")

    def tickCounterUpdate(self):
        if GPIO.input(self.RIGHT_ENCODER) == 0 and self.right_status == True:
            self.right_status = False
        if GPIO.input(self.RIGHT_ENCODER) == 1 and self.right_status == False:
            self.right_status = True
            self.right_tick += 1
            self.delta_right_tick += 1

        if GPIO.input(self.LEFT_ENCODER) == 0 and self.left_status == True:
            self.left_status = False
        if GPIO.input(self.LEFT_ENCODER) == 1 and self.left_status == False:
            self.left_status = True
            self.left_tick += 1
            self.delta_left_tick += 1

        delta = time.time() - self.last_reset
        if delta > 1:
            self.last_reset = time.time()

            self.left_rpm = int(self.delta_left_tick / delta) * 30
            self.right_rpm = int(self.delta_right_tick / delta) * 30

            self.delta_left_tick = 0
            self.delta_right_tick = 0

    def getLeftTick(self):
        return self.left_tick

    def getRightTick(self):
        return self.right_tick

    def getLeftRPM(self):
        return self.left_rpm

    def getRightRPM(self):
        return self.right_rpm

    def handleShutdown(self):
        self.pwm_right.stop()
        self.pwm_left.stop()

        self.right_speed = 0
        self.left_speed = 0

        GPIO.cleanup()

    def setRightMotorDirection(self, dir):
        if dir == 0:
            GPIO.output(self.RIGHT_IN1, 1)
            GPIO.output(self.RIGHT_IN2, 0)

        if dir == 1:
            GPIO.output(self.RIGHT_IN1, 0)
            GPIO.output(self.RIGHT_IN2, 1)

    def setLeftMotorDirection(self, dir):
        if dir == 0:
            GPIO.output(self.LEFT_IN3, 1)
            GPIO.output(self.LEFT_IN4, 0)

        if dir == 1:
            GPIO.output(self.LEFT_IN3, 0)
            GPIO.output(self.LEFT_IN4, 1)

    def setRightMotorSpeed(self, speed):
        self.right_speed = speed
        if speed - self.COMP_SPEED_R > 0:
            self.pwm_right.ChangeDutyCycle(speed - self.COMP_SPEED_R)

        else:
            self.pwm_right.ChangeDutyCycle(0)

    def setLeftMotorSpeed(self, speed):
        self.left_speed = speed
        if speed - self.COMP_SPEED_L > 0:
            self.pwm_left.ChangeDutyCycle(speed - self.COMP_SPEED_L)

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
