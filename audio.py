import pygame
import pygame.mixer

pygame.mixer.init()

#manages all the audio

#sound effects list
SFX = [
    "audio/suck.ogg",
    "audio/fire3.ogg",
    "audio/phit.ogg",
    "audio/pdie.ogg",
    "audio/ehit.ogg",
    "audio/edie.ogg",
]

SfxObjs = []

#music list
MUSIC = [
    "audio/ballon mountain.ogg",
    "audio/ballon plains.ogg"
]

#creates a list of sound objects for each sound file
for sfx in SFX:
    sound = pygame.mixer.Sound(sfx)
    SfxObjs.append(sound)

#plays specified music
def playMusic(key):
    pygame.mixer.music.load(MUSIC[key])
    pygame.mixer.music.play(-1)