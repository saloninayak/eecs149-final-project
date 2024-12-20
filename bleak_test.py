import asyncio
from bleak import BleakScanner

async def find_devices():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    print(devices)
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}, RSSI: {device.rssi} dBm")

asyncio.run(find_devices())
