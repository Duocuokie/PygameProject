import pygame
from pygame.locals import *
from pygame.math import *
import math
import time
import random

from player import Player
from playerProj1 import PlayerProj1
from shieldProj import ShieldProj
from camera import Camera
from enemySpawner import EnemySpawner


pygame.init()


Clock = pygame.time.Clock()

PLAYERFIRE = pygame.USEREVENT + 1
SPAWNENEMY = pygame.USEREVENT + 2
ENEMYDIE   = pygame.USEREVENT + 3

WIDTH, HEIGHT = 960, 720
HWIDTH, HHIEGHT = WIDTH//2, HEIGHT//2
FPS = 60

BACKGROUND = pygame.transform.scale_by(pygame.image.load("textures/background.png"), 2)


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


eSpawner = EnemySpawner(ENEMYDIE)

def main():
    
    #Setup player
    player = Player(PLAYERFIRE)
    playerCam = Camera()
    playerCam.position += (HWIDTH, HHIEGHT)
    shield = None

    #setup groups
    projectiles = pygame.sprite.Group()
    enemys = pygame.sprite.Group()

    
    pygame.time.set_timer(SPAWNENEMY, 1000)
    #main loop
    run = True
    while run:
        delta = Clock.tick(FPS)/1000
        for event in pygame.event.get():

            #spawn projectile  needs rework
            if event.type == PLAYERFIRE:
                Proj = PlayerProj1(player.rotation, player.position.copy(), player.charge)
                projectiles.add(Proj)
                if player.dash > 5 and shield == None:
                    shield = ShieldProj(player.rotation, player.position)
                    projectiles.add(shield)
                
            elif event.type == SPAWNENEMY:
    
                
                enemys = eSpawner.spawn(player.position, enemys)
                eSpawner.time += 1

            elif event.type == ENEMYDIE:
                eSpawner.entityCount[event.enemy.id] -= 1



            #quitting
            elif event.type == pygame.QUIT:
                run = False 



        #updating sprites
    
        
        player.update(playerCam.position, delta)
        if shield:
            if player.dash > 5:
                shield.position = player.position
                shield.offsetAngle = player.rotation
                shield.kb = player.charge * 37 + 1000
            else:
                shield.kill()
                shield = None

        enemys.update(playerCam.position, player.rect.center, delta)
        projectiles.update(playerCam.position, delta)

        #setting camera to go between player and mouse
        target = (player.position * 3 + Vector2(pygame.mouse.get_pos() - Vector2(HWIDTH, HHIEGHT) + player.position))/4
        playerCam.update(target, (HWIDTH, HHIEGHT))

        #--Collisions--
        #enemy soft collision
        for e in enemys:
            enemySoftCols = pygame.sprite.spritecollide(e, enemys, False, pygame.sprite.collide_circle)
            if enemySoftCols:
                if e != enemySoftCols[0]:
                    e.softCollide(enemySoftCols[0])
                elif len(enemySoftCols) > 1:
                    e.softCollide(enemySoftCols[1])
        #Enemy vs Player Projectilesddds
        enemyCols = pygame.sprite.groupcollide(enemys, projectiles, False, False, pygame.sprite.collide_circle_ratio(1.25))
        if enemyCols:
            usedProj = []
            for e in enemyCols:
                p = enemyCols[e][0]
                if p not in usedProj:
                    e.damage(p.atk, p)

                    if p == shield:
                        shield.hitCount += 1
                        player.hp = math.floor(clamp(player.hp + shield.hitCount/16 , 0, 50))
    
                    elif p.pierce <= 0:
                        usedProj.append(p)
                        p.kill()
                    else:
                        p.pierce -= 1
        
        #player vs Enemy
        playerCols = pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle)
        if playerCols:
            e = playerCols[0]
            
            player.damage(e.atk, e)
            if player.hp == 0:
                run = False
                
        print(player.hp)

        #--Rendering--

        blitList = []

        #only blit if on screen
        for enemy in enemys:
            ePos = Vector2(enemy.rect.topleft)

            ePlayerDist = enemy.position - player.position
            if abs(ePlayerDist[0]) > 1500:
                sign = math.copysign(1, ePlayerDist[0])
                enemy.position.x += -sign * 3000
            if abs(ePlayerDist[1]) > 1500:
                sign = math.copysign(1, ePlayerDist[1])
                enemy.position.y += -sign * 3000

            if abs(ePos.x - HWIDTH) <= WIDTH and abs(ePos.y - HHIEGHT) <= HEIGHT:
                blitList.append((enemy.image, ePos))
            




        for projectile in projectiles:
            pPos = Vector2(projectile.rect.topleft)
            if abs(pPos.x - HWIDTH) <= WIDTH and abs(pPos.y - HHIEGHT) <= HEIGHT and projectile != shield:
                blitList.append((projectile.image, pPos))
        

        #parralax BG
        screen.blit(BACKGROUND, (playerCam.position.x %256 - HWIDTH, playerCam.position.y %256 - HHIEGHT))

        screen.blits(blitList)

        if shield:
            pygame.draw.circle(screen, (20, 200, 50, 100), shield.rect.center, 40)

        screen.blit(player.image, player.rect)
        pygame.display.update()


        

#fail save if wrong file is run
if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
