import pigpio
import time

# Initialize the pigpio library and create a pigpio instance
pi = pigpio.pi()

# Check if pigpio is running
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Define the GPIO pin for the servo using BCM numbering (BCM 12 corresponds to GPIO 12)
servo_pin = 12  # BCM pin 12 is the same as physical pin 32

# Set the pin mode to output (though pigpio handles this internally)
pi.set_mode(servo_pin, pigpio.OUTPUT)

# Function to move the servo to a specific angle
def move_servo_to_angle(angle):
    # Convert angle (0-180 degrees) to servo pulse width (500-2500 microseconds)
    pulsewidth = int(500 + (angle / 180.0) * 2000)
    
    # Write the pulse width to the servo pin
    pi.set_servo_pulsewidth(servo_pin, pulsewidth)

# Test: Move the servo from 0 to 180 degrees
try:
    for angle in range(0, 181, 10):  # From 0 to 180 degrees in steps of 10
        print(f"Moving servo to {angle} degrees")
        move_servo_to_angle(angle)
        time.sleep(1)  # Wait for 1 second to observe the movement
        
    for angle in range(180, -1, -10):  # From 180 to 0 degrees in steps of 10
        print(f"Moving servo to {angle} degrees")
        move_servo_to_angle(angle)
        time.sleep(1)  # Wait for 1 second to observe the movement

finally:
    # Stop the servo by sending a pulse width of 0 (turn off the signal)
    pi.set_servo_pulsewidth(servo_pin, 0)
    # Cleanup and release the resources
    pi.stop()
    print("Program finished.")
