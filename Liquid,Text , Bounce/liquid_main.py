from time import sleep
from physics import Physics
from mpu6050 import MPU6050


class Liquid:

    def __init__(self):

        self.sensor = MPU6050()
        self.physics = Physics()

        self.physics.fill()

        self.base_x = 0
        self.base_y = 0
        self.base_z = 0

        print("Keep the board flat...")
        self.calibrate()

    def calibrate(self):

        sx = 0
        sy = 0
        sz = 0

        samples = 100

        for i in range(samples):

            a = self.sensor.read_accel_data()

            sx += a["x"]
            sy += a["y"]
            sz += a["z"]

            sleep(0.02)

        self.base_x = sx / samples
        self.base_y = sy / samples
        self.base_z = sz / samples

        print("Calibration complete!")

    def gravity(self):

        a = self.sensor.read_accel_data()

        dx = a["x"] - self.base_x
        dy = a["y"] - self.base_y

        # Scale tilt into gravity
        gx = -dx / 3.5
        gy = dy / 3.5

        # Clamp values
        if gx > 1:
            gx = 1
        if gx < -1:
            gx = -1

        if gy > 1:
            gy = 1
        if gy < -1:
            gy = -1

        return gx, gy

    def update(self):

        gx, gy = self.gravity()

        self.physics.update(gx, gy)

    def pixels(self):

        return self.physics.pixels()
