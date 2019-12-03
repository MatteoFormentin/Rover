import zmq

HOST = '192.168.0.1'
PORT = '5554'


class Network():
    def __init__(self, controller):
        self.controller = controller
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)

    def connect(self):
        try:
            print("connetto...")
            self.socket.connect("tcp://" + HOST + ":" + PORT)
            print("connesso!")
        except Exception:
            self.controller.showCheckConnectionDialog()

    def sendData(self, data):
        self.socket.send_string(data)

    def getData(self):
        return self.socket.recv_string()
