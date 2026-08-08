from machine import Pin, I2C
import sh1106
import time
import random
import math


# =========================================================
# OLED SETUP
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
# FIRE PARTICLES
# =========================================================

particles = []

for i in range(25):

    particles.append({
        "x": random.randint(45, 82),
        "y": random.randint(25, 58),
        "speed": random.randint(1, 3),
        "drift": random.choice([-1, 0, 0, 1]),
        "life": random.randint(10, 30)
    })


# =========================================================
# FIRE
# =========================================================

while True:

    oled.fill(0)

    # -----------------------------------------------------
    # GROUND
    # -----------------------------------------------------

    oled.line(35, 59, 92, 59, 1)

    # -----------------------------------------------------
    # LOGS
    # -----------------------------------------------------

    oled.line(43, 58, 65, 49, 1)
    oled.line(63, 58, 84, 49, 1)

    oled.line(43, 55, 65, 59, 1)
    oled.line(63, 59, 84, 55, 1)

    # -----------------------------------------------------
    # FIRE BODY
    # -----------------------------------------------------

    # Random flame width
    width = random.randint(10, 16)

    center = 64 + random.randint(-3, 3)

    # Main flame silhouette
    for y in range(56, 27, -1):

        height_from_bottom = 56 - y

        # Flame gets narrower toward top
        max_width = int(
            width * (1 - height_from_bottom / 34)
        )

        if max_width < 1:
            max_width = 1

        # Flickering movement
        flicker = random.randint(-2, 2)

        left = center - max_width + flicker
        right = center + max_width + flicker

        oled.line(left, y, right, y, 1)

    # -----------------------------------------------------
    # FLAME TIP
    # -----------------------------------------------------

    tip_x = center + random.randint(-5, 5)

    oled.pixel(tip_x, 23, 1)
    oled.pixel(tip_x - 1, 24, 1)
    oled.pixel(tip_x + 1, 24, 1)

    # -----------------------------------------------------
    # INNER FLAME
    # -----------------------------------------------------

    inner_x = center + random.randint(-3, 3)

    for y in range(52, 35, -1):

        w = int((52 - y) * 0.45)

        if w < 1:
            w = 1

        oled.line(
            inner_x - w,
            y,
            inner_x + w,
            y,
            0
        )

    # -----------------------------------------------------
    # RE-DRAW SMALL INNER FLAME
    # -----------------------------------------------------

    oled.line(inner_x, 50, inner_x - 4, 42, 1)
    oled.line(inner_x, 50, inner_x + 4, 42, 1)
    oled.line(inner_x - 4, 42, inner_x, 35, 1)
    oled.line(inner_x + 4, 42, inner_x, 35, 1)

    # -----------------------------------------------------
    # SPARK PARTICLES
    # -----------------------------------------------------

    for p in particles:

        # Move upward
        p["y"] -= p["speed"]

        # Horizontal drift
        p["x"] += p["drift"]

        p["life"] -= 1

        # Draw particle
        if p["life"] > 0:
            if 0 <= p["x"] < 128 and 0 <= p["y"] < 64:

                # Random flicker
                if random.randint(0, 2) != 0:
                    oled.pixel(
                        int(p["x"]),
                        int(p["y"]),
                        1
                    )

        # Respawn
        if p["y"] < 18 or p["life"] <= 0:

            p["x"] = random.randint(48, 80)
            p["y"] = random.randint(45, 58)

            p["speed"] = random.randint(1, 3)

            p["drift"] = random.choice([
                -1,
                0,
                0,
                1
            ])

            p["life"] = random.randint(10, 30)

    # -----------------------------------------------------
    # SHOW FRAME
    # -----------------------------------------------------

    oled.show()

    # Animation speed
    time.sleep(0.045)
