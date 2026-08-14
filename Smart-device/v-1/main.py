from machine import Pin, I2C, SoftI2C
import time
import math
import dht

from sh1106 import SH1106_I2C


# ============================================================
# PIN CONFIGURATION
# ============================================================

TOUCH_PIN = 0
DHT_PIN = 1

# MPU6050
MPU_SDA = 4
MPU_SCL = 5

# LEDs
LED1_PIN = 14
LED2_PIN = 13

# OLED SH1106
OLED_SDA = 10
OLED_SCL = 11


# ============================================================
# GPIO SETUP
# ============================================================

touch = Pin(TOUCH_PIN, Pin.IN)

led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)

led1.value(0)
led2.value(0)


# ============================================================
# DHT22
# ============================================================

dht_sensor = dht.DHT22(Pin(DHT_PIN))


# ============================================================
# I2C - MPU6050
# ============================================================

i2c_mpu = I2C(
    0,
    sda=Pin(MPU_SDA),
    scl=Pin(MPU_SCL),
    freq=400000
)


# ============================================================
# I2C - OLED SH1106
# GP10 = SDA
# GP11 = SCL
#
# Using I2C1 because GP10/GP11 support I2C1
# ============================================================

i2c_oled = I2C(
    1,
    sda=Pin(OLED_SDA),
    scl=Pin(OLED_SCL),
    freq=100000
)


# ============================================================
# I2C SCANNING
# ============================================================

print("Scanning MPU6050...")
mpu_devices = i2c_mpu.scan()
print(mpu_devices)

print("Scanning OLED...")
oled_devices = i2c_oled.scan()
print(oled_devices)


# ============================================================
# MPU6050 ADDRESS CHECK
# ============================================================

if 0x68 in mpu_devices:
    mpu_addr = 0x68

elif 0x69 in mpu_devices:
    mpu_addr = 0x69

else:
    raise Exception("MPU6050 not detected!")


# ============================================================
# OLED ADDRESS CHECK
# ============================================================

if len(oled_devices) == 0:
    raise Exception("OLED not detected on GP10 / GP11!")

oled_addr = oled_devices[0]

print("OLED found at:", hex(oled_addr))


# ============================================================
# OLED INITIALIZATION
# ============================================================

oled = SH1106_I2C(
    128,
    64,
    i2c_oled,
    oled_addr
)


# ============================================================
# MPU6050 DRIVER
# ============================================================

class MPU6050:

    def __init__(self, i2c, addr=0x68):

        self.i2c = i2c
        self.addr = addr

        # Wake up MPU6050
        self.write_reg(0x6B, 0x00)

        time.sleep_ms(100)

        # Accelerometer ±2G
        self.write_reg(0x1C, 0x00)

        # Gyroscope ±250 deg/sec
        self.write_reg(0x1B, 0x00)


    def write_reg(self, reg, value):

        self.i2c.writeto_mem(
            self.addr,
            reg,
            bytes([value])
        )


    def read_raw(self):

        data = self.i2c.readfrom_mem(
            self.addr,
            0x3B,
            14
        )

        ax = self._signed(data[0] << 8 | data[1])
        ay = self._signed(data[2] << 8 | data[3])
        az = self._signed(data[4] << 8 | data[5])

        temp = self._signed(data[6] << 8 | data[7])

        gx = self._signed(data[8] << 8 | data[9])
        gy = self._signed(data[10] << 8 | data[11])
        gz = self._signed(data[12] << 8 | data[13])

        return ax, ay, az, temp, gx, gy, gz


    def _signed(self, value):

        if value & 0x8000:
            value -= 65536

        return value


    def read(self):

        ax, ay, az, temp, gx, gy, gz = self.read_raw()

        # Accelerometer values in G
        ax = ax / 16384.0
        ay = ay / 16384.0
        az = az / 16384.0

        # Gyroscope values in deg/sec
        gx = gx / 131.0
        gy = gy / 131.0
        gz = gz / 131.0

        # MPU6050 internal temperature
        temperature = temp / 340.0 + 36.53

        return (
            ax,
            ay,
            az,
            gx,
            gy,
            gz,
            temperature
        )


# ============================================================
# INITIALIZE MPU6050
# ============================================================

mpu = MPU6050(
    i2c_mpu,
    mpu_addr
)


# ============================================================
# SENSOR VALUES
# ============================================================

dht_temp = 0.0
humidity = 0.0

ax = 0.0
ay = 0.0
az = 0.0

gx = 0.0
gy = 0.0
gz = 0.0

mpu_temp = 0.0


# ============================================================
# ARTIFICIAL HORIZON
# ============================================================

def draw_horizon(ax, ay, az):

    roll = math.atan2(
        ay,
        az
    )

    pitch = math.atan2(
        -ax,
        math.sqrt(
            ay * ay +
            az * az
        )
    )

    roll_deg = math.degrees(roll)
    pitch_deg = math.degrees(pitch)


    # Display center
    cx = 64
    cy = 32


    # Convert pitch angle into screen movement
    pitch_pixels = pitch_deg * 0.8


    # Horizon line
    length = 38

    dx = math.cos(roll) * length
    dy = math.sin(roll) * length

    x1 = int(cx - dx)
    y1 = int(cy - dy + pitch_pixels)

    x2 = int(cx + dx)
    y2 = int(cy + dy + pitch_pixels)


    oled.line(
        x1,
        y1,
        x2,
        y2,
        1
    )


    # Aircraft symbol
    oled.line(
        cx - 10,
        cy,
        cx - 3,
        cy,
        1
    )

    oled.line(
        cx + 3,
        cy,
        cx + 10,
        cy,
        1
    )

    oled.line(
        cx,
        cy - 3,
        cx,
        cy + 3,
        1
    )


    return roll_deg, pitch_deg


