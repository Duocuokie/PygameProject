import pygame
from pygame.locals import *

#ui button object

class Button():
    def __init__(self, pos, sprites, id, event):
        #sprites for normal hover and click
        self.sprites = sprites
        self.image = sprites[0]
        self.rect = self.image.get_rect() 
        self.rect.center = pos

        # the id will be used track what it does in the event
        self.id = id
        self.wasPresesed = False
        self.event = event

    def update(self):
        #send event if button was released and was pressed last frame
        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mousePos):
            if mouseClick[0]:
                self.image = self.sprites[2]
                self.wasPresesed = True
            else:
                if self.wasPresesed:
                     pygame.event.post(pygame.event.Event(self.event, {"id" : self.id}))
                self.image = self.sprites[1]
                self.wasPresesed = False
        else:
            if not mouseClick[0]:
                self.wasPresesed = False
            self.image = self.sprites[0]
            

    