import asyncio
from bleak import BleakScanner, BleakClient

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)  # Find your iPhone's device address
        #printf()"Found device: {device.address} - {device.name}")


    address = "C0:2C:5C:3B:68:AB"  # Katie Phone Address
    # Saloni bt: 3C:06:30:34:B3:16
    # Sathvika bt: A0:78:17:84:B7:C8
    # Tika bt: 
    async with BleakClient(address) as client:
        print("Connected to:", address)

        # Example: Read a characteristic
        characteristic_uuid = "YOUR_CHARACTERISTIC_UUID"  # Replace with the appropriate UUID
        value = await client.read_gatt_char(characteristic_uuid)
        print("Characteristic value:", value)

if __name__ == "__main__":
    asyncio.run(main())