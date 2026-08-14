# RP2040 Sensor Hub 🚀

A small sensor hub built using **RP2040 + MicroPython**. It reads temperature/humidity, motion data, and shows everything on an SH1106 OLED.

## 🔌 Pin Connections

| Component       | Pin            |
| --------------- | -------------- |
| 👆 Touch Sensor | **GP0**        |
| 🌡️ DHT22 Data  | **GP1**        |
| 📡 MPU6050 SDA  | **GP4**        |
| 📡 MPU6050 SCL  | **GP5**        |
| 🖥️ OLED SDA    | **GP10**       |
| 🖥️ OLED SCL    | **GP11**       |
| 💡 LED 1        | **GP13**       |
| 💡 LED 2        | **GP14**       |
| 🔋 VCC          | **3.3V**       |
| ⏚ GND           | **Common GND** |

## 📦 Libraries

Built-in MicroPython libraries:

```text
machine
time
math
dht
framebuf
micropython
```

Custom driver:

```text
sh1106.py
```

Make sure `sh1106.py` is uploaded to the RP2040 along with your main code.

## 🎮 How it works

* **Touch sensor** → changes between display pages.
* **DHT22** → shows temperature and humidity.
* **MPU6050** → reads acceleration and gyro data.
* **OLED** → shows environment, flight HUD, motion, and system status.
* **LED 1 (GP13)** → lights up when movement is detected.
* **LED 2 (GP14)** → flashes when you change pages.

## 🖥️ OLED Pages

1. 🌡️ **Environment** — Temperature, humidity, MPU temperature
2. ✈️ **Flight HUD** — Roll and pitch using MPU6050
3. 📊 **Motion** — Accelerometer + gyroscope values
4. ⚙️ **System** — Quick sensor status

That's basically it. A tiny RP2040 sensor dashboard with a surprisingly fun little **flight HUD** 😄
