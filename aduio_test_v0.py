import pygame



# Initialize pygame mixer
pygame.init()
pygame.mixer.init()



# Load your audio file (replace "your_audio.wav" with your file path)
# sound = pygame.mixer.Sound("your_audio.wav")
sound = pygame.mixer.Sound("Mary.mp3")

# Play the sound
sound.play()



# Keep the program running until you close it
while pygame.event.wait().type != pygame.QUIT:
    pass



# Quit pygame
pygame.quit()
