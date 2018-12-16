from tkinter import *
from tkinter import messagebox
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
        #self.socket_thread.start()

        self.app.bind("<Up>", self.upPressed)
        self.app.bind("<Down>", self.downPressed)
        self.app.bind("<Left>", self.leftPressed)
        self.app.bind("<Right>", self.rightPressed)

        self.app.bind("<space>", self.shiftPressed)


        self.updateData()

    def run(self):
        self.app.mainloop()

    def updateData(self):
        self.socket_thread.getData()
        self.app.after(500, self.updateData)

    def showCheckConnectionDialog(self):
        messagebox.showerror(
            "Errore Connessione",
            "Controllare la connessione e premere ok per riprovare"
        )

    def shiftPressed(self, event):
        self.socket_thread.sendCommand("X")
        print("X")
         
    def upPressed(self, event):
        self.socket_thread.sendCommand("W")

    def downPressed(self, event):
        self.socket_thread.sendCommand("S")
        print("downPressed")

    def leftPressed(self, event):
        self.socket_thread.sendCommand("A")
        print("leftPressed")

    def rightPressed(self, event):
        self.socket_thread.sendCommand("D")
        print("rightPressed")

    def keyboardController(self, key):
        pass

    def updateRadar(self, distance_vector):
        self.mainView.updateRadar(distance_vector)
