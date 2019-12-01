from tkinter import *
from tkinter import messagebox
from app.View.MainView import *
from app.Network import *
from app.Camera import *
from app.Joystick import *
import json

REFRESH_RATE = 100
ENABLE_JOYSTCK = True
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
        self.app.geometry("1540x620")  # 900x700
        self.app.configure(background="#282828")

        self.speed = SPEED
        self.turning_speed = TURNING_SPEED
        self.auto_speed = AUTO_SPEED
        self.auto_turning_speed = AUTO_TURNING_SPEED

        


        self.mainView = MainView(self.app, self)
        
        if ENABLE_NETWORK:
            self.network = Network(self)
            self.network.connect()
           # self.updateData()

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

    def updateData(self):
        s = bytes([0x01, 0x00])
        received = self.socket_connector.getData(s)
        if not len(received) == 0:
            # print(received)
            data = json.loads(received)
            self.mainView.updateRadar(data["radar"])
            self.mainView.updateMotorData(data["motor"], data["battery"])
            self.mainView.updateGPSData(data["gps"])
            self.mainView.updateCompass(data["compass"])
            self.mainView.getButtons().updateMode(data["mode"])

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
                'commands':[
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
                    'value': 1
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

    def goRight(self):
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
                    'value': self.speed
                },
                {
                    'command': 'LM_speed',
                    'value': self.speed
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

    '''def setRemoteMode(self):
        s = bytes([0x02, 0x00])
        self.socket_connector.sendCommand(s)

    def setAutoMode(self):
        s = bytes([0x02, 0x01])
        self.socket_connector.sendCommand(s)

    def goForward(self):
        # MOTOR1 (RIGHT) DIRECTION
        s = bytes([0x10, 0x00])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) DIRECTION
        s = bytes([0x11, 0x00])
        self.socket_connector.sendCommand(s)

        # MOTOR1 (RIGHT) POWER
        s = bytes([0x12, self.speed])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) POWER
        s = bytes([0x13, self.speed])
        self.socket_connector.sendCommand(s)

    def goBackward(self):
        # MOTOR1 (RIGHT) DIRECTION
        s = bytes([0x10, 0x01])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) DIRECTION
        s = bytes([0x11, 0x01])
        self.socket_connector.sendCommand(s)

        # MOTOR1 (RIGHT) POWER
        s = bytes([0x12, self.speed])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) POWER
        s = bytes([0x13, self.speed])
        self.socket_connector.sendCommand(s)

    def goLeft(self):
        # MOTOR1 (RIGHT) DIRECTION
        s = bytes([0x10, 0x00])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) DIRECTION
        s = bytes([0x11, 0x01])
        self.socket_connector.sendCommand(s)

        # MOTOR1 (RIGHT) POWER
        s = bytes([0x12, self.turning_speed])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) POWER
        s = bytes([0x13, self.turning_speed])
        self.socket_connector.sendCommand(s)

    def goRight(self):
        # MOTOR1 (RIGHT) DIRECTION
        s = bytes([0x10, 0x01])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) DIRECTION
        s = bytes([0x11, 0x00])
        self.socket_connector.sendCommand(s)

        # MOTOR1 (RIGHT) POWER
        s = bytes([0x12, self.turning_speed])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) POWER
        s = bytes([0x13, self.turning_speed])
        self.socket_connector.sendCommand(s)

    def stop(self):
        # MOTOR1 (RIGHT) POWER
        s = bytes([0x12, 0])
        self.socket_connector.sendCommand(s)

        # MOTOR2 (LEFT) POWER
        s = bytes([0x13, 0])
        self.socket_connector.sendCommand(s)
'''
