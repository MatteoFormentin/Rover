
import zmq





class Network:
    def __init__(self):
        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        footage_socket.bind('tcp://*:5555')

        footage_socket.send(jpg_as_text)
