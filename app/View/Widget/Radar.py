from tkinter import *

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300

PADDING_LEFT = 20
PADDING_TOP = 50

RANGE = 1024 / 7


class Radar(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=1)

        range_xy = 10, 40, 290, 320
        
        r_one = 100
        xy_one = 10+r_one, 40+r_one, 290-r_one, 320-r_one

        r_two = 66
        xy_two = 10+r_two, 40+r_two, 290-r_two, 320-r_two

        r_three = 33
        xy_three = 10+r_three, 40+r_three, 290-r_three, 320-r_three

        r_four = 0
        xy_four = 10+r_four, 40+r_four, 290-r_four, 320-r_four

        rover_xy = 130, 130+52, 170, 170+52

        self.range = self.create_arc(
            range_xy, start=0, extent=180, outline="black", style="pieslice", fill="green")

        self.sector = [
            [
                self.create_arc(
                    xy_four, start=0, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=30, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=60, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=90, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=120, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=150, extent=30, outline="black", width=1, fill="green")
            ],

            [
                self.create_arc(
                    xy_three, start=0, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=30, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=60, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=90, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=120, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=150, extent=30, outline="black", width=1, fill="green")
            ],

            [
                self.create_arc(
                    xy_two, start=0, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=30, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=60, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=90, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=120, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=150, extent=30, outline="black", width=1, fill="green")
            ],

            [
                self.create_arc(
                    xy_one, start=0, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=30, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=60, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=90, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=120, extent=30, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=150, extent=30, outline="black", width=1, fill="green")
            ]
        ]

        self.rover = self.create_rectangle(rover_xy, fill="orange")

        #self.update([0, 11, 21, 31, 41, 31])
        #self.reset()

    # NOTE: Distance array are from right (0°) to left (180°) view from back to front
    def update(self, distance_vector):
        self.reset()
        for i in range(0, 6):
            if distance_vector[i] in range(30, 40):
                self.itemconfig(self.sector[0][i], fill="red")

            if distance_vector[i] in range(20, 30):
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")

            if distance_vector[i] in range(10, 20):
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")

            if distance_vector[i] in range(0, 10):
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")
                self.itemconfig(self.sector[3][i], fill="red")

    def reset(self):
        for i in range(0, 4):
            for k in range(0, 6):
                self.itemconfig(self.sector[i][k], fill="green")
