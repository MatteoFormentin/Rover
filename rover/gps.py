
import time
import board
import serial

import adafruit_gps


class Gps:
    def __init__(self):
        #self.uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

        self.uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
        self.gps_sensor = adafruit_gps.GPS(
            self.uart, debug=False)     # Use UART/pyserial
        self.gps_sensor.send_command(
            b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.gps_sensor.send_command(b'PMTK220,1000')
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!


    def update(self):
        # On warm up the sensor 
        try:
            self.gps_sensor.update()
        except Exception:
            pass

    def getData(self):
        return self.gps_sensor

    def isGpsFix(self):
        return self.gps_sensor.has_fix

    def getCurrentPoint(self):
        return [self.gps_sensor.latitude, self.gps_sensor.longitude]
