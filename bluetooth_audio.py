import bluetooth
import time
import subprocess

# Function to pair and connect to the iPhone using its known MAC address
def pair_and_connect_iphone(mac_address):
    # Using bluetoothctl to pair, trust, and connect
    print(f"Pairing and connecting to iPhone at {mac_address}...")
    subprocess.run(['bluetoothctl', 'pair', mac_address])
    subprocess.run(['bluetoothctl', 'trust', mac_address])
    subprocess.run(['bluetoothctl', 'connect', mac_address])
    
    # Wait a bit to allow the connection to be established
    time.sleep(5)
    print("Connected to iPhone.")
    
# Function to start PulseAudio and monitor Bluetooth audio sink
def start_pulseaudio_monitor():
    # Start PulseAudio if it's not running
    subprocess.run(['pulseaudio', '--start'])
    
    # Run pavucontrol to monitor and manage the Bluetooth audio stream
    print("Starting PulseAudio monitor...")
    subprocess.run(['pavucontrol'])
    
    # This will allow the user to interact with PulseAudio if needed.
    print("Monitoring PulseAudio. Press Ctrl+C to exit.")
    
# Main function to handle the Bluetooth connection and audio stream
def main():
    # iPhone's MAC address (replace with the actual address)
    iphone_mac_address = "C0:2C:5C:3B:68:AB"  # Example MAC address

    # Pair, trust, and connect to the iPhone
    pair_and_connect_iphone(iphone_mac_address)

    # Start PulseAudio to manage the Bluetooth audio stream
    start_pulseaudio_monitor()

    # Monitor the audio stream; this keeps the script running and the connection alive
    try:
        while True:
            time.sleep(1)  # Keep the script running to maintain the connection
    except KeyboardInterrupt:
        print("Exiting...")
        # Close the connection to the iPhone (via bluetoothctl)
        subprocess.run(['bluetoothctl', 'disconnect', iphone_mac_address])
        print("Disconnected from iPhone.")

if __name__ == "__main__":
    main()
