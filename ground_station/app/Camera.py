import cv2
import socket
import base64
import numpy as np
from threading import Thread


class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.run_thread = True
        self.curr_frame = None

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversocket.bind((self.getIp(), 7777))

        self.video_stream_status = False

    def startVideoStream(self):
        self.video_stream_status = True

    def stopVideoStream(self):
        self.video_stream_status = False
    
    def getIp(self):
        return socket.gethostbyname(socket.gethostname())

    def run(self):
        packets = []
        seq = -1  # Sequence number of frames
        counter = 0  # Count how many chunks of the current frame already received

        while self.run_thread:
            if self.video_stream_status:
                d, a = serversocket.recvfrom(4096)  # Check if a chunks arrived
                if d:
                    print(d)
                    # sequence number, number of chunks of the frame, current chunks, chunks data
                    packet_seq, tot, curr, data = self.decodePacket(d)

                    # if a most recent frame arrived, discard the oldest one
                    if packet_seq != seq:
                        packets = [None] * tot
                        seq = packet_seq
                        counter = 0

                    # Put chunk in order
                    packets[curr] = data
                    counter += 1

                    # if number of chunks received = total chunks number of the frame assemble and show the image
                    if counter == tot:
                        img = b''
                        for i in packets:
                            img = img + i

                        self.curr_frame = img

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

    def startVideoStream(self):
        self.video_stream_status = True

    def stopVideoStream(self):
        self.video_stream_status = False

    def decodePacket(self, packet):
        packet_seq = int.from_bytes(packet[0:10], "little", signed=False)
        tot = int.from_bytes(packet[10:20], "little", signed=False)
        curr = int.from_bytes(packet[20:30], "little", signed=False)
        data = packet[30:]
        # print("Header| " + " Seq: " + str(packet_seq) + " | Total: " +
        #     str(tot) + " | Curr: " + str(curr) + "|")

        return packet_seq, tot, curr, data
