import math
from PID import *
import time

wapoints = []

point = [0, 0]  # lat, lon


class Waypoint:
    def __init__(self, motor, gps, compass):
        self.rotationPID = PID(0.1, 0, 0, -100, 100)
        self.distancePID = PID(0.2, 0.1, 0, 0, 100)

        self.run = False

        self.motor = motor
        self.gps = gps
        self.compass = compass

        self.waypoints = []
        self.current_point = 0
        self.current_waypoint_index = 0  # Waipoint Array Index

    def update(self):
        if not self.run:
            return

        if not self.gps.isGpsFix():  # Wait for fix
            self.motor.motorStop()
            return

        self.current_point = self.gps.getCurrentPoint()

        next_point = self.waypoints[self.current_waypoint_index]

        # Calculate bearing from next point
        dest_bearing = computeBearing(self.current_point, next_point)
        curr_bearing = self.compass.getBearing()

        # Calculate distance from next point
        distance_to_dest = self.computeDistance(self.current_point, next_point)

        # If destination reached
        if distance_to_dest < 1:
            self.current_waypoint_index += 1
        # If bearing of rover is wrong rotate to correct
        elif dest_bearing != curr_bearing:  # +- offeset
            speed = self.rotationPID.computeOutput(curr_bearing, dest_bearing)
            if dest_bearing > curr_bearing:

                self.motor.rotateLeft(speed)

            if dest_bearing < curr_bearing:

                self.motor.rotateRight(speed)

        # If correct bearing is correct and destination is far go forward
        else:
            speed = self.distancePID.computeOutput(distance_to_dest, 0)
            self.motor.goForward(speed)

    def setRun(self, status):
        if status == True:
            self.rotationPID.reset()

        self.run = status

    def addWaypoints(self, w):
        self.waypoints += w

    def addWaipoint(self, point):
        self.waypoints.append(point)

    # DEBUG ONLY
    def rotateToBearing(self, curr, dest):
        speed = self.rotationPID.computeOutput(curr, dest)
        '''if speed < 10:
            speed = 0'''

        print("speed: " + str(speed) + " curr: " +
              str(curr) + " dest: " +
              str(dest) + "        ")

        if speed > 0:
            print("rotate left")
            self.motor.rotateLeft(speed)

        elif speed < 0:
            print("rotate right")
            self.motor.rotateRight(-1 * speed)

        # DEBUG ONLY
        if curr == dest:
            print("stop")

            self.motor.motorStop()

        print()

        # time.sleep(0.1)

    def computeBearing(self, p1, p2):
        ''' Compute bearing between point 1 and 2 '''
        lat1 = math.radians(p1[0])
        lat2 = math.radians(p2[0])

        lon1 = math.radians(p1[1])
        lon2 = math.radians(p2[1])

        y = math.sin(lon2-lon1) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1) * \
            math.cos(lat2)*math.cos(lon2-lon1)
        brng = math.degrees(math.atan2(y, x))
        return brng

    def computeDistance(self, p1, p2):
        R = 6371e3  # Earth radius

        lat1 = math.radians(p1[0])
        lat2 = math.radians(p2[0])

        lon1 = math.radians(p1[1])
        lon2 = math.radians(p2[1])

        delta_lat = math.radians(lat2-lat1)
        delta_lon = math.radians(lon2-lon1)

        a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1) * \
            math.cos(lat2) * math.sin(delta_lon/2) * math.sin(delta_lon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c
        return d
