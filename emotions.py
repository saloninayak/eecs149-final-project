import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# SPOTIFY VARIABLES
SPOTIPY_CLIENT_ID = "6447bdc28d8649ed840592a2b268ff7a"
SPOTIPY_CLIENT_SECRET = "f6e67c7cbb734c66a9a4b004923bfe59"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-modify-playback-state user-read-playback-state"

# Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE
    )
)

# PLAYLIST IDS AND TRACKS
# HAPPY_PLAYLIST_URI = "spotify:playlist:37i9dQZF1EIgG2NEOhqsD7"

HAPPY_URI = "spotify:playlist:2mOB2Yer40pX3Og7OcCu6c"
SAD_URI = "spotify:playlist:5UbBTbqrx4kb2f0mCtXI8v"
NEUTRAL_URI = "spotify:playlist:7lKHu924iTf0gRJnpIHfn7"
ANGRY_URI = "spotify:playlist:1qgBdeNcnseR4GiiWfF7ai"


def is_song_playing():
    playback_state = sp.current_playback()
    if playback_state and playback_state["is_playing"]:
        return True
    return False


# Function to wait for the song to finish
def wait_for_song_to_end():
    while True:
        playback_state = sp.current_playback()

        # Ensure playback_state exists and there's an active track
        if playback_state and playback_state["is_playing"]:
            progress_ms = playback_state["progress_ms"]
            duration_ms = playback_state["item"]["duration_ms"]

            # Check if the song has ended
            if progress_ms >= duration_ms - 1000:  # Allow slight buffer for precision
                sp.pause_playback()  # Explicitly pause playback
                print("Song ended. Playback paused.")
                break
        else:
            print("No active playback. Waiting...")

        time.sleep(1)  # Polling interval to avoid API spamming


# Start capturing video
cap = cv2.VideoCapture(0)

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
            playlist_uri = HAPPY_URI
            print("playing happy")
        elif emotion == "sad":
            playlist_uri = SAD_URI
            print("playing sad")
        elif emotion == "angry":
            playlist_uri = ANGRY_URI
            print("playing angry")
        else:
            playlist_uri = NEUTRAL_URI
            print("playing neutral")

        # Play the selected playlist
        sp.start_playback(context_uri=playlist_uri)

        # Wait for the song to finish before re-analyzing
        wait_for_song_to_end()

        # Break the loop to prevent re-detection during the current song
        break

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

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()