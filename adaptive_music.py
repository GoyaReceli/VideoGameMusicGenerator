## USE A JOYSTICK TO CONTROL THE INTENSITY AND WINNING VALUES MANUALLY
## LEFT STICK CONTROLS INTENSITY AND RIGHT STICK CONTROLS WINNING STATUS

import pygame, sys
from pygame.locals import *

## Setting up pygame
pygame.mixer.init()
startX = 1200
startY = 800
WIN = pygame.display.set_mode((int(startX), int(startY)))
pygame.display.set_caption("Adaptive Music")


## Setting up the joystick
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


## Setting up pre-recorded music files
pygame.mixer.music.load('music/Intense.mp3')
pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/Intense.mp3'))
pygame.mixer.Channel(0).set_volume(0.5)

pygame.mixer.music.load('music/Calm.mp3')
pygame.mixer.Channel(1).play(pygame.mixer.Sound('music/Calm.mp3'))
pygame.mixer.Channel(1).set_volume(0.5)

pygame.mixer.music.load('music/Win.mp3')
pygame.mixer.Channel(2).play(pygame.mixer.Sound('music/Win.mp3'))
pygame.mixer.Channel(2).set_volume(0.5)

pygame.mixer.music.load('music/WinIntense.mp3')
pygame.mixer.Channel(3).play(pygame.mixer.Sound('music/WinIntense.mp3'))
pygame.mixer.Channel(3).set_volume(0.0)


## Initializing variables
intensity = 0.5
winning = 0.5

while True:

    ## Key Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == JOYAXISMOTION:
            if event.axis == 1:
                intensity = (1 - event.value) / 2
            if event.axis == 3:
                winning = (1 - event.value) / 2


    ## Set volumes of the channels
    pygame.mixer.Channel(0).set_volume(intensity)
    pygame.mixer.Channel(1).set_volume(1 - intensity)
    pygame.mixer.Channel(2).set_volume(winning)
    if intensity > 0.5 and winning > 0.5:
        pygame.mixer.Channel(3).set_volume((winning-0.5) + (intensity-0.5))

