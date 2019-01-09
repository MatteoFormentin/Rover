import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

gps_coord = {
    "lat": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "lon": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}


fig = Figure(figsize=(5, 4), dpi=100)
fig.add_subplot(111).plot(gps_coord["lat"], gps_coord["lon"])

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

#toolbar = NavigationToolbar2Tk(canvas, root)
#toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
tkinter.mainloop()
