from tkinter import *
from tkinter import messagebox
from app.View.MainView import *
from app.SocketConnector import *
from app.Joystick import *

REFRESH_RATE = 50
ENABLE_JOYSTCK = False
ENABLE_NETWORK = False


class Controller:
    def __init__(self):
        self.app = Tk()
        self.app.resizable(width=False, height=False)
        self.app.wm_title("Rover Ground Station")
        self.app.wm_iconname("Rover Ground Station")
        self.app.geometry("940x620")  # 900x700
        self.app.configure(background="#282828")

        self.mainView = MainView(self.app, self)
        self.mainView.pack()

        self.socket_connector = SocketConnector(self)

        if ENABLE_JOYSTCK:
            self.joystick = Joystick(self)
            self.joystick.processEvent()
        else:
            self.app.bind("<Up>", self.upPressed)
            self.app.bind("<Down>", self.downPressed)
            self.app.bind("<Left>", self.leftPressed)
            self.app.bind("<Right>", self.rightPressed)

            self.app.bind("<space>", self.shiftPressed)
            self.app.bind("o", self.oPressed)
            self.app.bind("p", self.pPressed)

        if(ENABLE_NETWORK):
            self.socket_connector.connectToRover()
            self.updateData()

    def run(self):
        self.app.mainloop()
        #except UnicodeDecodeError:

    def updateData(self):
        self.socket_connector.getData()
        self.app.after(REFRESH_RATE, self.updateData)

    def showCheckConnectionDialog(self):
        messagebox.showerror(
            "Errore Connessione",
            "Assicurarsi di essere connessi alla rete WiFi del rover!"
        )

    def showCheckControllerDialog(self):
        messagebox.showerror(
            "Controller non Connesso",
            "Collegare un Controller!"
        )

    def updateRadar(self, distance_vector):
        self.mainView.updateRadar(distance_vector)

    def updateMotorData(self, motor_data, battery):
        self.mainView.updateMotorData(motor_data, battery)

    def updateGPSData(self, gps_data):
        self.mainView.updateGPSData(gps_data)

    def updateCompass(self, heading):
        self.mainView.updateCompass(heading)

    def goForward(self):
        self.socket_connector.sendCommand("W")

    def goBackward(self):
        self.socket_connector.sendCommand("S")

    def goLeft(self):
        self.socket_connector.sendCommand("A")

    def goRight(self):
        self.socket_connector.sendCommand("D")

    def stop(self):
        self.socket_connector.sendCommand("X")

    def upSpeed(self):
        self.socket_connector.sendCommand("P")

    def downSpeed(self):
        self.socket_connector.sendCommand("O")

    def ringBuzzer(self):
        self.socket_connector.sendCommand("K")

    def stopBuzzer(self):
        self.socket_connector.sendCommand("L")

    # Handle keyboard mode command

    def upPressed(self, event):
        self.goForward()

    def downPressed(self, event):
        self.goBackward()

    def leftPressed(self, event):
        self.goLeft()

    def rightPressed(self, event):
        self.goRight

    def shiftPressed(self, event):
        self.stop()

    def oPressed(self, event):
        self.downSpeed()

    def pPressed(self, event):
        self.upSpeed()
