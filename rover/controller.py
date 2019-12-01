from motor import *
from network import *
from camera import *
from queue import *
from threading import Thread

import json


class Controller:
    def __init__(self):
        self.motor = Motor()

        self.queue = Queue()
        self.network = Network(self.queue)
        self.network.start()

        self.camera = Camera()
        self.camera.start()

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    data = json.loads(self.queue.get())

                    for c in data['commands']:
                        if c['command'] == 'RM_dir':
                            self.motor.setRightMotorDirection(c['value'])
                            print('RM_dir')
                        if c['command'] == 'LM_dir':
                            print('LM_dir')
                            self.motor.setLeftMotorDirection(c['value'])
                        if c['command'] == 'RM_speed':
                            self.motor.setRightMotorSpeed(c['value'])
                            print('RM_speed')
                        if c['command'] == 'LM_speed':
                            print('LM_speed')
                            self.motor.setLeftMotorSpeed(c['value'])

                # HERE ALL SENSORS LOOPS

            except KeyboardInterrupt:
                self.motor.handleShutdown()
                self.camera.stop()
