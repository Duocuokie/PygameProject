import pygame
from pygame.locals import *
from pygame.math import *
import math

pygame.init()
#askfhksadhf

Clock = pygame.time.Clock()

DUCKIMAGE = pygame.image.load("textures/DuckSprites.png")

WIDTH, HEIGHT = 800, 600
FPS = 60


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

class ball(pygame.sprite.Sprite):
    def __init__(self, angle, pos):
        super().__init__()
        self.dir = dir
        self.image = pygame.Surface((16, 16))
        self.image.fill((220, 175, 30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.velocity = Vector2(500, 0).rotate(-angle)
        
    def update(self, delta):
        self.rect.move_ip(self.velocity * delta)
        

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
   
        #self.image = DUCKIMAGE
        self.image = pygame.image.load('textures/bar.png')
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.velocity = Vector2(0.0, 0.0)
        self.maxSpeed = 6
        self.acceleration = 60
        self.friction = 30
        self.direction = Vector2(0, 0)
        self.mouseDir = [0, 0]
        self.mouseAngle = 0.0

    def applyAccel(self, dir, delta):
        self.velocity = self.velocity.move_towards(dir * self.maxSpeed, self.acceleration * delta)


    def applyFriction(self, delta):
        self.velocity = self.velocity.move_towards(Vector2(0, 0), self.friction * delta)

    def update(self, delta):
        keys = pygame.key.get_pressed()
        self.direction = Vector2(0, 0)
        self.direction[0] = int(keys[K_d]) - int(keys[K_a])
        self.direction[1] = int(keys[K_s]) - int(keys[K_w])

        if self.direction == [0, 0]:
            player.applyFriction(delta)
        else:
            self.direction = self.direction.normalize()
            player.applyAccel(self.direction, delta)

        self.rect.move_ip(self.velocity[0], self.velocity[1])
        self.mouseDir = (Vector2(pygame.mouse.get_pos()) - Vector2(self.rect.center))
        self.mouseAngle = -math.degrees(math.atan2(self.mouseDir[1], self.mouseDir[0]))
        prevCenter = self.rect.center
        self.image = pygame.image.load('textures/bar.png')
        self.image = pygame.transform.rotate(self.image, self.mouseAngle)
        self.rect = self.image.get_rect()
        self.rect.center = prevCenter
player = Player()

projectiles = pygame.sprite.Group()

def main():
    run = True
    delta = Clock.tick(FPS)/1000
    while run:

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    
                    bal = ball(player.mouseAngle, player.rect.center)
                    print(player.mouseAngle, -math.degrees(math.atan2(bal.velocity[1], bal.velocity[0])))
                    projectiles.add(bal)


            if event.type == pygame.QUIT:
                run = False

        player.update(delta)
        projectiles.update(delta)

        screen.fill((0, 0, 0))

        projectiles.draw(screen)
        screen.blit(player.image, player.rect)

        pygame.display.update()
        delta = Clock.tick(FPS)/1000

if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
