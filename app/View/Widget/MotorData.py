from tkinter import *

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class MotorData(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.motor_data_label = self.create_text(
            (CANVAS_WIDTH/2, 30), text="MOTOR DATA", fill="white", font=("default", 30))

        self.state_label = self.create_text(
            (105, 70), text="State: ", fill="white", font=("default", 30))
        self.state_value = self.create_text(
            (105 + 90, 70), text="N/A", fill="red", font=("default", 30))

        self.right_throttle_label = self.create_text(
            (105, 105), text="Right: ", fill="white", font=("default", 30))
        self.right_throttle_value = self.create_text(
            (105 + 90, 105), text="N/A", fill="red", font=("default", 30))

        self.left_throttle_label = self.create_text(
            (95, 140), text="Left: ", fill="white", font=("default", 30))
        self.left_throttle_value = self.create_text(
            (105 + 90, 140), text="N/A", fill="red", font=("default", 30))

        self.battery_label = self.create_text(
            (95, 175), text="Battery: ", fill="white", font=("default", 30))
        self.battery_value = self.create_text(
            (105 + 100, 175), text="N/A", fill="green", font=("default", 30))

    def update(self, motor_data, battery):

        if motor_data["state"] == 0:
            self.itemconfig(self.state_value,
                            text="STOP", fill="red")

        if motor_data["state"] == 1:
            self.itemconfig(self.state_value,
                            text="FORW", fill="green")

        if motor_data["state"] == 2:
            self.itemconfig(self.state_value,
                            text="BACK", fill="green")

        if motor_data["state"] == 3:
            self.itemconfig(self.state_value,
                            text="LEFT", fill="green")

        if motor_data["state"] == 4:
            self.itemconfig(self.state_value,
                            text="RIGHT", fill="green")

        self.itemconfig(self.left_throttle_value,
                        text=(str(motor_data["left_power"]) + "%"))
        self.itemconfig(self.right_throttle_value,
                        text=(str(motor_data["right_power"]) + "%"))
        self.itemconfig(self.battery_value,
                        text=(str(round(battery, 1)) + "V"))
