import pygame
from pygame.locals import *
from pygame.math import *
import math
import time
import random

from player import Player
from enemy import Enemy
from projectile import Projectile
from camera import Camera

pygame.init()


Clock = pygame.time.Clock()



WIDTH, HEIGHT = 960, 720
FPS = 60


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()





def main():
    player = Player()
    playerCam = Camera()
    playerCam.position += (WIDTH//2, HEIGHT//2)

    projectiles = pygame.sprite.Group()
    enemys = pygame.sprite.Group()

    for i in range(3):
        guy = Enemy((400, 200))
        enemys.add(guy)
    run = True
    while run:
        delta = Clock.tick(FPS)/1000
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    bal = Projectile(player.rotation, player.position.copy())
                    projectiles.add(bal)


            if event.type == pygame.QUIT:
                run = False 

        target = (player.position * 4 + Vector2(pygame.mouse.get_pos() - Vector2(WIDTH//2, HEIGHT//2) + player.position))/5
        playerCam.update(target, (WIDTH//2, HEIGHT//2))
        player.update(playerCam.position, delta)
        enemys.update(playerCam.position, player.rect.center, delta)
        projectiles.update(playerCam.position, delta)


        if pygame.sprite.groupcollide(enemys, projectiles, True, True, pygame.sprite.collide_circle_ratio(1.2)):
            erm = Vector2(1000, 0).rotate(random.uniform(0, 360.0))
            guyagain = Enemy(erm + player.position)
            enemys.add(guyagain)

        if pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle):
            run = False

        screen.fill((17, 7, 32))

        projectiles.draw(screen)
        enemys.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.update()

if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
