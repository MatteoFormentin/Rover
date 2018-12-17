import pygame


class Joystick():
    def __init__(self, controller):
        self.controller = controller
        pygame.init()
        pygame.joystick.init()

        while pygame.joystick.get_count() < 1:
            self.controller.showCheckControllerDialog()
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
                        self.controller.goBackward()

                    # STOP
                    if -1 <= event.value < 0:
                        self.controller.stop()

                    # FORWARD
                    if event.value <= -1:
                        self.controller.goForward()

                if event.axis == 3:
                    # STOP
                    if 0 <= event.value < 1:
                        self.controller.stop()

                    # RIGHT
                    if event.value >= 1:
                        self.controller.goRight()

                    # STOP
                    if -1 <= event.value < 0:
                        self.controller.stop()

                    # LEFT
                    if event.value <= -1:
                        self.controller.goLeft()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 5:
                    self.controller.upSpeed()
                if event.button == 4:
                    self.controller.downSpeed()

        self.controller.app.after(1, self.processEvent)
