from threading import Thread
import numpy as np
import base64
import cv2
import zmq




class Camera(Thread):
    def __init__(self):
        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.PUB)
        self.footage_socket.bind('tcp://*:5555')
        self.camera = cv2.VideoCapture(0)  # init the camera

    def run(self):
        while run_thread:
            grabbed, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            self.footage_socket.send(jpg_as_text)

    def stop(self):
        self.run_thread = False
        self.camera.release()
        cv2.destroyAllWindows()
