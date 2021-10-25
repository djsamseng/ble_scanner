from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        return
        if isNewDev:
            print("Discovered device", dev.addr, "RSSI=", dev.rssi)
        elif isNewData:
            print("Received new data from", dev.addr, "RSSI=", dev.rssi)
        print(dev.getScanData()[-1][-1])

    def handleNotification(self, cHandle, data):
        print("Notification:", cHandle, data)

def find_device_by_name(scanner, name="SamBeacon", timeout=1):
    devices = scanner.scan(timeout=timeout)
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete Local Name" and value.startswith(name):
                print(value, dev.rssi, dev.addr, dev.addrType)
                addr = dev.addr
                return dev
    return None

def loop():
    last_update = time.time()
    scanner = Scanner().withDelegate(ScanDelegate())

    while True:
        dev = find_device_by_name(scanner)
        if dev is not None:
            last_update = time.time()
        else:
            print("Waiting:", time.time() - last_update)

def main():
    loop()

if __name__ == "__main__":
    main()
# sudo -E python3 ble_scanner.py
