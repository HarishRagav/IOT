import bluetooth
import time
import struct

ble = bluetooth.BLE()
ble.active(True)

name = "ESP32_HARISH"

# BLE advertising payload
adv_data = bytearray()

# Flags
adv_data += struct.pack("BBB", 2, 0x01, 0x06)

# Complete local name
adv_data += struct.pack("BB", len(name) + 1, 0x09)
adv_data += name.encode()

print("Starting BLE advertising...")
ble.gap_advertise(100_000, adv_data=adv_data)

print("BLE is ON!")
print("Look for:", name)

while True:
    time.sleep(1)