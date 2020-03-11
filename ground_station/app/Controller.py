from tkinter import *
from tkinter import messagebox
from app.View.MainView import *
from app.Network import *
from app.Camera import *
from app.Joystick import *
from app.View.ControllerWindow import *
from app.View.Console import *

import json
import sys
from queue import *
import cv2
import base64
import numpy as np
import os
import time

REFRESH_RATE = 100
ENABLE_NETWORK = True
ENABLE_CAMERA = True

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
        self.app.geometry("1300x620")  # 900x700
        self.app.configure(background="#282828")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.speed = SPEED
        self.turning_speed = TURNING_SPEED
        self.auto_speed = AUTO_SPEED
        self.auto_turning_speed = AUTO_TURNING_SPEED

        self.network = Network(self)
        self.camera_queue = Queue(30)
        self.camera = Camera()
        self.camera.start()

        self.mainView = MainView(self.app, self)

        self.joystick = Joystick(self)
        self.joystick_enabled = self.joystick.init()

        # set default scale value
        self.mainView.getButtons().updateSpeed(SPEED)
        self.mainView.getButtons().updateTurningSpeed(TURNING_SPEED)
        self.mainView.getButtons().updateAutoSpeed(AUTO_SPEED)
        self.mainView.getButtons().updateAutoTurningSpeed(AUTO_TURNING_SPEED)

        self.mainView.pack()  # let here otherwise crash

        self.console = Console()
        self.console.println("ROVER GROUND STATION v1.0")
        self.console.println("www.matteoformentin.com")
        self.console.println()
        self.console.println("JOYSTICK ENABLED") if self.joystick_enabled else self.console.println(
            "JOYSTICK NOT CONNECTED")

        self.app.after(2000, self.initNetwork)

    def run(self):
        self.app.mainloop()

    def initNetwork(self):
        self.console.println("Connecting to Rover...")
        self.network.connect()
        self.console.println("Getting data...")
        self.updateData()
        self.console.println("Done.")
        self.console.println("Starting camera stream...")
        self.startVideoStream()
        self.updateCamera()
        self.console.println("Done.")
        self.console.println()

    def on_closing(self):
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.quitApp()

    def quitApp(self):
        if ENABLE_NETWORK:
            self.network.disconnect()
        if ENABLE_CAMERA:
            self.camera.stop()

        self.app.destroy()
        sys.exit()

    def showControllerWindow(self):
        self.top = ControllerWindow(self)

    def showCheckConnectionDialog(self):
        messagebox.showerror(
            "Connection Error",
            "Please make sure to be connected to the rover Wi-Fi and restart Ground Station"
        )
        self.console.println("Connection Error")
        self.quitApp()

    def showCheckControllerDialog(self):
        messagebox.showerror(
            "Controller not Found",
            "Use the virtual controller to control the rover"
        )
        # self.quitApp()

    def updateCamera(self):
        self.mainView.updateCameraWindow(
            self.camera.getFrame(), self.camera.getFPS())
        self.app.after(15, self.updateCamera)

    def setSpeed(self, speed):
        self.speed = speed
        self.mainView.getButtons().updateSpeed(self.speed)
        self.console.println("Speed setted to " + str(self.speed))

    def setTurningSpeed(self, speed):
        self.turning_speed = speed
        self.mainView.getButtons().updateTurningSpeed(self.turning_speed)
        self.console.println("Turning speed setted to " +
                             str(self.turning_speed))

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

        if not len(received) == 0:
            data = json.loads(received)
            self.mainView.updateRadar(data["radar"])
            self.mainView.updateMotorData(data["motor"], 100)
            self.mainView.updateGPSData(data["gps"])
            self.mainView.updateCompass(data["compass"])

            self.console.clearData()
            self.console.printData("DATA")

            self.console.printData(
                "Radar: " + "R" + str(data["radar"][0]) + " C" + str(data["radar"][1]) + " L" + str(data["radar"][2]))

            self.console.printData(
                "Compass: " + str(data["compass"]))

            self.console.printData("Motors:")
            self.console.printData(
                "left_power: " + str(data["motor"]["left_power"]))
            self.console.printData(
                "right_power: " + str(data["motor"]["right_power"]))
            self.console.printData(
                "left_tick: " + str(data["motor"]["left_tick"]))
            self.console.printData(
                "right_tick: " + str(data["motor"]["right_tick"]))
            self.console.printData(
                "left_rpm: " + str(data["motor"]["left_rpm"]))
            self.console.printData(
                "right_rpm: " + str(data["motor"]["right_rpm"]))

            self.console.printData("GPS:")
            self.console.printData(
                "fix: " + str(data["gps"]["fix"]))
            self.console.printData(
                "fix_quality: " + str(data["gps"]["fix_quality"]))
            self.console.printData(
                "satellites: " + str(data["gps"]["satellites"]))
            self.console.printData(
                "latitude: " + str(data["gps"]["latitude"]))
            self.console.printData(
                "longitude: " + str(data["gps"]["longitude"]))
            self.console.printData(
                "speed: " + str(data["gps"]["speed"]))
            self.console.printData(
                "altitude: " + str(data["gps"]["altitude"]))

            # self.mainView.getButtons().updateMode(data["mode"])

        self.app.after(REFRESH_RATE, self.updateData)

    def startVideoStream(self):
        data = {
            'commands': [
                {
                    'command': 'C_Stream_S',
                    'value': self.camera.getIp()
                }
            ]
        }

        self.network.sendData(json.dumps(data))
        self.camera.startVideoStream()

    def takePhoto(self):
        data = {
            'commands': [
                {
                    'command': 'C_Take_Photo'
                }
            ]
        }

        self.console.println("Taking photo...")
        self.network.sendData(json.dumps(data))
        received = self.network.getData()
        b64 = base64.b64decode(received)
        npimg = np.fromstring(b64, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)

        image = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.console.println("Saving photo...")
        cv2.imwrite(os.path.expanduser('~') +
                    '/Desktop/photo-' + timestr + '.jpg', image)
        self.console.println("Done.")
        self.console.println()

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
        self.console.println("Going Forward...")


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
        self.console.println("Going Backward...")


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
        self.console.println("Turning Left...")


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
        self.console.println("Turning Right...")


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
        self.console.println("Stop")
