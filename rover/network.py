import zmq
from queue import *
from threading import Thread

PORT = "5554"


class Network(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % PORT)
        self.run_thread = True
        self.queue = queue

    def getData(self):
        return self.socket.recv_string()

    def sendData(self, data):
        self.socket.send_string(data)

    def run(self):
        while self.run_thread:
            self.queue.put(self.getData())

    def stop(self):
        self.run_thread = False
