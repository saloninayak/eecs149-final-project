import datetime, threading, time
import RPi.GPIO as GPIO
import asyncio
import atexit
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
try:
    timerThread = threading.Thread(target=toggleLEDRow)
    #timerThread.daemon = True
    timerThread.start()

except KeyboardInterrupt:
    for pin in gpio_pins:
        GPIO.output(pin, GPIO.LOW)
    time.sleep(5)
    GPIO.cleanup()  # Clean up GPIO pins on exit
    exit_event.set()
    