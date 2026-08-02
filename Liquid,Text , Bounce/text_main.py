from machine import Pin, SPI
import max7219
from time import sleep

# SPI Configuration
from machine import Pin, SPI

spi = SPI(
    0,
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3)
)

cs = Pin(4, Pin.OUT)

display = max7219.Matrix8x8(spi, cs, 1)

display.brightness(5)


from time import sleep

while True:
    for x in range(60):
        display.fill(0)
        display.text("EDWIN", 8-x, 0, 1)
        display.show()
        sleep(0.05)

