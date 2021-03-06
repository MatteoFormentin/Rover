from Motor.motor import *
from network import *
from camera import *
from queue import *
from radar import *
from gps import *
from compass import *
from waypoint import *


from threading import Thread
import time
import json


class Controller:
    def __init__(self):
        self.motor = Motor()

        # NETWORK THREAD
        self.queue = Queue()  # Shared queue
        self.network = Network(self.queue)
        self.network.start()

        # SENSORS SETUP
        self.gps = Gps()
        self.compass = Compass()
        self.radar = Radar()

        # CAMERA THREAD
        self.camera = Camera()
        self.camera.start()

        # WAYPOINT NAVIGATION CONTROLLER
       # self.waypoint_navigation = Waypoint(self.motor, self.gps, self.compass)

        self.ground_station_ip_address = "0"

        #self.waypoint_navigation.addWaypoint([45.6327, 8.8289])
       # self.waypoint_navigation.setRun(True)

        ''' print("ROTATING")
        while True:
            self.waypoint_navigation.rotateToBearing(self.compass.getBearingNormalized(),
                                                     180)'''

        print("ROVER STARTED")

    def run(self):
        while True:
            try:
                # READ ONE COMMAND PACKET AND EXECUTE ALL THE COMMANDS FROM GROUND STATION
                if not self.queue.empty():
                    data = json.loads(self.queue.get())

                    for c in data['commands']:
                        # SEND NEW DATA
                        if c['command'] == 'update':
                            self.network.sendData(self.collectAllData())

                        # CAMERA STREAM COMMANDS
                        if c['command'] == 'C_Stream_Start':
                            self.ground_station_ip_address = c['value']
                            self.camera.setGroundStationIpAddress(
                                self.ground_station_ip_address)
                            self.camera.startVideoStream()

                        if c['command'] == 'C_Stream_Stop':
                            self.camera.stopVideoStream()

                        if c['command'] == 'C_Take_Photo':
                            img_encoded = self.camera.takePhoto()
                            self.network.sendBytes(img_encoded)

                        # MOTORS COMMANDS
                        if c['command'] == 'RM_dir':
                            self.motor.setRightMotorDirection(c['value'])

                        if c['command'] == 'LM_dir':
                            self.motor.setLeftMotorDirection(c['value'])

                        if c['command'] == 'RM_speed':
                            self.motor.setRightMotorSpeed(c['value'])

                        if c['command'] == 'LM_speed':
                            self.motor.setLeftMotorSpeed(c['value'])

                # HERE ALL SENSORS LOOPS
                #self.motor.update()
                self.waypoint_navigation.update()
                self.gps.update()
                self.radar.update()

            except KeyboardInterrupt:
                self.motor.handleShutdown()
                self.camera.stop()
                self.network.stop()
                self.camera.join()
                self.network.join()
                exit()

    def collectAllData(self):
        gps_data = self.gps.getData()

        data = json.dumps({
            "motor": {
                "state": "STOP",
                "left_power": self.motor.getLeftMotorSpeed(),
                "right_power": self.motor.getRightMotorSpeed(),
                "left_tick": self.motor.getLeftTick(),
                "right_tick": self.motor.getRightTick(),
                "left_rpm": self.motor.getLeftRPM(),
                "right_rpm": self.motor.getRightRPM()
            },

            "compass": self.compass.getBearing(),
            "radar": self.radar.getDistances(),

            "gps": {
                "fix": gps_data.has_fix,
                "fix_quality": gps_data.fix_quality,
                "satellites": gps_data.satellites,
                "latitude": round(gps_data.latitude, 4) if gps_data.latitude != None else "",
                "longitude": round(gps_data.longitude, 4) if gps_data.longitude != None else "",
                "speed": gps_data.speed_knots if gps_data.speed_knots != None else "",
                "altitude": gps_data.altitude_m if gps_data.altitude_m != None else ""
            }
        })

        return data


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
