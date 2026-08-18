import network
import time

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

wifi.connect("HARISH", "123456789")

print("Connecting to Wi-Fi...")

while not wifi.isconnected():
    print(".", end="")
    time.sleep(1)

print("\nCONNECTED! 🔥")
print("Network config:", wifi.ifconfig())