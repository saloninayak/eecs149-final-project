import bluetooth

# Replace with your iPhone's Bluetooth address
iphone_address = "C0:2C:5C:3B:68:AB"
port = 1  # Typically, Bluetooth serial uses port 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((iphone_address, port))

sock.send("Hello from Raspberry Pi!")
sock.close()
