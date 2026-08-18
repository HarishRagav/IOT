import network
import time

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Scanning Wi-Fi networks...\n")

networks = wifi.scan()

# Sort by signal strength (strongest first)
networks.sort(key=lambda x: x[3], reverse=True)

for i, net in enumerate(networks, 1):
    ssid = net[0].decode("utf-8", "ignore")
    bssid = ":".join("{:02X}".format(b) for b in net[1])
    channel = net[2]
    rssi = net[3]
    security = net[4]
    hidden = net[5]

    # Security type
    security_names = {
        0: "OPEN",
        1: "WEP",
        2: "WPA-PSK",
        3: "WPA2-PSK",
        4: "WPA/WPA2-PSK",
        5: "WPA2-Enterprise"
    }

    sec_name = security_names.get(security, "UNKNOWN")

    print("NETWORK", i)
    print("SSID     :", ssid if ssid else "[Hidden]")
    print("BSSID    :", bssid)
    print("Channel  :", channel)
    print("Signal   :", rssi, "dBm")
    print("Security :", sec_name)
    print("Hidden   :", bool(hidden))
    print("-" * 35)

print("\nScan complete!")