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
HWIDTH, HHIEGHT = WIDTH//2, HEIGHT//2
FPS = 60

BACKGROUND = pygame.transform.scale_by(pygame.image.load("textures/background.png"), 2)


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()





def main():

    #Setup player
    player = Player()
    playerCam = Camera()
    playerCam.position += (WIDTH//2, HEIGHT//2)

    #setup groups
    projectiles = pygame.sprite.Group()
    enemys = pygame.sprite.Group()

    for i in range(3):
        guy = Enemy((400, 200))
        enemys.add(guy)
    
    #main loop
    run = True
    while run:
        delta = Clock.tick(FPS)/1000
        for event in pygame.event.get():

            #spawn projectile  needs rework
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    bal = Projectile(player.rotation, player.position.copy())
                    projectiles.add(bal)

            #quitting
            if event.type == pygame.QUIT:
                run = False 



        #updating sprites
        player.update(playerCam.position, delta)
        enemys.update(playerCam.position, player.rect.center, delta)
        projectiles.update(playerCam.position, delta)

        #setting camera to go between player and mouse
        target = (player.position * 3 + Vector2(pygame.mouse.get_pos() - Vector2(WIDTH//2, HEIGHT//2) + player.position))/4
        playerCam.update(target, (WIDTH//2, HEIGHT//2))

        #Collisions
        #Enemy vs Player Projectiles
        collisions = pygame.sprite.groupcollide(enemys, projectiles, False, False, pygame.sprite.collide_circle_ratio(1.25))
        if collisions:
            print(collisions)
            usedProj = []
            for e in collisions:
                p = collisions[e][0]
                print(e)
                print(collisions[e] )
                if p not in usedProj:
                    e.damage(5, 1)
                    if p.pierce <= 0:
                        usedProj.append(p)
                        p.kill()
                    else:
                        p.pierce -= 1
                collisions[e][0].kill()
            erm = Vector2(1000, 0).rotate(random.uniform(0, 360.0))
            guyagain = Enemy(erm + player.position)
            enemys.add(guyagain)
        #player vs Enemy
        if pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle):
            run = False

        #Rendering
        screen.fill((17, 7, 32))

        blitList = []

        #only blits if on screen
        for enemy in enemys:
            ePos = Vector2(enemy.rect.topleft)
            if abs(ePos.x - HWIDTH) <= WIDTH and abs(ePos.y - HHIEGHT) <= HEIGHT:
                blitList.append((enemy.image, ePos))

        for projectile in projectiles:
            pPos = Vector2(projectile.rect.topleft)
            if abs(pPos.x - HWIDTH) <= WIDTH and abs(pPos.y - HHIEGHT) <= HEIGHT:
                blitList.append((projectile.image, pPos))

        #parralax BG
        screen.blit(BACKGROUND, (playerCam.position.x %256 - HWIDTH, playerCam.position.y %256 - HHIEGHT))

        screen.blits(blitList)

        screen.blit(player.image, player.rect)
        pygame.display.update()

if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
