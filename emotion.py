import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = "311a28ee5d9c48d0a7794b282d216e90"
SPOTIFY_CLIENT_SECRET = "33c84ebc7a874a4a80ccb9ebfe712ca0"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Set up Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state",
    )
)

# Playlist for "happy" emotion
HAPPY_PLAYLIST_URI = "spotify:playlist:6rv8taFNyTz4Zu8VyjBebz"

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start capturing video
cap = cv2.VideoCapture(0)

playlist_playing = False  # Track if the happy playlist is already playing

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
            sp.start_playback(context_uri=HAPPY_PLAYLIST_URI)
            print("Playing happy playlist.")

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
