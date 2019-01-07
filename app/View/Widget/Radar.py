from tkinter import *

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class Radar(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        range_xy = 10, 40, 290, 320

        r = 15

        xy_eight = 10+7*r, 40+7*r, 290-7*r, 320-7*r

        xy_seven = 10+6*r, 40+6*r, 290-6*r, 320-6*r

        xy_six = 10+5*r, 40+5*r, 290-5*r, 320-5*r

        xy_five = 10+4*r, 40+4*r, 290-4*r, 320-4*r

        xy_four = 10+3*r, 40+3*r, 290-3*r, 320-3*r

        xy_three = 10+2*r, 40+2*r, 290-2*r, 320-2*r

        xy_two = 10+r, 40+r, 290-r, 320-r

        xy_one = 10, 40, 290, 320

        rover_xy = 130, 130+25, 170, 170+25

       # self.range = self.create_arc(
        #    range_xy, start=0, extent=180, outline="red", style="arc", fill="red")

        self.sector = [
            [
                self.create_arc(
                    xy_one, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_one, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_two, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_two, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_three, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_three, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_four, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_four, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_five, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_five, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_five, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_six, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_six, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_six, start=110, extent=40, outline="black", width=1, fill="green"),
            ],
            [
                self.create_arc(
                    xy_seven, start=30, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_seven, start=70, extent=40, outline="black", width=1, fill="green"),
                self.create_arc(
                    xy_seven, start=110, extent=40, outline="black", width=1, fill="green"),
            ]
        ]

        self.create_arc(xy_eight, start=30, extent=120,
                        outline="#282828", width=0, fill="#282828")
        self.rover = self.create_rectangle(rover_xy, fill="orange")

        self.reset()

    # NOTE: Distance array are from right (0°) to left (180°) view from back to front
    def update(self, distance_vector):
        self.reset()
        for i in range(0, 3):

            d = distance_vector[i]

            if 80 <= d < 100:
                self.itemconfig(self.sector[0][i], fill="red")

            if 60 <= d < 80:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red") 

            if 40 <= d < 60:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")

            if 30 <= d < 40:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")
                self.itemconfig(self.sector[3][i], fill="red")

            if 20 <= d < 30:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")
                self.itemconfig(self.sector[3][i], fill="red")
                self.itemconfig(self.sector[4][i], fill="red")

            if 10 <= d < 20:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")
                self.itemconfig(self.sector[3][i], fill="red")
                self.itemconfig(self.sector[4][i], fill="red")
                self.itemconfig(self.sector[5][i], fill="red")

            if 0 <= d < 10:
                self.itemconfig(self.sector[0][i], fill="red")
                self.itemconfig(self.sector[1][i], fill="red")
                self.itemconfig(self.sector[2][i], fill="red")
                self.itemconfig(self.sector[3][i], fill="red")
                self.itemconfig(self.sector[4][i], fill="red")
                self.itemconfig(self.sector[5][i], fill="red")
                self.itemconfig(self.sector[6][i], fill="red")

    def reset(self):
        for i in range(0, 7):
            for k in range(0, 3):
                self.itemconfig(self.sector[i][k], fill="green")
