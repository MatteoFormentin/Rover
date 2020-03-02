from tkinter import *


class ControllerWindow(Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.configure(background="#282828")
        self.title("Controller")
        self.up_button = Button(
            self, text="F", background="#282828", highlightbackground="#282828", width=20)
        self.up_button.grid(row=0, column=0, columnspan=2)

        self.up_button.bind("<ButtonPress>", self.up_on_press)
        self.up_button.bind("<ButtonRelease>", self.on_release)

        self.left_button = Button(
            self, text="L", background="#282828", highlightbackground="#282828", width=20)
        self.left_button.grid(row=1, column=0)

        self.left_button.bind("<ButtonPress>", self.left_on_press)
        self.left_button.bind("<ButtonRelease>", self.on_release)

        self.right_button = Button(
            self, text="R", background="#282828", highlightbackground="#282828", width=20)
        self.right_button.grid(row=1, column=1)

        self.right_button.bind("<ButtonPress>", self.right_on_press)
        self.right_button.bind("<ButtonRelease>", self.on_release)

        self.down_button = Button(
            self, text="B", background="#282828", highlightbackground="#282828", width=20)
        self.down_button.grid(row=2, columnspan=2)

        self.down_button.bind("<ButtonPress>", self.down_on_press)
        self.down_button.bind("<ButtonRelease>", self.on_release)

    def up_on_press(self, event):
        self.controller.goForward()

    def left_on_press(self, event):
        self.controller.goLeft()

    def right_on_press(self, event):
        self.controller.goRight()

    def down_on_press(self, event):
        self.controller.goBackward()

    def on_release(self, event):
        self.controller.stop()
