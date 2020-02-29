from threading import Thread
import base64
import cv2
import math
import socket
import time

class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.camera = cv2.VideoCapture(0)  # init the camera
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.seq_number = 0

        self.ground_station_ip_address = ""

        self.run_thread = True
        self.video_stream_status = False

        self.fps = 0

    def run(self):
        last_reset = time.time()
        rcv_frame_delta = 0
        while self.run_thread:
            if self.video_stream_status:

                #FPS CALC
                delta = time.time() - last_reset
                if delta > 1:
                    last_reset = time.time()
                    self.fps = int(rcv_frame_delta / delta)
                    rcv_frame_delta = 0
                #END

                img = self.getVideoFrame()
                data = self.generatePacket(img, self.seq_number)

                for i in data:
                    self.clientsocket.sendto(
                        i, (self.ground_station_ip_address, 7777))

                self.seq_number += 1
                
                rcv_frame_delta += 1

                #print("FPS: " + str(self.fps) + "        ", end='\r')

    def stop(self):
        self.run_thread = False
        self.camera.release()

    def startVideoStream(self):
        self.seq_number = 0
        self.video_stream_status = True

    def stopVideoStream(self):
        self.video_stream_status = False

    def getVideoFrame(self):
        grabbed, frame = self.camera.read()  # grab the current frame
        frame = cv2.resize(frame, (320, 240))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text  # output byte array

    def generatePacket(self, data, seq_number):
        packet_dimension = 4096 - 8  # Byte dimension of packet
        # number of packet to be generated to contain all data
        packet_number = math.ceil(len(data)/packet_dimension)

        packets = []
        for i in range(0, packet_number):
            # Genrate packet header
            # Structure
            # |Sequence Number(2)|Packet Number(2)|Current Packet(2)|Data(packet_dimension - 20)|
            header = seq_number.to_bytes(
                2, "little", signed=False) + packet_number.to_bytes(
                2, "little", signed=False) + i.to_bytes(2, "little", signed=False)

            # Split data into packets
            start = i * packet_dimension
            end = start + packet_dimension
            packet = header + data[start:end]
            packets.append(packet)

            # print()
            # print("Header| " + " Seq: " + str(seq_number) + " | Total: " +
            #      str(packet_number) + " | Curr: " + str(i) + "|")

        return packets

    def setGroundStationIpAddress(self, ip):
        self.ground_station_ip_address = ip
