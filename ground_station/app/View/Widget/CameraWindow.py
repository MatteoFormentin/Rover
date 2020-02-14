from tkinter import *
from PIL import ImageTk, Image
import os
import math

CANVAS_WIDTH = 390
CANVAS_HEIGHT = 300



class CameraWindow(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=0,
                         highlightthickness=0)

        self.curr_frame = None

    def updateCameraWindow(self, img):
        try:
            self.image = Image.fromarray(img)
            self.image = ImageTk.PhotoImage(self.image)

            # if the panel is not None, we need to initialize it
            if self.curr_frame is None:
                self.curr_frame = self.create_image(
                    CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=self.image)

            # otherwise, simply update the panel
            else:
                self.itemconfig(self.curr_frame, image=self.image)
        except Exception as e:
            print(e)
            pass
