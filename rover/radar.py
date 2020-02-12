from gpiozero import DistanceSensor, Device
from gpiozero.pins.native import NativeFactory
import configparser


HC_TRIGGER_RIGHT = 17
HC_ECHO_RIGHT = 27
HC_TRIGGER_CENTER = "BOARD12"
HC_ECHO_CENTER = "BOARD15"
HC_TRIGGER_LEFT = "BOARD16"
HC_ECHO_LEFT = "BOARD18"


class Radar:
    def __init__(self):

        Device.pin_factory = NativeFactory()

        '''self.left = DistanceSensor(
            echo=config['MOTOR']['HC_ECHO_LEFT'], trigger=config['MOTOR']['HC_TRIGGER_LEFT'])
        self.center = DistanceSensor(
            echo=config['MOTOR']['HC_ECHO_CENTER'], trigger=config['MOTOR']['HC_TRIGGER_CENTER'])
        self.right = DistanceSensor(
            echo=config['MOTOR']['HC_ECHO_RIGHT'], trigger=config['MOTOR']['HC_TRIGGER_RIGHT'])'''

        '''self.left = DistanceSensor(
            echo=HC_ECHO_LEFT, trigger=HC_TRIGGER_LEFT)
        self.center = DistanceSensor(
            echo=HC_ECHO_CENTER, trigger=HC_TRIGGER_CENTER)'''
        self.right = DistanceSensor(
            echo=HC_ECHO_RIGHT, trigger=HC_TRIGGER_RIGHT, max_distance = 2.0)

    def getDistances(self):
        '''measure = [0, 0, 0]
        measure[0] = self.right.distance
        measure[1] = self.center.distance
        measure[2] = self.left.distance'''
        print(self.right.distance)
        #return measure
