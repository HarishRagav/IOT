import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

networks = wifi.scan()

for net in networks:
    ssid = net[0].decode()
    rssi = net[3]

    print("Wi-Fi:", ssid, "| Signal:", rssi)