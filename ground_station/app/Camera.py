import cv2
import zmq
import base64
import numpy as np
from threading import Thread


class Camera(Thread):
    def __init__(self):
        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.SUB)
        self.footage_socket.connect('tcp://10.0.20.133:5555')
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        self.run_thread = True

    def run(self):
        while run_thread:
            frame = footage_socket.recv_string()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("Stream", source)
            cv2.waitKey(1)

    def stop(self):
        self.run_thread = False
