from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class GPSPlot():
    def __init__(self, root):
         # Widget will be update by gps data

        self.gps_coord = {
            "lat": [],
            "lon": []
        }

        self.fig = Figure(figsize=(2*2.5, 3),
                          dpi=100, facecolor="#282828")

        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_facecolor("#282828")
        self.ax1.set_title("TRACK ROUTE", color="white")

        self.ax1.set_xlabel("Longitudine", color="white")
        self.ax1.set_ylabel("Latitudine", color="white")
        self.ax1.tick_params(labelcolor="white")

        self.ax1.autoscale(enable=True)

        self.coord_line = Line2D([], [], color="white", linewidth=2)
        self.current_pos = Line2D(
            [], [], color="red", marker="o", markeredgecolor="r")

        self.home_point = Line2D(
            [], [], color="green", marker="^", markeredgecolor="g")

        self.ax1.add_line(self.coord_line)
        self.ax1.add_line(self.current_pos)
        self.ax1.add_line(self.home_point)

        self.ax1.set_xlim(-10, 10)
        self.ax1.set_ylim(-10, 10)
        #self.ax1.set_aspect("equal", "datalim")
        self.coord_line.set_data(0, 0)
        self.current_pos.set_data(0, 0)
        self.home_point.set_data(0, 0)

        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.first_data = True

        self.home_coord = {
            "lat": 0,
            "lon": 0
        }

        #self.testPlot()

    def updatePlot(self, lat, lon):
        if lat != None and lon != None:
            lat = round(lat, 5)
            lon = round(lon, 5)
            # Filter duplicate point
            if (len(self.gps_coord["lat"]) > 0 or len(self.gps_coord["lon"]) > 0) and self.gps_coord["lat"][-1] == lat and self.gps_coord["lon"][-1] == lon:
                return

            # first point -> set home
            if (len(self.gps_coord["lat"]) == 0 or len(self.gps_coord["lon"]) == 0):
                self.home_coord["lat"] = lat
                self.home_coord["lon"] = lon

            self.gps_coord["lat"].append(lat)
            self.gps_coord["lon"].append(lon)

            # Add new position coordinate to the line of track
            self.coord_line.set_data(
                self.gps_coord["lon"], self.gps_coord["lat"])

            self.ax1.set_xlim(np.amin(self.gps_coord["lon"]) - 0.0001, np.amax(
                self.gps_coord["lon"]) + 0.0001)
            self.ax1.set_ylim(np.amin(self.gps_coord["lat"]) - 0.0001, np.amax(
                self.gps_coord["lat"]) + 0.0001)

            # Set current
            self.current_pos.set_data(
                self.gps_coord["lon"][-1], self.gps_coord["lat"][-1])

            #self.home_point.set_data(
            #    self.home_coord["lat"], self.home_coord["lon"])

            self.home_point.set_data(
                self.gps_coord["lon"][0], self.gps_coord["lat"][0])

            self.canvas.draw()

    def testPlot(self):
        lat = 45.63192
        lon = 8.82720
        for i in range(0, 10):
            self.updatePlot(lat, lon)
            lat += 0.00002
            lon += 0.00002

        for i in range(0, 10):
            self.updatePlot(lat, lon)
            lat -= 0.00001
            lon += 0.00008

        for i in range(0, 10):
            self.updatePlot(lat, lon)
            lat += 0.00003
            lon -= 0.00005
