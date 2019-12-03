from motor import *
from network import *
from camera import *
from queue import *
from radar import *

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

        #self.radar = Radar()
        
        print("READY!")
        '''while True:
            self.radar.update()'''

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    data = json.loads(self.queue.get())

                    for c in data['commands']:
                        if c['command'] == 'update':
                            self.network.sendData(self.collectAllData())
                            
                        if c['command'] == 'RM_dir':
                            self.motor.setRightMotorDirection(c['value'])

                        if c['command'] == 'LM_dir':
                            self.motor.setLeftMotorDirection(c['value'])

                        if c['command'] == 'RM_speed':
                            self.motor.setRightMotorSpeed(c['value'])

                        if c['command'] == 'LM_speed':
                            self.motor.setLeftMotorSpeed(c['value'])

                # HERE ALL SENSORS LOOPS
                

            except KeyboardInterrupt:
                self.motor.handleShutdown()
                self.camera.stop()
                self.network.stop()
                #self.camera.join()
                #self.network.join()
                exit()
    
    def collectAllData(self):
        return json.dumps({
            "motor": {
                "state": "STOP",
                "left_power": self.motor.getLeftMotorSpeed(),
                "right_power": self.motor.getRightMotorSpeed()
            }
            

            #"radar": self.radar.update()
        })


'''JSON MESSAGE TO GROUND STATION
{
    "radar": [0, 1, 2, 3, 4, 5],
    "gps": {
        "latitude": 1.00,
            "longitude": 1.00,
            "speed": 10.0,
            "altitude": 220
    },
    "imu": [pitch, roll],
    "compass": gradi_int,
    "motor": {
        "state": "STOP",
        "left_power": 100,
        "right_power": 100
    }
}
'''
