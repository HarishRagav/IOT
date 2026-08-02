from machine import SPI, Pin
from time import sleep, sleep_ms
import max7219
from mpu6050 import MPU6050


class MazeEngine:

    def __init__(self):

        # -------------------------------
        # DISPLAY
        # -------------------------------

        self.spi = SPI(
            0,
            baudrate=10000000,
            polarity=0,
            phase=0,
            sck=Pin(2),
            mosi=Pin(3)
        )

        self.cs = Pin(4, Pin.OUT)

        self.display = max7219.Matrix8x8(
            self.spi,
            self.cs,
            1
        )

        self.display.brightness(5)

        # -------------------------------
        # SENSOR
        # -------------------------------

        self.sensor = MPU6050()

        # -------------------------------
        # PLAYER
        # -------------------------------

        self.ball_x = 1.0
        self.ball_y = 1.0

        self.vel_x = 0.0
        self.vel_y = 0.0

        # -------------------------------
        # CALIBRATION
        # -------------------------------

        self.base_x = 0
        self.base_y = 0
        self.base_z = 0

        # -------------------------------
        # LEVELS
        # -------------------------------

        self.levels = [

            [

            "########",
            "#S     #",
            "# ###  #",
            "# #    #",
            "# #### #",
            "#     G#",
            "#      #",
            "########"

            ]

        ]

        self.level = 0

        self.load_level()

        self.calibrate()

    # ---------------------------------------
    # CALIBRATION
    # ---------------------------------------

    def calibrate(self):

        print("----------------------")
        print("Keep Board Flat")
        print("----------------------")

        sx = 0
        sy = 0
        sz = 0

        for i in range(100):

            a = self.sensor.read_accel_data()

            sx += a["x"]
            sy += a["y"]
            sz += a["z"]

            sleep(0.02)

        self.base_x = sx / 100
        self.base_y = sy / 100
        self.base_z = sz / 100

        print("Calibration Complete!")

    # ---------------------------------------
    # LOAD LEVEL
    # ---------------------------------------

    def load_level(self):

        self.maze = self.levels[self.level]

        for y in range(8):

            for x in range(8):

                c = self.maze[y][x]

                if c == "S":

                    self.ball_x = x
                    self.ball_y = y

                elif c == "G":

                    self.goal_x = x
                    self.goal_y = y

    # ---------------------------------------
    # DRAW
    # ---------------------------------------

    def draw(self):

        self.display.fill(0)

        for y in range(8):

            for x in range(8):

                if self.maze[y][x] == "#":

                    self.display.pixel(x, y, 1)

        self.display.pixel(
            self.goal_x,
            self.goal_y,
            1
        )

        self.display.pixel(
            round(self.ball_x),
            round(self.ball_y),
            1
        )

        self.display.show()

    # ---------------------------------------
    # UPDATE
    # ---------------------------------------

    def update(self):

        self.draw()