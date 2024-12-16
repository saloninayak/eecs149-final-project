import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load your audio file (replace "your_audio.wav" with your file path)
# sound = pygame.mixer.Sound("your_audio.wav")
sound = pygame.mixer.Sound("/home/djmoody2/DJ Moody Project/Mary.mp3")

# Play the sound
playing = sound.play()

# Keep the program running until you close it
while playing.get_busy():
    pygame.time.delay(100)
    print('playing')

# Quit pygame
pygame.quit()