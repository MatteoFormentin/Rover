from motor import *

class Controller:
    def __init__(self):
        self.motor = Motor()

        self.motor.rotateRight(80)
      
    def run(self):
        while True:
            try:
                pass

            except KeyboardInterrupt:
                self.motor.handleShutdown()
