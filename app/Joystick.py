import pygame

TURNING_SPEED = 105


class Joystick():
    def __init__(self, controller):
        self.controller = controller
        pygame.init()
        pygame.joystick.init()

        self.speed = 105

        while pygame.joystick.get_count() < 1:
            self.controller.showCheckControllerDialog()
            pygame.joystick.quit()
            pygame.joystick.init()

        pygame.joystick.Joystick(0).init()

    def processEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 4:
                    # STOP
                    if 0 <= event.value < 1:
                        self.controller.stop()

                    # BACKWARD
                    if event.value >= 1:
                        self.controller.goBackward(self.speed)

                    # STOP
                    if -1 <= event.value < 0:
                        self.controller.stop()

                    # FORWARD
                    if event.value <= -1:
                        self.controller.goForward(self.speed)

                if event.axis == 3:
                    # STOP
                    if 0 <= event.value < 1:
                        self.controller.stop()

                    # RIGHT
                    if event.value >= 1:
                        self.controller.goRight(TURNING_SPEED)

                    # STOP
                    if -1 <= event.value < 0:
                        self.controller.stop()

                    # LEFT
                    if event.value <= -1:
                        self.controller.goLeft(TURNING_SPEED)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 5:
                    self.setSpeed(self.speed + 50)
                if event.button == 4:
                    self.setSpeed(self.speed - 50)

        self.controller.app.after(1, self.processEvent)

    def setSpeed(self, new_speed):
        if new_speed > 255:
            self.speed = 255
        elif new_speed < 50:
            self.speed = 105
        else:
            self.speed = new_speed
