from tkinter import *
import os

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300

BUTTON_WIDTH = 15
SLIDER_LENGHT = 150


class Buttons(Frame):
    def __init__(self, master, controller):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.grid_propagate(False)

        self.controller = controller
        self.mode = 0

        self.status_label = Label(
            self, text="REMOTE MODE",  background="#282828", fg="green",  font=("Helvetica", 24))
        self.status_label.grid(row=0, column=0, rowspan=2, pady=(50, 0))

        self.auto_button = Button(
            self, text="Auto Mode", background="#282828", highlightbackground="#282828", width=BUTTON_WIDTH, command=self.autoButtonPressed)
        self.auto_button.grid(row=2, column=0, padx=(50, 50))
        self.photo_button = Button(
            self, text="Take Photo", background="#282828", highlightbackground="#282828", width=BUTTON_WIDTH, command=self.photoButtonPressed)
        self.photo_button.grid(row=3, column=0)

        self.speed = Scale(
            self, from_=0, to=100, orient=HORIZONTAL,  background="#282828", fg="white", length=SLIDER_LENGHT, label="Speed",
            command=self.changedScaleSpeed)
        self.speed.grid(row=0, column=1, pady=(20, 0))

        self.turning_speed = Scale(
            self, from_=0, to=100, orient=HORIZONTAL,  background="#282828", fg="white", length=SLIDER_LENGHT, label="Turning Speed", command=self.changedScaleTurningSpeed)
        self.turning_speed.grid(row=1, column=1, pady=(5, 0))

        self.auto_speed = Scale(
            self, from_=0, to=100, orient=HORIZONTAL,  background="#282828", fg="white", length=SLIDER_LENGHT, label="Auto Speed", command=self.changedScaleAutoSpeed)
        self.auto_speed.grid(row=2, column=1, pady=(5, 0))

        self.auto_turning_speed = Scale(
            self, from_=0, to=100, orient=HORIZONTAL,  background="#282828", fg="white", length=SLIDER_LENGHT, label="Auto Turning Speed", command=self.changedScaleAutoTurningSpeed)
        self.auto_turning_speed.grid(row=3, column=1, pady=(5, 0))

    def autoButtonPressed(self):
        if self.mode == 0:
            self.controller.setAutoMode()

        if self.mode == 1:
            self.controller.setRemoteMode()

    def photoButtonPressed(self):
        self.controller.takePhoto()

    def updateMode(self, mode):
        if mode != self.mode:
            print(mode)

            self.mode = mode
            if mode == 0:
                self.status_label.config(text=("REMOTE MODE"), fg="green")
                self.auto_button.config(text=("AUTO MODE"))

            if mode == 1:
                self.status_label.config(text=("AUTO MODE"), fg="orange")
                self.auto_button.config(text=("REMOTE MODE"))

    def changedScaleSpeed(self, val):
        self.controller.setSpeed(self.speed.get())

    def changedScaleTurningSpeed(self, val):
        self.controller.setTurningSpeed(self.turning_speed.get())

    def changedScaleAutoSpeed(self, val):
        self.controller.setAutoSpeed(self.auto_speed.get())

    def changedScaleAutoTurningSpeed(self, val):
        self.controller.setAutoTurningSpeed(self.auto_turning_speed.get())

    def updateSpeed(self, speed):
        self.speed.set(speed)

    def updateTurningSpeed(self, speed):
        self.turning_speed.set(speed)

    def updateAutoSpeed(self, speed):
        self.auto_speed.set(speed)

    def updateAutoTurningSpeed(self, speed):
        self.auto_turning_speed.set(speed)
