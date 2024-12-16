import RPi.GPIO as GPIO


# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
#GPIO.setup(13, GPIO.OUT)
#GPIO.setup(2, GPIO.OUT)
GPIO.output(17,True)
#GPIO.output(13,GPIO.HIGH)
#GPIO.output(2,GPIO.HIGH)
i = 0
while (i < 10000000):
 i = i + 1
 print('alive')
