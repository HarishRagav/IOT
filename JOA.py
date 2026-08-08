from machine import Pin, I2C
import sh1106
import time
import random


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
# CUSTOM PIXEL FONT
# =========================================================

FONT = {

    "A": [
        "01110",
        "11011",
        "11011",
        "11111",
        "11011",
        "11011",
        "11011",
    ],

    "C": [
        "01111",
        "11000",
        "11000",
        "11000",
        "11000",
        "11000",
        "01111",
    ],

    "F": [
        "11111",
        "11000",
        "11000",
        "11110",
        "11000",
        "11000",
        "11000",
    ],

    "J": [
        "00111",
        "00011",
        "00011",
        "00011",
        "11011",
        "11011",
        "01110",
    ],

    "K": [
        "11011",
        "11110",
        "11100",
        "11000",
        "11100",
        "11110",
        "11011",
    ],

    "L": [
        "11000",
        "11000",
        "11000",
        "11000",
        "11000",
        "11000",
        "11111",
    ],

    "O": [
        "01110",
        "11011",
        "11011",
        "11011",
        "11011",
        "11011",
        "01110",
    ],

    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ],
}


# =========================================================
# DRAW SCALED TEXT
# =========================================================

def draw_word_scaled(text, y, scale, spacing):

    char_width = 5 * scale

    width = (
        len(text) * char_width
        + (len(text) - 1) * spacing
    )

    # Center horizontally
    x = (128 - width) // 2

    for char in text:

        bitmap = FONT.get(
            char,
            FONT[" "]
        )

        for row in range(7):

            for col in range(5):

                if bitmap[row][col] == "1":

                    oled.fill_rect(
                        x + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        1
                    )

        x += char_width + spacing


# =========================================================
# DRAW LOGO
# =========================================================

def draw_logo():

    oled.fill(0)

    # -----------------------------------------
    # SMALL TOP TEXT
    # -----------------------------------------

    draw_word_scaled(
        "JACK OF",
        5,
        1,
        2
    )

    # -----------------------------------------
    # BIG "ALL"
    # -----------------------------------------

    draw_word_scaled(
        "ALL",
        23,
        3,
        4
    )


# =========================================================
# RANDOM PIXEL NOISE
# =========================================================

def pixel_noise(amount):

    for _ in range(amount):

        x = random.randint(
            10,
            117
        )

        y = random.randint(
            2,
            61
        )

        oled.pixel(
            x,
            y,
            random.randint(0, 1)
        )


# =========================================================
# SMALL GLITCH
# =========================================================

def glitch_slice():

    draw_logo()

    # Random horizontal slice

    y = random.randint(
        3,
        58
    )

    height = random.choice([
        1,
        1,
        2,
        3
    ])

    # Erase slice

    oled.fill_rect(
        0,
        y,
        128,
        height,
        0
    )

    # Broken digital fragments

    for _ in range(
        random.randint(2, 6)
    ):

        x = random.randint(
            5,
            115
        )

        width = random.randint(
            3,
            18
        )

        oled.fill_rect(
            x,
            y,
            width,
            height,
            1
        )


# =========================================================
# HEAVY GLITCH
# =========================================================

def heavy_glitch():

    draw_logo()

    # Horizontal interference

    for _ in range(
        random.randint(3, 8)
    ):

        y = random.randint(
            3,
            60
        )

        height = random.randint(
            1,
            3
        )

        # Random erase

        if random.randint(0, 1):

            oled.fill_rect(
                0,
                y,
                128,
                height,
                0
            )

        # Random fragments

        else:

            for _ in range(
                random.randint(1, 5)
            ):

                x = random.randint(
                    0,
                    120
                )

                width = random.randint(
                    2,
                    20
                )

                oled.fill_rect(
                    x,
                    y,
                    width,
                    height,
                    1
                )

    # Noise

    pixel_noise(
        random.randint(
            10,
            35
        )
    )


# =========================================================
# BOOT ANIMATION
# =========================================================

def boot():

    oled.fill(0)

    # -----------------------------------------
    # RANDOM BOOT NOISE
    # -----------------------------------------

    for frame in range(12):

        oled.fill(0)

        pixel_noise(
            frame * 5
        )

        oled.show()

        time.sleep(0.04)


    # -----------------------------------------
    # JACK OF
    # -----------------------------------------

    oled.fill(0)

    draw_word_scaled(
        "JACK OF",
        5,
        1,
        2
    )

    oled.show()

    time.sleep(0.3)


    # -----------------------------------------
    # ALL
    # -----------------------------------------

    oled.fill(0)

    draw_word_scaled(
        "JACK OF",
        5,
        1,
        2
    )

    draw_word_scaled(
        "ALL",
        23,
        3,
        4
    )

    oled.show()

    time.sleep(0.5)


# =========================================================
# START
# =========================================================

boot()


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    # -----------------------------------------
    # CLEAN LOGO
    # -----------------------------------------

    draw_logo()

    oled.show()

    time.sleep(
        random.uniform(
            1.2,
            3.0
        )
    )


    # -----------------------------------------
    # SMALL GLITCH
    # -----------------------------------------

    for _ in range(
        random.randint(1, 3)
    ):

        glitch_slice()

        oled.show()

        time.sleep(
            random.uniform(
                0.025,
                0.07
            )
        )


    # -----------------------------------------
    # RECOVER
    # -----------------------------------------

    draw_logo()

    oled.show()

    time.sleep(0.25)


    # -----------------------------------------
    # OCCASIONAL HEAVY GLITCH
    # -----------------------------------------

    if random.randint(0, 4) == 0:

        for _ in range(
            random.randint(2, 5)
        ):

            heavy_glitch()

            oled.show()

            time.sleep(
                random.uniform(
                    0.02,
                    0.06
                )
            )

        # Snap back to clean logo

        draw_logo()

        oled.show()

    time.sleep(
        random.uniform(
            0.7,
            2.0
        )
    )
