from tkinter import *
import os

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300

BUTTON_WIDTH = 15


class Buttons(Frame):
    def __init__(self, master, controller):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.pack_propagate(False)

        self.controller = controller
        self.mode = 0

        self.status_label = Label(
            self, text="REMOTE MODE",  background="#282828", fg="green",  font=("Helvetica", 24))
        self.status_label.pack(pady=50)

        self.auto_button = Button(
            self, text="Auto Mode", background="#282828", highlightbackground="#282828", width=BUTTON_WIDTH, command=self.autoButtonPressed)
        self.auto_button.pack()

        self.remote_button = Button(
            self, text="Remote Mode", background="#282828", highlightbackground="#282828", width=BUTTON_WIDTH, command=self.remoteButtonPressed)
        self.remote_button.pack()

    def remoteButtonPressed(self):
        self.controller.setRemoteMode()

    def autoButtonPressed(self):
        self.controller.setAutoMode()

    def updateMode(self, mode):
        if mode != self.mode:
            print(mode)

            self.mode = mode
            if mode == 0:
                self.status_label.config(text=("REMOTE MODE"))

            if mode == 1:
                self.status_label.config(text=("AUTO MODE"))
