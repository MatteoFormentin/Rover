from app.View.Widget.Radar import *

class MainView(Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.connection_state = 0

        self.radar = Radar(self)
        self.radar.grid(row=0, column=2)

    def updateRadar(self, distance_vector):
        self.radar.update(distance_vector)
