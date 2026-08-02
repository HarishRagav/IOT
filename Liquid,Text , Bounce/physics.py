from time import sleep

class Ball:

    def __init__(self, sensor):

        self.sensor = sensor

        self.x = 3.5
        self.y = 3.5

        self.vx = 0.0
        self.vy = 0.0

        self.base_x = 0
        self.base_y = 0
        self.base_z = 0

        self.calibrate()

    def calibrate(self):

        print("Keep the board flat...")

        sx = sy = sz = 0

        for i in range(100):

            a = self.sensor.read_accel_data()

            sx += a["x"]
            sy += a["y"]
            sz += a["z"]

            sleep(0.02)

        self.base_x = sx / 100
        self.base_y = sy / 100
        self.base_z = sz / 100

        print("Done!")

    def update(self):

        a = self.sensor.read_accel_data()

        ax = (a["x"] - self.base_x) / 4
        ay = -(a["y"] - self.base_y) / 4

        # gravity
        self.vx += ax * 0.20
        self.vy += ay * 0.20

        # friction
        self.vx *= 0.95
        self.vy *= 0.95

        self.x += self.vx
        self.y += self.vy

        bounce = 0.70

        if self.x < 1:
            self.x = 1
            self.vx *= -bounce

        if self.x > 6:
            self.x = 6
            self.vx *= -bounce

        if self.y < 1:
            self.y = 1
            self.vy *= -bounce

        if self.y > 6:
            self.y = 6
            self.vy *= -bounce

    def draw(self, display):

        display.pixel(round(self.x), round(self.y), 1)
