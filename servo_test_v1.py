import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
servo_pin = 12          # GPIO pin connected to the servo signal wire
GPIO.setup(servo_pin, GPIO.OUT)  # Set the pin to output mode

# Start PWM on GPIO18 with a frequency of 33.33Hz
pwm = GPIO.PWM(servo_pin, 50)  # Set PWM frequency to 33.33Hz for 30ms pulse cycle

pwm.start(0)  # Start PWM with a 0% duty cycle

try:
    # Sweep the servo from 0 to 180 degrees
    GPIO.output(servo_pin, True)
    angle = int(input("Enter angle (0-180): "))
    duty_cycle = 2 + (angle / 180) * 10
    pwm.ChangeDutyCycle(duty_cycle)
    #for duty_cycle in range(2, 12):  # Duty cycle between 3% and 6% (1ms to 2ms)
    #    pwm.ChangeDutyCycle(duty_cycle)
    #    print('waiting')
    #    time.sleep(5)  # Wait for the servo to reach the position
    time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()  # Stop the PWM signal
    GPIO.cleanup()  # Clean up the GPIO settings
    print("GPIO cleaned up and PWM stopped")
