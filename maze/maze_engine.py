from machine import Pin, SPI
from time import sleep_ms
import max7219
from mpu6050 import MPU6050

WIDTH = 8
HEIGHT = 8

# ----------------------------------------
# LEVELS
# ----------------------------------------

LEVELS = [

[
"########",
"#S.....#",
"#.###..#",
"#.#....#",
"#.####.#",
"#.....G#",
"#......#",
"########"

]

]

# ----------------------------------------
# BALL
# ----------------------------------------

class Ball:

    def __init__(self):

        self.x = 1.0
        self.y = 1.0

        self.vx = 0.0
        self.vy = 0.0

        self.ax = 0.0
        self.ay = 0.0

        self.radius = 0.25

        self.friction = 0.93
        self.bounce = 0.35
        self.max_speed = 0.55

    def update(self):

        self.vx += self.ax
        self.vy += self.ay

        self.vx *= self.friction
        self.vy *= self.friction

        if self.vx > self.max_speed:
            self.vx = self.max_speed

        if self.vx < -self.max_speed:
            self.vx = -self.max_speed

        if self.vy > self.max_speed:
            self.vy = self.max_speed

        if self.vy < -self.max_speed:
            self.vy = -self.max_speed

        self.x += self.vx
        self.y += self.vy

# ----------------------------------------
# ENGINE
# ----------------------------------------

class MazeEngine:

    def __init__(self):

        # ---------------- Display ----------------

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

        # ---------------- Sensor ----------------

        self.sensor = MPU6050()

        # ---------------- Ball ----------------

        self.ball = Ball()

        # ---------------- Calibration ----------------

        self.base_x = 0
        self.base_y = 0
        self.base_z = 0

        # ---------------- Level ----------------

        self.level = 0

        self.load_level()

        self.calibrate()

    # ----------------------------------------

    def calibrate(self):

        print("Keep board flat...")

        sx = 0
        sy = 0
        sz = 0

        for i in range(100):

            a = self.sensor.read_accel_data()

            sx += a["x"]
            sy += a["y"]
            sz += a["z"]

            sleep_ms(20)

        self.base_x = sx / 100
        self.base_y = sy / 100
        self.base_z = sz / 100

        print("Calibration Complete")

    # ----------------------------------------

    def load_level(self):

        self.maze = LEVELS[self.level]

        for y in range(HEIGHT):

            for x in range(WIDTH):

                c = self.maze[y][x]

                if c == "S":

                    self.ball.x = x
                    self.ball.y = y

                elif c == "G":

                    self.goal_x = x
                    self.goal_y = y

    # ----------------------------------------

    def draw(self):

        self.display.fill(0)

        for y in range(HEIGHT):

            for x in range(WIDTH):

                if self.maze[y][x] == "#":

                    self.display.pixel(x, y, 1)

        # Goal

        self.display.pixel(
            self.goal_x,
            self.goal_y,
            1
        )

        # Ball

        self.display.pixel(
            round(self.ball.x),
            round(self.ball.y),
            1
        )

        self.display.show()

    # ----------------------------------------
        # ----------------------------------------
    # SENSOR
    # ----------------------------------------

    def read_gravity(self):

        a = self.sensor.read_accel_data()

        gx = (a["x"] - self.base_x) / 8.0
        gy = -(a["y"] - self.base_y) / 8.0

        # dead zone
        if abs(gx) < 0.03:
            gx = 0

        if abs(gy) < 0.03:
            gy = 0

        return gx, gy

    # ----------------------------------------
    # COLLISION
    # ----------------------------------------

    def is_wall(self, x, y):

        tx = int(round(x))
        ty = int(round(y))

        if tx < 0 or tx >= WIDTH:
            return True

        if ty < 0 or ty >= HEIGHT:
            return True

        return self.maze[ty][tx] == "#"

    # ----------------------------------------

    def move_ball(self):

        # ---------- X Axis ----------

        nx = self.ball.x + self.ball.vx

        if not self.is_wall(nx, self.ball.y):

            self.ball.x = nx

        else:

            self.ball.vx *= -self.ball.bounce

        # ---------- Y Axis ----------

        ny = self.ball.y + self.ball.vy

        if not self.is_wall(self.ball.x, ny):

            self.ball.y = ny

        else:

            self.ball.vy *= -self.ball.bounce

    # ----------------------------------------

    def check_goal(self):

        if (
            round(self.ball.x) == self.goal_x and
            round(self.ball.y) == self.goal_y
        ):

            print("LEVEL COMPLETE!")

            for i in range(4):

                self.display.fill(1)
                self.display.show()
                sleep_ms(120)

                self.display.fill(0)
                self.display.show()
                sleep_ms(120)

            self.ball.x = 1
            self.ball.y = 1

            self.ball.vx = 0
            self.ball.vy = 0

    # ----------------------------------------

    def update(self):

        gx, gy = self.read_gravity()

        self.ball.ax = gx * 0.08
        self.ball.ay = gy * 0.08

        self.ball.update()

        self.move_ball()

        self.check_goal()

        self.draw()