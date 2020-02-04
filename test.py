# Load configuration file
from threading import Thread
import numpy as np
import base64
import cv2
import zmq

import socket

camera = cv2.VideoCapture(0)  # init the camera


while True:
    grabbed, frame = camera.read()  # grab the current frame
    frame = cv2.resize(frame, (640, 480))  # resize the frame
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)

    self.chunks = jpg_as_text[0:]







    print(len(jpg_as_text))

