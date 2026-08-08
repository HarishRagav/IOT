from machine import Pin, I2C
import sh1106
import time

# GP20 = SDA
# GP21 = SCL

i2c = I2C(
    0,
    sda=Pin(20),
    scl=Pin(21),
    freq=100000
)

print("I2C devices:", [hex(x) for x in i2c.scan()])

oled = sh1106.SH1106_I2C(
    128,
    64,
    i2c,
    addr=0x3C
)

oled.fill(0)

oled.text("HELLO HARISH!", 0, 0)
oled.text("SH1106 OLED", 0, 16)
oled.text("SDA : GP20", 0, 32)
oled.text("SCL : GP21", 0, 48)

oled.show()

while True:
    time.sleep(1)
