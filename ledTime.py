import RPi.GPIO as GPIO
import time
import machine

led_pin = 17 # Replace '2' with the GPIO pin connected to your LED


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17,False)
led_status = False
timer = machine.Timer(-1) # Create a timer object


def toggle_led(timer):
   led_status = not led_status
   GPIO.output(17,led_status) # Toggle the LED state

timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=toggle_led)