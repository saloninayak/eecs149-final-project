import bluetooth
import time
import subprocess
import threading
import RPi.GPIO as GPIO

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
gpio_pins = [18, 13, 6, 5, 27, 17]
# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in gpio_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

exit_event = threading.Event()

def toggleLEDRow():
    next_call = time.time()
    led_status = False
    gpio_pin = 0
    while True:
        GPIO.output(gpio_pins[gpio_pin],led_status)
        #GPIO.output(1,led_status)
        #GPIO.output(2,led_status)
        gpio_pin += 1
        if(gpio_pin > len(gpio_pins) - 1):
            gpio_pin = 0
            led_status = not led_status
        next_call = next_call+0.045 #could pose an overflow problem
        time.sleep(next_call - time.time())

# Function to pair and connect to the iPhone using its known MAC address
def pair_and_connect_iphone(mac_address):
    # Using bluetoothctl to pair, trust, and connect
    print(f"Pairing and connecting to iPhone at {mac_address}...")

    #subprocess.run(['bluetoothctl', 'pair', mac_address])
    #subprocess.run(['bluetoothctl', 'trust', mac_address])
    #subprocess.run(['bluetoothctl', 'connect', mac_address])
    port = 1  # Typically, Bluetooth serial uses port 1
    sock.connect((mac_address, port))
    
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
    #start_pulseaudio_monitor()

    # Monitor the audio stream; this keeps the script running and the connection alive
    try:
        timerThread = threading.Thread(target=toggleLEDRow)
        #timerThread.daemon = True
        timerThread.start()
        while True:
            time.sleep(1)  # Keep the script running to maintain the connection
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        # Close the connection to the iPhone (via bluetoothctl)
        #subprocess.run(['bluetoothctl', 'disconnect', iphone_mac_address])
        sock.close()
        print("Disconnected from iPhone.")
        for pin in gpio_pins:
            GPIO.output(pin, GPIO.LOW)
        time.sleep(5)
        GPIO.cleanup()  # Clean up GPIO pins on exit
        exit_event.set()

if __name__ == "__main__":
    main()