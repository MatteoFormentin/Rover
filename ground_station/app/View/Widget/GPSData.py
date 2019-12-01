from tkinter import *

CANVAS_WIDTH = 250
CANVAS_HEIGHT = 300


class GPSData(Canvas):
    def __init__(self, master, gps_plot):
        super().__init__(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#282828", borderwidth=0,
                         highlightthickness=0)

        self.gps_plot = gps_plot

        self.gps_label = self.create_text(
            (CANVAS_WIDTH/2, 30), text="GPS", fill="white", font=("default", 30))

        self.state_label = self.create_text(
            (90, 70), text="State: ", fill="white", font=("default", 30), anchor="e")
        self.state_value = self.create_text(
            (90 + 100, 70), text="N/A", fill="red", font=("default", 15), anchor="e")

        self.speed_label = self.create_text(
            (90, 105), text="Spd: ", fill="white", font=("default", 30), anchor="e")
        self.speed_value = self.create_text(
            (90 + 100, 105), text="N/A", fill="red", font=("default", 15), anchor="e")

        self.altitude_label = self.create_text(
            (90, 140), text="Alt: ", fill="white", font=("default", 30), anchor="e")
        self.altitude_value = self.create_text(
            (90 + 100, 140), text="N/A", fill="red", font=("default", 15), anchor="e")

        self.latitude_label = self.create_text(
            (90, 175), text="Lat: ", fill="white", font=("default", 30), anchor="e")
        self.latitude_value = self.create_text(
            (90 + 100, 175), text="N/A", fill="red", font=("default", 15), anchor="e")

        self.longitude_label = self.create_text(
            (90, 210), text="Long: ", fill="white", font=("default", 30), anchor="e")
        self.longitude_value = self.create_text(
            (90 + 100, 210), text="N/A", fill="red", font=("default", 15), anchor="e")

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
            lat = self.parseCoord(gps_data["latitude"])
            lon = self.parseCoord(gps_data["longitude"])
            self.itemconfig(self.state_value,
                            text="Fix", fill="green")
            self.itemconfig(self.speed_value,
                            text=(str(round(gps_data["speed"]*1.8, 1)) + " Km/h"))
            self.itemconfig(self.altitude_value,
                            text=(str(gps_data["altitude"]) + " mslm"))
            self.itemconfig(self.latitude_value, text=(str(lat)))
            self.itemconfig(self.longitude_value, text=(str(lon)))
            self.gps_plot.updatePlot(lat, lon)

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
        return round(val, 4)
