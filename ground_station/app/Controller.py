from tkinter import *
from tkinter import messagebox
from app.View.MainView import *
from app.Network import *
from app.Camera import *
from app.Joystick import *
import json
import sys

REFRESH_RATE = 100
ENABLE_JOYSTCK = True
ENABLE_NETWORK = True
ENABLE_CAMERA = False

SPEED = 100
TURNING_SPEED = 80
AUTO_SPEED = 0
AUTO_TURNING_SPEED = 0


class Controller:
    def __init__(self):
        self.app = Tk()
        self.app.resizable(width=False, height=False)
        self.app.wm_title("Rover Ground Station")
        self.app.wm_iconname("Rover Ground Station")
        self.app.geometry("1420x620")  # 900x700
        self.app.configure(background="#282828")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.speed = SPEED
        self.turning_speed = TURNING_SPEED
        self.auto_speed = AUTO_SPEED
        self.auto_turning_speed = AUTO_TURNING_SPEED

        self.mainView = MainView(self.app, self)

        if ENABLE_NETWORK:
            self.network = Network(self)
            self.network.connect()
            print("First update...")
            self.updateData()
            print("Done!")

        if ENABLE_JOYSTCK:
            self.joystick = Joystick(self)
            self.joystick.processEvent()

        if ENABLE_CAMERA:
            self.camera = Camera()
            self.camera.start()
            self.updateCamera()

        # set default scale value
        self.mainView.getButtons().updateSpeed(SPEED)
        self.mainView.getButtons().updateTurningSpeed(TURNING_SPEED)
        self.mainView.getButtons().updateAutoSpeed(AUTO_SPEED)
        self.mainView.getButtons().updateAutoTurningSpeed(AUTO_TURNING_SPEED)

        self.mainView.pack()

    def run(self):
        self.app.mainloop()
        # except UnicodeDecodeError:

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
           self.quitApp()

    def quitApp(self):
        if ENABLE_NETWORK:
            self.network.disconnect()
        if ENABLE_CAMERA:
            self.camera.stop()
        if ENABLE_JOYSTCK:
            self.controller.stop()
        self.app.destroy()
        sys.exit()

    def updateData(self):
        data = {
            'commands': [
                {
                    'command': 'update'
                }
            ]
        }

        self.network.sendData(json.dumps(data))
        received = self.network.getData()
        print(received)

        if not len(received) == 0:
            print(received)
            data = json.loads(received)
           # print(data["radar"])
           # self.mainView.updateRadar(data["radar"])
            self.mainView.updateMotorData(data["motor"], 100)
            # self.mainView.updateGPSData(data["gps"])
            # self.mainView.updateCompass(data["compass"])
            # self.mainView.getButtons().updateMode(data["mode"])

        self.app.after(REFRESH_RATE, self.updateData)

    def showCheckConnectionDialog(self):
        messagebox.showerror(
            "Connection Error",
            "Please make sure to be connected to the rover Wi-Fi and restart Ground Station"
        )
        self.quitApp()

    def showCheckControllerDialog(self):
        messagebox.showerror(
            "Controller not Found",
            "Connect the rover controller and restart Ground Station"
        )
        self.quitApp()

    def updateCamera(self):
        self.mainView.updateCameraWindow(self.camera.getFrame())
        self.app.after(1, self.updateCamera)

    def setSpeed(self, speed):
        self.speed = speed
        self.mainView.getButtons().updateSpeed(self.speed)

    def setTurningSpeed(self, speed):
        self.turning_speed = speed
        self.mainView.getButtons().updateTurningSpeed(self.turning_speed)

    def setAutoSpeed(self, speed):
        self.auto_speed = speed
        self.mainView.getButtons().updateAutoSpeed(self.auto_speed)

    def setAutoTurningSpeed(self, speed):
        self.auto_turning_speed = speed
        self.mainView.getButtons().updateAutoTurningSpeed(self.auto_turning_speed)

    def getSpeed(self):
        return self.speed

    def getTurningSpeed(self):
        return self.turning_speed

    def getAutoSpeed(self):
        return self.auto_speed

    def getAutoTurningSpeed(self):
        return self.auto_turning_speed

    # COMMAND SEND
    def setRemoteMode(self):
        pass

    def setAutoMode(self):
        pass

    def goForward(self):
        data = {
            'commands': [
                {
                    'command': 'RM_dir',
                    'value': 0
                },
                {
                    'command': 'LM_dir',
                    'value': 0
                },
                {
                    'command': 'RM_speed',
                    'value': self.speed
                },
                {
                    'command': 'LM_speed',
                    'value': self.speed
                }
            ]
        }

        self.network.sendData(json.dumps(data))

    def goBackward(self):
        data = {
            'commands': [
                {
                    'command': 'RM_dir',
                    'value': 1
                },
                {
                    'command': 'LM_dir',
                    'value': 1
                },
                {
                    'command': 'RM_speed',
                    'value': self.speed
                },
                {
                    'command': 'LM_speed',
                    'value': self.speed
                }
            ]
        }

        self.network.sendData(json.dumps(data))

    def goLeft(self):
        data = {
            'commands': [
                {
                    'command': 'RM_dir',
                    'value': 0
                },
                {
                    'command': 'LM_dir',
                    'value': 1
                },
                {
                    'command': 'RM_speed',
                    'value': self.turning_speed
                },
                {
                    'command': 'LM_speed',
                    'value': self.turning_speed
                }
            ]
        }

        self.network.sendData(json.dumps(data))

    def goRight(self):
        data = {
            'commands': [
                {
                    'command': 'RM_dir',
                    'value': 1
                },
                {
                    'command': 'LM_dir',
                    'value': 0
                },
                {
                    'command': 'RM_speed',
                    'value': self.turning_speed
                },
                {
                    'command': 'LM_speed',
                    'value': self.turning_speed
                }
            ]
        }

        self.network.sendData(json.dumps(data))

    def stop(self):
        data = {
            'commands': [
                {
                    'command': 'RM_speed',
                    'value': 0
                },
                {
                    'command': 'LM_speed',
                    'value': 0
                }
            ]
        }

        self.network.sendData(json.dumps(data))
