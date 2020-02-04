
import time
import board
import busio

import adafruit_gps


class Gps:
    def __init__(self):
        self.uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(
            self.uart, debug=False)     # Use UART/pyserial
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.gps.send_command(b'PMTK220,1000')
        # Or decrease to once every two seconds by doubling the millisecond value.
        # Be sure to also increase your UART timeout above!


def update(self):
    self.gps.update()


def getData(self):
    
    self.gps.has_fix

    self.gps.latitude
    self.gps.longitude
    self.gps.fix_quality

    self.gps.satellites
    self.gps.altitude_m
    self.gps.speed_knots
