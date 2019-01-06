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
            (105 + 90, 105), text="N/A", fill="red", font=("default", 30))

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
                            text=(str(gps_data["speed"]*1.8) + " Km/h"))
            self.itemconfig(self.altitude_value,
                            text=(str(gps_data["altitude"]) + " mslm"))
            self.itemconfig(self.latitude_value,
                            text=(str(self.parseLat(gps_data["latitude"]))))
            self.itemconfig(self.longitude_value,
                            text=(str(self.parseLon(gps_data["longitude"]))))

    # COORD:
    # Lat: DDMM.MMMM
    # Lon: DDDMM.MMMM
    # Speed is in knot

    def parseLat(self, coord):
        deg = int(coord[0:1])
        deg += float(coord[2:-1])/60
        return deg

    def parseLon(self, coord):
        deg = int(coord[0:2])
        deg += float(coord[3:-1])/60
        return deg
