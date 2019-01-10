from tkinter import *
from PIL import ImageTk, Image
import os
import math

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300

L = 150


class Compass(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.filename = os.path.join(os.path.abspath(
            os.curdir), 'app/images/compass_background.jpg')

        self.img = Image.open(self.filename)
        self.image = ImageTk.PhotoImage(self.img)
        self.background = self.create_image(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=self.image)

        self.heading_label = self.create_text(
            (280, 20), text="0°", fill="white", font=("default", 30), anchor="e")

        self.arrow = None
        self.updateHeading(0)

    def updateHeading(self, heading):
        h = heading
        heading = -heading * 2 * math.pi / 360.0
        xy = (CANVAS_WIDTH/2-L/2*math.sin(heading), CANVAS_HEIGHT/2-L/2*math.cos(heading),
              CANVAS_WIDTH/2+L/2*math.sin(heading), CANVAS_HEIGHT/2+L/2*math.cos(heading))
        self.delete(self.arrow)
        self.arrow = self.create_line(xy, width=4, fill="green",
                                      arrow="first", arrowshape="12 14 7")
        self.itemconfig(self.heading_label, text=(str(h) + "°"))
