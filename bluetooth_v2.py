from bluepy.btle import Peripheral, UUID

# Replace with your iPhone's Bluetooth address
iphone_address = "XX:XX:XX:XX:XX:XX"

try:
    iphone = Peripheral(iphone_address)
    # ... rest of your code to interact with the iPhone
except Exception as e:
    print("Error connecting to iPhone:", e)