import RPi.GPIO as GPIO
import pigpio
import time

# Set up GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set the servo pin
servo_pin = 12

# Set up PWM on the servo pin at 50Hz
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    """Sets the servo angle in degrees (0-180)."""
    duty_cycle = 2 + (angle / 180) * 10
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(2)  # Give the servo time to move

try:
    GPIO.output(servo_pin, True)
    while True:
        angle = int(input("Enter angle (0-180): "))
        set_angle(angle)

except KeyboardInterrupt:
    # Clean up GPIO pins on exit
    pwm.stop()
    GPIO.cleanup()
