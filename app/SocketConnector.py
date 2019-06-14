import threading
import time
import json
import socket
import sys

HOST = '192.168.0.1'
PORT = 8080


class SocketConnector():
    def __init__(self, controller):
        self.state = None
        self.controller = controller

        self.rover_socket = None

        self.last_command = None
        self.connection_state = False

    def stop(self):
        self.close()
        self.state = False

    def connectToRover(self):
        connected = False
        while not connected:
            try:
                print("provo a connettermi")
                self.rover_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.rover_socket.settimeout(5)
                self.rover_socket.connect((HOST, PORT))
                connected = True
                self.connection_state = True
                print("connesso")
            except (socket.timeout):
                print("errore timeout")
                connected = False
                self.connection_state = False
                self.controller.showCheckConnectionDialog()
            except OSError:
                print("Rover non acceso.")
                self.controller.showCheckConnectionDialog()

    def close(self):
        self.rover_socket.close()

    def getData(self):
        try:
            self.rover_socket.sendall("U".encode('ASCII'))
            received = self.rover_socket.recv(1024).decode('ASCII')

            if not len(received) == 0:
                #print(received)
                data = json.loads(received)
                self.controller.updateRadar(data["radar"])
                self.controller.updateMotorData(data["motor"], data["battery"])
                self.controller.updateGPSData(data["gps"])
                self.controller.updateCompass(data["compass"])
                self.controller.updateMode(data["mode"])

        except socket.timeout:
            print("Connessione chiusa")
            self.connection_state = False
            self.connectToRover()

        except:
            print("Generic Error - get data")
            self.connection_state = False
            self.connectToRover()

    def sendCommand(self, to_send):
        if not self.connection_state:
            return
        '''if self.last_command == to_send:
            print("duplicate")
            return'''
        try:
            self.rover_socket.sendall(to_send.encode('ASCII'))
            self.last_command = to_send
        except socket.timeout:
            print("Connessione chiusa - Send command")
            self.connection_state = False
            self.connectToRover()

        except:
            print("Generic Error - Send command")
