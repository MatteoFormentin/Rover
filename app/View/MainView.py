from app.View.Widget.Radar import *
from app.View.Widget.MotorData import *
from app.View.Widget.Angle import *
from app.View.Widget.GPSData import *
from app.View.Widget.GPSPlot import *
from app.View.Widget.Compass import *
from app.View.Widget.Buttons import *


class MainView(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.configure(background="#282828")

        self.radar = Radar(self)
        self.radar.grid(row=0, column=2)

        self.motor_data = MotorData(self)
        self.motor_data.grid(row=0, column=0)

        self.compass = Compass(self)
        self.compass.grid(row=0, column=3)

        self.buttons = Buttons(self, self.controller)
        self.buttons.grid(row=0, column=1)

        self.gps_plot = GPSPlot(self)
        self.gps_plot.canvas.get_tk_widget().grid(row=1, column=1, columnspan=2)

        self.gps_data = GPSData(self, self.gps_plot)
        self.gps_data.grid(row=1, column=0)

    def updateRadar(self, distance_vector):
        self.radar.update(distance_vector)

    def updateMotorData(self, motor_data, battery):
        self.motor_data.update(motor_data, battery)

    def updateGPSData(self, gps_data):
        self.gps_data.update(gps_data)

    def updateCompass(self, heading):
        self.compass.updateHeading(heading)

    def updateMode(self, mode):
        self.buttons.updateMode(mode)
