# LIBRARY: https://github.com/RigacciOrg/py-qmc5883l
import py_qmc5883l

CORRECTION = 0

CALIBRATION = [[1.02629383e+00, -1.92258846e-02, - 1.70457032e+03],
               [-1.92258846e-02,  1.01405785e+00,  4.14480013e+02],
               [0.00000000e+00,  0.00000000e+00,  1.00000000e+00]]


class Compass:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L()
        self.sensor.calibration = CALIBRATION

    def getBearing(self):
        return int((self.sensor.get_bearing() + CORRECTION) % 360)

    def getBearingNormalized(self):
        bearing = int((self.sensor.get_bearing() + CORRECTION) % 360)
        if bearing > 180:
            bearing -= 360
        return bearing
