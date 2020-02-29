from tkinter import *
from PIL import ImageTk, Image
import os
import math

CANVAS_WIDTH = 390
CANVAS_HEIGHT = 300


class CameraWindow(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=0,
                         highlightthickness=0, background="#282828")

        self.curr_frame = self.create_image(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
        self.fps_label = self.create_text(
            (340, 45), text="FPS: ", fill="red", font=("default", 15), anchor="e")

    def updateCameraWindow(self, img, fps):
        self.itemconfig(self.fps_label, text=("FPS: " + str(fps)))
        try:
            self.image = Image.fromarray(img)
            self.image = ImageTk.PhotoImage(self.image)

            self.itemconfig(self.curr_frame, image=self.image)
        except Exception as e:
            #print(e)
            pass
