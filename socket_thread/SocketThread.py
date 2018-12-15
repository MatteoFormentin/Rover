import threading
import time
import json
import socket
import sys

HOST = '10.0.0.123'    # The remote host
PORT = 8080              # The same port as used by the server

# NOTE: Data are exchanged ONLY in JSON format


class SocketThread(threading.Thread):
    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.name = "SocketThread"
        self.state = None

        self.controller = controller

        self.rover_socket = None
        self.connectToRover()
        print("connesso")

    def run(self):
        self.state = True
        while self.state is True:
            try:
                self.rover_socket.sendall("DATA".encode('ASCII'))
                data = self.rover_socket.recv(1024).decode('ASCII')

                if not len(data) == 0:
                    radar = json.loads(data)['radar']
                    print(radar)
                    print("data ok\n")
                    self.controller.updateRadar(radar)

            except socket.timeout:
                print("Connessione chiusa")
                self.connection_state = False
                self.connectToRover()

            data = None

            time.sleep(0.5)  # necessario per non bloccare il seriale

    def stop(self):
        self.close()
        self.state = False

    def connectToRover(self):
        connected = False
        while not connected:
            try:
                self.rover_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.rover_socket.settimeout(2)
                self.rover_socket.connect((HOST, PORT))
                connected = True
                self.connection_state = True
            except (socket.timeout):
                print("riprovo")
                connected = False
                self.connection_state = False
            except OSError:
                print("Rover non acceso.") #TODO: Sostituire con finestra errore che chiede di verificare se rover acceso.
                self.stop()
                sys.exit()
                
    def close(self):
        self.rover_socket.close()