# ============================================================
# PAGE SYSTEM
# ============================================================

page = 0
last_touch = 0

PAGE_COUNT = 4


def check_touch():

    global last_touch

    now = time.ticks_ms()

    if touch.value() == 1:

        if time.ticks_diff(
            now,
            last_touch
        ) > 500:

            last_touch = now

            return True

    return False


# ============================================================
# PAGE 0 - ENVIRONMENT
# ============================================================

def page_environment():

    oled.fill(0)

    oled.text(
        "ENVIRONMENT",
        20,
        0
    )

    oled.line(
        0,
        10,
        127,
        10,
        1
    )

    oled.text(
        "TEMP",
        0,
        18
    )

    oled.text(
        "{:.1f} C".format(dht_temp),
        65,
        18
    )

    oled.text(
        "HUM",
        0,
        34
    )

    oled.text(
        "{:.1f} %".format(humidity),
        65,
        34
    )

    oled.text(
        "MPU TEMP",
        0,
        50
    )

    oled.text(
        "{:.1f}C".format(mpu_temp),
        70,
        50
    )

    oled.show()


# ============================================================
# PAGE 1 - FLIGHT HUD
# ============================================================

def page_hud():

    oled.fill(0)

    oled.text(
        "FLIGHT HUD",
        28,
        0
    )

    oled.line(
        0,
        9,
        127,
        9,
        1
    )

    roll, pitch = draw_horizon(
        ax,
        ay,
        az
    )

    oled.text(
        "R:{:+.0f}".format(roll),
        0,
        53
    )

    oled.text(
        "P:{:+.0f}".format(pitch),
        70,
        53
    )

    oled.show()


# ============================================================
# PAGE 2 - MOTION
# ============================================================

def page_motion():

    oled.fill(0)

    oled.text(
        "MOTION",
        42,
        0
    )

    oled.line(
        0,
        9,
        127,
        9,
        1
    )

    oled.text(
        "AX {:+.2f}G".format(ax),
        0,
        14
    )

    oled.text(
        "AY {:+.2f}G".format(ay),
        0,
        25
    )

    oled.text(
        "AZ {:+.2f}G".format(az),
        0,
        36
    )

    oled.text(
        "GX {:+.0f}".format(gx),
        0,
        48
    )

    oled.text(
        "GY {:+.0f}".format(gy),
        43,
        48
    )

    oled.text(
        "GZ {:+.0f}".format(gz),
        86,
        48
    )

    oled.show()


# ============================================================
# PAGE 3 - SYSTEM STATUS
# ============================================================

def page_system():

    oled.fill(0)

    oled.text(
        "RP2040 SYSTEM",
        15,
        0
    )

    oled.line(
        0,
        10,
        127,
        10,
        1
    )

    oled.text(
        "MPU6050 OK",
        0,
        20
    )

    oled.text(
        "DHT22 OK",
        0,
        34
    )

    oled.text(
        "OLED OK",
        0,
        48
    )

    oled.show()


# ============================================================
# DRAW CURRENT PAGE
# ============================================================

def draw_page():

    if page == 0:

        page_environment()

    elif page == 1:

        page_hud()

    elif page == 2:

        page_motion()

    elif page == 3:

        page_system()


# ============================================================
# STARTUP SCREEN
# ============================================================

oled.fill(0)

oled.text(
    "RP2040",
    42,
    15
)

oled.text(
    "SENSOR HUB",
    25,
    30
)

oled.text(
    "BOOTING...",
    30,
    45
)

oled.show()


led1.value(1)
led2.value(0)

time.sleep(2)

led1.value(0)


# ============================================================
# MAIN LOOP
# ============================================================

last_dht = 0
last_mpu = 0
last_display = 0


while True:

    now = time.ticks_ms()


    # --------------------------------------------------------
    # TOUCH - CHANGE PAGE
    # --------------------------------------------------------

    if check_touch():

        page += 1

        if page >= PAGE_COUNT:
            page = 0

        led2.value(1)

        time.sleep_ms(50)

        led2.value(0)


    # --------------------------------------------------------
    # DHT22
    # --------------------------------------------------------

    if time.ticks_diff(
        now,
        last_dht
    ) >= 2000:

        last_dht = now

        try:

            dht_sensor.measure()

            dht_temp = dht_sensor.temperature()
            humidity = dht_sensor.humidity()

        except Exception as e:

            print(
                "DHT error:",
                e
            )


    # --------------------------------------------------------
    # MPU6050
    # --------------------------------------------------------

    if time.ticks_diff(
        now,
        last_mpu
    ) >= 50:

        last_mpu = now

        try:

            (
                ax,
                ay,
                az,
                gx,
                gy,
                gz,
                mpu_temp
            ) = mpu.read()

        except Exception as e:

            print(
                "MPU error:",
                e
            )


    # --------------------------------------------------------
    # LED1 - MOVEMENT INDICATOR
    # --------------------------------------------------------

    motion = (

        abs(gx) > 30 or
        abs(gy) > 30 or
        abs(gz) > 30

    )

    led1.value(
        1 if motion else 0
    )


    # --------------------------------------------------------
    # OLED DISPLAY UPDATE
    # --------------------------------------------------------

    if time.ticks_diff(
        now,
        last_display
    ) >= 100:

        last_display = now

        draw_page()


    time.sleep_ms(5)
