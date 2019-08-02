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
               # self.rover_socket.settimeout(1)
                #self.rover_socket.setblocking(1)
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

    def getData(self, to_send):
        try:
            self.rover_socket.sendall(to_send)
            received = self.rover_socket.recv(1024).decode('ASCII')
            return received

        except socket.timeout:
            print("Connessione chiusa")
            self.connection_state = False
            self.close()
            self.connectToRover()
            return ""

        except Exception as e:
            print(e)
            print("Generic Error - get data")
            self.connection_state = False
            self.close()
            self.connectToRover()
            return ""

    def sendCommand(self, to_send):
        if not self.connection_state:
            return
        '''if self.last_command == to_send:
            print("duplicate")
            return'''
        try:
            self.rover_socket.sendall(to_send)
            self.last_command = to_send
        except socket.timeout:
            print("Connessione chiusa - Send command")
            self.connection_state = False
            self.connectToRover()

        except Exception as e:
            print("Generic Error - Send command")
            self.connection_state = False
            self.close()
            self.connectToRover()
            print(e)
