from app.View.Widget.Radar import *
from app.View.Widget.MotorData import *
from app.View.Widget.Angle import *


class MainView(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.connection_state = 0

        self.radar = Radar(self)
        self.radar.grid(row=0, column=1)

        self.motor_data = MotorData(self)
        self.motor_data.grid(row=0, column=2)

        self.angle = Angle(self)
        self.angle.grid(row=0, column=0)

    def updateRadar(self, distance_vector):
        self.radar.update(distance_vector)

    def updateMotorData(self, motor_data):
        self.motor_data.update(motor_data)
