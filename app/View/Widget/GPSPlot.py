from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300


class GPSPlot(FigureCanvasTkAgg):
    def __init__(self, root):
        super()
        self.gps_coord = {
            "lat": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "lon": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }

        self.fig = Figure(figsize=(3.125, 3.125), dpi=100)

        self.fig.add_subplot(111).plot(self.gps_coord["lat"], self.gps_coord["lon"])

        # A tk.DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        #toolbar = NavigationToolbar2Tk(canvas, root)
        #toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
