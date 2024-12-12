import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
# SPOTIFY_CLIENT_ID = "6447bdc28d8649ed840592a2b268ff7a"
# SPOTIFY_CLIENT_SECRET = "f6e67c7cbb734c66a9a4b004923bfe59"
# SPOTIFY_REDIRECT_URI = "http://localhost:8000/callback"


# export SPOTIPY_CLIENT_ID='6447bdc28d8649ed840592a2b268ff7a'
# export SPOTIPY_CLIENT_SECRET='f6e67c7cbb734c66a9a4b004923bfe59'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

scope = "user-modify-playback-state user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results["items"]):
# track = item["track"]
#  print(idx, track["artists"][0]["name"], " – ", track["name"])


# Set up Spotify authentication
# sp = spotipy.Spotify(
# auth_manager=SpotifyOAuth(
# client_id=SPOTIFY_CLIENT_ID,
# client_secret=SPOTIFY_CLIENT_SECRET,
# redirect_uri=SPOTIFY_REDIRECT_URI,
#  scope="user-modify-playback-state user-read-playback-state",
# )
# )


# Playlist for "happy" emotion
HAPPY_PLAYLIST_URI = "spotify:playlist:37i9dQZF1EIgG2NEOhqsD7"

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
            sp.start_playback(context_uri=HAPPY_PLAYLIST_URI)  # errors here
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
