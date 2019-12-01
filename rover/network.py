
import zmq

PORT = "5554"


class Network:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % PORT)

    def getData(self):
        return self.socket.recv_string()

    def sendData(self, data):
        self.socket.send_string(data)
