import zmq

HOST = '192.168.0.1'
PORT = '5554'


class Network():
    def __init__(self, controller):
        self.controller = controller
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.RCVTIMEO = 10000
        self.connected = False
        #self.socket.setsockopt(zmq.ZMQ_CONNECT_TIMEOUT, 1000)
        

    def connect(self):
        self.socket.connect("tcp://" + HOST + ":" + PORT)
        self.connected = True


    def sendData(self, data):
        self.socket.send_string(data)

    def getData(self):
        try:
            data = self.socket.recv_string()
        except Exception as e:
            self.connected = False
            self.controller.showCheckConnectionDialog()
            return
        return data

    def disconnect(self):
        if self.connected:
            self.context.destroy()
