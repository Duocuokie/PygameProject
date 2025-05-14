import pygame
from pygame.locals import *
from pygame.math import *
import math
import time
import random

from player import Player
from playerProj1 import PlayerProj1
from enemyProj1 import EnemyProj1
from shieldProj import ShieldProj
from camera import Camera
from enemySpawner import EnemySpawner
from healthBar import HealthBar
from score import Score

pygame.init()

FONTDD = pygame.freetype.Font("textures/DigitalDisco.ttf", 16)

Clock = pygame.time.Clock()

PLAYERFIRE = pygame.USEREVENT + 1
SPAWNENEMY = pygame.USEREVENT + 2
ENEMYDIE   = pygame.USEREVENT + 3
ENEMYFIRE = pygame.USEREVENT + 4

WIDTH, HEIGHT = 960, 540
HWIDTH, HHIEGHT = WIDTH//2, HEIGHT//2
FPS = 60

BACKGROUND = pygame.transform.scale_by(pygame.image.load("textures/background.png"), 2)


# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN|SCALED)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()



def main():
    #pygame.display.toggle_fullscreen()
    #Setup player
    player = Player(PLAYERFIRE)
    playerCam = Camera()
    playerCam.position += (HWIDTH, HHIEGHT)
    shield = None

    eSpawner = EnemySpawner(ENEMYDIE, ENEMYFIRE)
    pHealthBar = HealthBar((16, 16))
    gameScore = Score(FONTDD)

    #setup groups
    projectiles = pygame.sprite.Group()
    enemys = pygame.sprite.Group()

    
    pygame.time.set_timer(SPAWNENEMY, 1000)
    #main loop
    run = True
    while run:
        delta = Clock.tick(FPS)/1000
        for event in pygame.event.get():

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
                gameScore.updateScore(event.enemy.score)
                gameScore.updateCombo()
                eSpawner.entityCount[event.enemy.id] -= 1

            elif event.type == ENEMYFIRE:
                Proj = EnemyProj1(event.enemy.playerAngle, event.enemy.position.copy())
                projectiles.add(Proj)

            #quitting
            elif event.type == pygame.QUIT:
                run = False 


        #updating sprites
    
        
        player.update(playerCam.position, delta)
        if shield:
            if player.dash > 5:
                shield.position = player.position
                shield.offsetAngle = player.rotation
                shield.kb = player.charge * 37 + 800
            else:
                shield.kill()
                shield = None

        enemys.update(playerCam.position, player.rect.center, delta)
        projectiles.update(playerCam.position, delta)

        #setting camera to go between player and mouse
        target = (player.position * 4 + Vector2(pygame.mouse.get_pos() - Vector2(HWIDTH, HHIEGHT) + player.position))/5
        playerCam.update(target, (HWIDTH, HHIEGHT))
        pHealthBar.update(player.hp)
        gameScore.update(delta)

        #--Collisions--
        #enemy soft collision
        for e in enemys:
            enemySoftCols = pygame.sprite.spritecollide(e, enemys, False, pygame.sprite.collide_circle)
            if enemySoftCols:
                if e != enemySoftCols[0]:
                    e.softCollide(enemySoftCols[0])
                elif len(enemySoftCols) > 1:
                    e.softCollide(enemySoftCols[1])
        #Enemy vs Player Projectiles
        enemyCols = pygame.sprite.groupcollide(enemys, projectiles, False, False, pygame.sprite.collide_circle_ratio(1.25))
        if enemyCols:
            usedProj = []
            for e in enemyCols:
                p = enemyCols[e][0]
                if p not in usedProj and p.layer == 0:
                    e.damage(p.atk, p)

                    if p == shield:
                        shield.hitCount += 1
                        gameScore.updateScore(2)
                        player.hp = math.floor(clamp(player.hp + shield.hitCount/26 , 0, 50))
    
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

        playerProjCols = pygame.sprite.spritecollide(player, projectiles, False, pygame.sprite.collide_circle)
        if playerProjCols:
            for p in playerProjCols:
                if p.layer == 1:
                    player.damage(p.atk, p)
                    p.kill()
                    if player.hp == 0:
                        run = False
                
        #print(player.hp)

        #--Rendering--

        blitList = []

        #only blits if on screen
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
            pygame.draw.circle(screen, (20, 200, 50, 100), shield.rect.center, 32)

        screen.blit(player.image, player.rect)

        screen.blit(pHealthBar.image, pHealthBar.rect)

        screen.blit(gameScore.image, (448, 0))

        pygame.display.update()


        

#fail save if wrong file is run
if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
