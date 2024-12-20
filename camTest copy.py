import cv2
from deepface import DeepFace
import pygame
import random
import time
import RPi.GPIO as GPIO
import datetime, threading
import asyncio
from bleak import BleakScanner

gpio_pins = [24, 23, 22, 27, 17, 4]
pygame.mixer.init()

# bluetooth
async def find_devices():
    print("Scanning for devices....")
    devices = await BleakScanner.discover()
    found = False
    for device in devices:
        #print(f"Name: {device.name}")
        if device.name == "tikaa":
            found = True 
    if found: 
        print("Tika's device located, continue playing music")


# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in gpio_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

pygame.mixer.init()
# HAPPY = pygame.mixer.Sound("happy.mp3")
# SAD = pygame.mixer.Sound("sad.mp3")
# ANGRY = pygame.mixer.Sound("anger.mp3")
# NEUTRAL = pygame.mixer.Sound("noot.mp3")
HAPPY = "happy2.mp3"
SAD = "sad2.mp3"
ANGRY ="anger2.mp3"
NEUTRAL = "nootnoot.mp3"

sound = None



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
        time.sleep(0.045)


# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start capturing video
cap = cv2.VideoCapture(0)

def playSong():
    sound.play()
    time.sleep(15)

try:
    timerThread = threading.Thread(target=toggleLEDRow)
    #timerThread.daemon = True
    timerThread.start()
    
    while True:
        
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB format
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for x, y, w, h in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = rgb_frame[y : y + h, x : x + w]

            # Perform emotion analysis on the face ROI
            result = DeepFace.analyze(
                face_roi, actions=["emotion"], enforce_detection=False
            )

            # Determine the dominant emotion
            emotion = result[0]["dominant_emotion"]

            # If emotion is "happy" and playlist isn't already playing, start the playlist

            if emotion == "happy":
                sound = HAPPY
                #pygame.mixer.music.load(HAPPY)
                #sound.play()
                #print("playing happy")
            elif emotion == "sad":
                sound = SAD
                #pygame.mixer.music.load(SAD)
                #sound.play()
                #print("playing sad")
            elif emotion == "angry":
                sound = ANGRY
                #pygame.mixer.music.load(ANGRY)
                #sound.play()
                #print("playing angry")
            elif emotion== "neutral":
                sound = NEUTRAL
            else: 
                sound = None
                
                #sound.play()
                #print("playing neutral")
            #songThread = threading.Thread(target=playSong)
            #songThread.start()
            #songThread.join()
            #playing = sound.play()
            if sound and not pygame.mixer.music.get_busy():
                print("playing " + emotion)
                asyncio.run(find_devices())
                pygame.mixer.music.load(sound)
                pygame.mixer.music.play()

            
            # Draw rectangle around face and label with predicted emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2
            )

        # Display the resulting frame
        cv2.imshow("Real-time Emotion Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
except KeyboardInterrupt:
    pass
finally:
    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()