from tkinter import *
import math

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class Angle(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=1)

        self.pitch_line = None
        #self.createPitchLine(60)

    def update(self, motor_data):
        pass

    def reset(self):
        pass

    def createPitchLine(self, angle):
        self.create_line(50, 100 + 100*math.sin(angle*2*math.pi/360.0),
                         250, 100 - 100*math.sin(angle*2*math.pi/360.0), fill="red", width=5)
