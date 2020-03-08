import time


class PID:
    def __init__(self, k_p, k_i, k_d, min_value, max_value, angle=False):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d

        self.max_value = max_value
        self.min_value = min_value

        self.angle_pid = angle

        self.previous_error = 0
        self.integral = 0

        self.last_execution = time.time()

    def computeOutput(self, current, setpoint):
        dt = time.time() - self.last_execution
        error = setpoint - current

        if self.angle_pid and error > 180:
            error -= 360

        self.integral += error * dt
        derivative = (error - self.previous_error) / dt

        # Proportional + Itegral + Derivative
        output = error * self.k_p + self.integral * self.k_i + derivative * self.k_d

        if output > self.max_value:
            output = self.max_value
        if output < self.min_value:
            output = self.min_value

        self.last_execution = time.time()
        self.previous_error = error

        return int(output)

    def reset(self):
        self.previous_error = 0
        self.integral = 0
        self.last_execution = time.time()
