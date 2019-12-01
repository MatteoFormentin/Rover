import RPi.GPIO as GPIO
import configparser


class Motor:
    def __init__(self):
        # Load configuration file
        '''config = configparser.ConfigParser()
        config.read('pin_configuration.ini')

        self.RIGHT_IN1 = int(config['MOTOR']['RIGHT_IN1'])
        self.RIGHT_IN2 = int(config['MOTOR']['RIGHT_IN2'])
        self.LEFT_IN3 = int(config['MOTOR']['LEFT_IN3'])
        self.LEFT_IN4 = int(config['MOTOR']['LEFT_IN4'])
        self.RIGHT_PWM_ENA = int(config['MOTOR']['RIGHT_PWM_ENA'])
        self.RIGHT_PWM_ENB = int(config['MOTOR']['RIGHT_PWM_ENB'])
        self.COMP_SPEED_R = int(config['MOTOR']['COMP_SPEED_R'])
        self.COMP_SPEED_L = int(config['MOTOR']['COMP_SPEED_L'])'''

        self.RIGHT_IN1 = 31
        self.RIGHT_IN2 = 33
        self.LEFT_IN3 = 35
        self.LEFT_IN4 = 37
        self.RIGHT_PWM_ENA = 36
        self.RIGHT_PWM_ENB = 38
        self.COMP_SPEED_R = 0
        self.COMP_SPEED_L = 0


        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RIGHT_IN1, GPIO.OUT)
        GPIO.setup(self.RIGHT_IN2, GPIO.OUT)
        GPIO.setup(self.LEFT_IN3, GPIO.OUT)
        GPIO.setup(self.LEFT_IN4, GPIO.OUT)
        GPIO.setup(self.RIGHT_PWM_ENA, GPIO.OUT)
        GPIO.setup(self.RIGHT_PWM_ENB, GPIO.OUT)

        self.pwm_right = GPIO.PWM(self.RIGHT_PWM_ENA, 50)
        self.pwm_left = GPIO.PWM(self.RIGHT_PWM_ENB, 50)

        # Start pwm with 0 duty cycle
        self.pwm_right.start(0)
        self.pwm_left.start(0)

        self.right_speed=0
        self.left_speed=0

    def handleShutdown(self):
        self.pwm_right.stop()
        self.pwm_left.stop()

        self.right_speed = 0
        self.left_speed = 0

        #GPIO.cleanup()


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
        self.right_speed=speed
        if speed - self.COMP_SPEED_R > 0:
            self.pwm_right.ChangeDutyCycle(speed - self.COMP_SPEED_R)

        else:
            self.pwm_right.ChangeDutyCycle(0)

    def setLeftMotorSpeed(self, speed):
        self.right_speed=speed
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
