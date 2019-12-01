from motor import *
from network import *
from camera import *

import json

class Controller:
    def __init__(self):
        self.motor = Motor()
        self.network = Network()
        self.camera = Camera()
        self.camera.start()

        #self.motor.rotateRight(80)
      
    def run(self):
        while True:
            try:
                data = json.loads(self.network.getData())
                
                for c in data['commands']:
                    if c['command'] == 'RM_dir':
                        self.motor.setRightMotorDirection(c['value'])
                    if c['command'] == 'LM_dir':
                        self.motor.setLeftMotorDirection(c['value'])
                    if c['command'] == 'RM_speed':
                        self.motor.setRightMotorSpeed(c['value'])
                    if c['command'] == 'LM_speed':
                        self.motor.setLeftMotorSpeed(c['value'])


            except KeyboardInterrupt:
                self.motor.handleShutdown()
                self.camera.stop()
