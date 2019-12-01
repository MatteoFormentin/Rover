import zmq

HOST = '10.0.20.133'
PORT = '5554'


class Network():
    def __init__(self, controller):
        self.controller = controller
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)

    def connect(self):
        try:
            self.socket.connect("tcp://" + HOST + ":" + PORT)
        except Exception:
            self.controller.showCheckConnectionDialog()

    def sendData(self, data):
        self.socket.send_string(data)

    def getData(self):
        self.socket.recv_string()
