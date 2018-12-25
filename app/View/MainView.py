from app.View.Widget.Radar import *
from app.View.Widget.MotorData import *
from app.View.Widget.Angle import *
from app.View.Widget.GPSData import *


class MainView(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.connection_state = 0

        self.radar = Radar(self)
        self.radar.grid(row=0, column=0)

        self.motor_data = MotorData(self)
        self.motor_data.grid(row=0, column=1)

        self.gps_data = GPSData(self)
        self.gps_data.grid(row=0, column=2)

    def updateRadar(self, distance_vector):
        self.radar.update(distance_vector)

    def updateMotorData(self, motor_data, battery):
        self.motor_data.update(motor_data, battery)

    def updateGPSData(self, gps_data):
        self.gps_data.update(gps_data)
