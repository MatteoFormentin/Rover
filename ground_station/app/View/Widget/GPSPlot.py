from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class GPSPlot():
    def __init__(self, root):
         # Widget will be update by gps data
        

        self.gps_coord = {
            "lat": [],
            "lon": []
        }

        self.fig = Figure(figsize=(2*3.125, 3.125),
                          dpi=100, facecolor="#282828")

        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_facecolor("#282828")
        self.ax1.set_title("TRACK ROUTE", color="white")

        self.ax1.set_xlabel("Longitudine", color="white")
        self.ax1.set_ylabel("Latitudine", color="white")
        self.ax1.tick_params(labelcolor="white")

        self.coord_line = Line2D([], [], color="white", linewidth=2)
        self.current_pos = Line2D(
            [], [], color="red", marker="o", markeredgecolor="r")

        self.ax1.add_line(self.coord_line)
        self.ax1.add_line(self.current_pos)

        self.ax1.set_xlim(-10, 10)
        self.ax1.set_ylim(-10, 10)
        #self.ax1.set_aspect("equal", "datalim")
        self.coord_line.set_data(0, 0)
        self.current_pos.set_data(0, 0)

        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def updatePlot(self, lat, lon):
        if lat != None and lon != None and (self.gps_coord["lat"][-1] != lat and self.gps_coord["lon"][-1] != lon):
            self.gps_coord["lat"].append(lat)
            self.gps_coord["lon"].append(lon)

            self.coord_line.set_data(
                self.gps_coord["lon"], self.gps_coord["lat"])

            self.ax1.set_xlim(np.amin(self.gps_coord["lon"]), np.amax(
                self.gps_coord["lon"]))
            self.ax1.set_ylim(np.amin(self.gps_coord["lat"]), np.amax(
                self.gps_coord["lat"]))

            self.current_pos.set_data(
                self.gps_coord["lon"][-1], self.gps_coord["lat"][-1])

            print(self.gps_coord["lat"])
            print(self.gps_coord["lon"])

            self.canvas.draw()
