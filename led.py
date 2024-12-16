import datetime, threading, time
import RPi.GPIO as GPIO
import asyncio


# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
#GPIO.setup(1, GPIO.OUT)
#GPIO.setup(2, GPIO.OUT)
GPIO.output(17,True)
#GPIO.output(1,False)
#GPIO.output(2,False)


def toggleLEDRow():
    next_call = time.time()
    led_status = False
    while True:
        led_status = not led_status
        GPIO.output(17,led_status)
        #GPIO.output(1,led_status)
        #GPIO.output(2,led_status)
        next_call = next_call+2;
        time.sleep(next_call - time.time())

timerThread = threading.Thread(target=toggleLEDRow)
#timerThread.daemon = True
timerThread.start()