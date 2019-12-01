import cv2
import zmq
import base64
import numpy as np
from threading import Thread


class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.DISH)
        self.footage_socket.connect('udp://192.168.0.1:5555')
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        self.run_thread = True
        self.curr_frame = None

    def run(self):
        while self.run_thread:
            self.curr_frame = self.footage_socket.recv_string()
            
            #cv2.imshow("Stream", source)
            # cv2.waitKey(1)

    def getFrame(self):
        try:
            img = base64.b64decode(self.curr_frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            return cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        except Exception:
            pass

    def stop(self):
        self.run_thread = False
