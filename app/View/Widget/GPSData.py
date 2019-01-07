from tkinter import *

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class GPSData(Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.gps_label = self.create_text(
            (CANVAS_WIDTH/2, 30), text="GPS DATA", fill="white", font=("default", 30))

        self.state_label = self.create_text(
            (105, 70), text="State: ", fill="white", font=("default", 30))
        self.state_value = self.create_text(
            (105 + 90, 70), text="N/A", fill="red", font=("default", 30))

        self.speed_label = self.create_text(
            (105, 105), text="Speed: ", fill="white", font=("default", 30))
        self.speed_value = self.create_text(
            (105 + 120, 105), text="N/A", fill="red", font=("default", 30))

        self.altitude_label = self.create_text(
            (95, 140), text="Alt: ", fill="white", font=("default", 30))
        self.altitude_value = self.create_text(
            (105 + 90, 140), text="N/A", fill="red", font=("default", 30))

        self.latitude_label = self.create_text(
            (95, 175), text="Lat: ", fill="white", font=("default", 30))
        self.latitude_value = self.create_text(
            (105 + 100, 175), text="N/A", fill="green", font=("default", 30))

        self.longitude_label = self.create_text(
            (95, 210), text="Long: ", fill="white", font=("default", 30))
        self.longitude_value = self.create_text(
            (105 + 100, 210), text="N/A", fill="green", font=("default", 30))

    def update(self, gps_data):
        # print(gps_data)
        if gps_data["state"] == 0:
            self.itemconfig(self.state_value,
                            text="Not Fix", fill="red")
            self.itemconfig(self.speed_value,
                            text="N/A", fill="red")
            self.itemconfig(self.altitude_value,
                            text="N/A", fill="red")
            self.itemconfig(self.latitude_value,
                            text="N/A", fill="red")
            self.itemconfig(self.longitude_value,
                            text="N/A", fill="red")

        else:
            self.itemconfig(self.state_value,
                            text="Fix", fill="green")
            self.itemconfig(self.speed_value,
                            text=(
                                str(round(gps_data["speed"]*1.8, 1)) + " Km/h"))
            self.itemconfig(self.altitude_value,
                            text=(str(gps_data["altitude"]) + " mslm"))
            self.itemconfig(self.latitude_value,
                            text=(str(round(self.parseCoord(gps_data["latitude"]), 3))))
            self.itemconfig(self.longitude_value,
                            text=(str(round(self.parseCoord(gps_data["longitude"]), 3))))

    # COORD:
    # Lat: DDMM.MMMM
    # Lon: DDDMM.MMMM
    # Speed is in knot

    def parseCoord(self, coord):
        coord = str(coord)
        splitted = coord.split(".")
        integer = splitted[0]
        if(len(integer) == 1 or len(integer) == 2):
            return
        if(len(integer) == 3):
            integer = "00" + integer
        if(len(integer) == 4):
            integer = "0" + integer
        minute = float(integer[3:]) + float("0." + splitted[1])
        deg = int(integer[0:3])
        val = deg + minute/60
        return val
