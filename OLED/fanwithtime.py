from machine import Pin, I2C, RTC
import sh1106
import time
import math


# =========================================================
# OLED
# =========================================================

i2c = I2C(
    0,
    sda=Pin(20),
    scl=Pin(21),
    freq=100000
)

oled = sh1106.SH1106_I2C(
    128,
    64,
    i2c,
    addr=0x3C
)


# =========================================================
# RTC
# =========================================================

rtc = RTC()

# Set this ONCE, then comment it out.
rtc.datetime((
    2026,
    8,
    9,
    6,
    4,
    0,
    0,
    0
))


# =========================================================
# FAN
# =========================================================

CX = 64
CY = 22

RADIUS = 20

# 90 RPM
RPM = 90

ROTATIONS_PER_SECOND = RPM / 60

FRAME_TIME = 0.025

ANGLE_STEP = (
    2 * math.pi
    * ROTATIONS_PER_SECOND
    * FRAME_TIME
)

angle = 0.0


# =========================================================
# DRAW ONE TAPERED WING
# =========================================================

def draw_wing(angle):

    inner = 2
    outer = RADIUS

    # Width at the outside
    outer_width = 4

    dx = math.cos(angle)
    dy = math.sin(angle)

    # Perpendicular direction
    px = -dy
    py = dx

    # Center
    cx = CX + dx * inner
    cy = CY + dy * inner

    # Outer tip
    ox = CX + dx * outer
    oy = CY + dy * outer

    # Outer edges
    left_x = ox + px * outer_width
    left_y = oy + py * outer_width

    right_x = ox - px * outer_width
    right_y = oy - py * outer_width

    # Build tapered wing
    for i in range(21):

        t = i / 20

        x = cx + (ox - cx) * t
        y = cy + (oy - cy) * t

        # Narrow near center,
        # wide near tip
        w = outer_width * t

        x1 = x + px * w
        y1 = y + py * w

        x2 = x - px * w
        y2 = y - py * w

        oled.line(
            int(x1),
            int(y1),
            int(x2),
            int(y2),
            1
        )


# =========================================================
# FIVE-WING FAN
# =========================================================

def draw_star(angle):

    # 5 wings
    # 360 / 5 = 72 degrees

    for i in range(1):

        wing_angle = (
            angle +
            i * (2 * math.pi / 1)
        )

        draw_wing(
            wing_angle
        )

    # Center hub
    oled.fill_rect(
        CX - 3,
        CY - 3,
        7,
        7,
        1
    )


# =========================================================
# TIME
# =========================================================

def draw_time():

    data = rtc.datetime()

    hour = data[4]
    minute = data[5]
    second = data[6]

    text = "{:02d}:{:02d}:{:02d}".format(
        hour,
        minute,
        second
    )

    x = (
        128 -
        len(text) * 8
    ) // 2

    oled.text(
        text,
        x,
        49
    )


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    oled.fill(0)

    # Five-wing spinner
    draw_star(angle)

    # Time
    draw_time()

    oled.show()

    # Rotate
    angle += ANGLE_STEP

    if angle >= 2 * math.pi:
        angle -= 2 * math.pi

    time.sleep(FRAME_TIME)
