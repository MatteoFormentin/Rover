# LIBRARY: https://github.com/RigacciOrg/py-qmc5883l
import py_qmc5883l

CORRECTION = 0
class Compass:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L()

    def getBearing(self):
        return int((self.sensor.get_bearing() + CORRECTION ) % 360)
