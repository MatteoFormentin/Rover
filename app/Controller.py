from tkinter import *
from app.View.MainView import *
from socket_thread.SocketThread import *
class Controller:
    def __init__(self):
        self.app = Tk()
        self.app.resizable(width=False, height=False)
        self.app.geometry("1000x700")
        self.app.configure(background="#282828")

        self.mainView = MainView(self.app, self)
        self.mainView.pack()

        self.socket_thread = SocketThread(self)
        self.socket_thread.start()

    def run(self):
        self.app.mainloop()

    def updateRadar(self, distance_vector):
        self.mainView.updateRadar(distance_vector)
