import pygame
from pygame.locals import *
from pygame.math import *
import math

#file imports

from player import Player
from playerProj1 import PlayerProj1
from shieldProj import ShieldProj
from camera import Camera

from enemySpawner import EnemySpawner
from enemyProj1 import EnemyProj1

from healthBar import HealthBar
from score import Score
from button import Button

import audio

pygame.init()


Clock = pygame.time.Clock()

#Custom events
PLAYERFIRE = pygame.USEREVENT + 1
SPAWNENEMY = pygame.USEREVENT + 2
ENEMYDIE   = pygame.USEREVENT + 3
ENEMYFIRE = pygame.USEREVENT + 4
BUTTONPRESSED = pygame.USEREVENT + 5


#load grphics
FONTDD = pygame.freetype.Font("textures/DigitalDisco.ttf", 16)
BACKGROUND = []
TITLE = pygame.image.load("textures/background.png")


for i in range(2):
    BACKGROUND.append(pygame.image.load(f"textures/background{i + 1}.png"))

#button images

RETRY = [
    pygame.image.load("textures/retry1.png"),
    pygame.image.load("textures/retry2.png"),
    pygame.image.load("textures/retry3.png")
]

EXIT = [
    pygame.image.load("textures/exit1.png"),
    pygame.image.load("textures/exit2.png"),
    pygame.image.load("textures/exit3.png")
]

PLAY = [
    pygame.image.load("textures/play1.png"),
    pygame.image.load("textures/play2.png"),
    pygame.image.load("textures/play3.png")
]

HELP = [
    pygame.image.load("textures/help1.png"),
    pygame.image.load("textures/help2.png"),
    pygame.image.load("textures/help3.png"),
    pygame.image.load("textures/help4.png")
]


#display settings
WIDTH, HEIGHT = 960, 540
HWIDTH, HHIEGHT = WIDTH//2, HEIGHT//2
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN|SCALED)
pygame.display.set_caption("Not Brawlloon")
clock = pygame.time.Clock()

#manages highscore saved in stats.txt
def loadHighscore():
    with open("stats.txt", 'r') as f:
        h = f.read()
    try:
        h = int(h)
    except:
        with open("stats.txt", "w") as f:
            f.write(str(0))
        h = 0

    return(h)
    
def saveHighscore(score):
    
    with open("stats.txt", "w") as f:
        f.write(str(score))

#start menu
def start():
    #sets up buttons
    startBut = Button((HWIDTH, HHIEGHT), PLAY, 0, BUTTONPRESSED)
    exitBut = Button((48, 48), EXIT, 1, BUTTONPRESSED)
    helpBut = Button((WIDTH - 32, 32), HELP, 4, BUTTONPRESSED)
    action = None
    isHelp = False
    run = True
    audio.playMusic(1)
    while run:
        delta = Clock.tick(FPS)/1000

        #quits or plays game depending on button
        for event in pygame.event.get():
            if event.type == BUTTONPRESSED:
                if event.id == 0:
                    action = 1
                    run = False
                elif event.id == 1:
                    action = "quit"
                    run = False
                elif event.id == 4:
                    isHelp = not isHelp
            #quitting
            elif event.type == pygame.QUIT:
                quitting = True
                run = False 

        startBut.update()
        exitBut.update()
        helpBut.update()
        
        screen.blit(TITLE, (0, 0))

        #show controls
        if isHelp:
            screen.blit(HELP[3], (0, HEIGHT - 128))

        screen.blit(startBut.image, startBut.rect)
        screen.blit(exitBut.image, exitBut.rect)
        screen.blit(helpBut.image, helpBut.rect)

        pygame.display.update()
    return(action)

#gameplay
def game():
    highscore = loadHighscore()

    #Setup objectas
    player = Player(PLAYERFIRE)
    playerCam = Camera()
    playerCam.position += (HWIDTH, HHIEGHT)
    shield = None

    eSpawner = EnemySpawner(ENEMYDIE, ENEMYFIRE)
    pHealthBar = HealthBar((16, 16))
    gameScore = Score(FONTDD, highscore)

    #setup groups
    projectiles = pygame.sprite.Group()
    enemys = pygame.sprite.Group()

    #variables for the death screen
    screenSurf = pygame.Surface((WIDTH, HEIGHT))
    deathImage = None
    Retry = None

    
    pygame.time.set_timer(SPAWNENEMY, 1000)
    #main loop
    run = True
    action = 0

    audio.playMusic(0)

    while run:
        delta = Clock.tick(FPS)/1000
        if player.hp > 0:
            print(highscore)
            for event in pygame.event.get():
                #player shoots
                if event.type == PLAYERFIRE:
                    Proj = PlayerProj1(player.rotation, player.position.copy(), player.charge)
                    projectiles.add(Proj)
                    #create sheild
                    if player.dash > 5 and shield == None:
                        shield = ShieldProj(player.rotation, player.position)
                        projectiles.add(shield)
                #spawn enemy
                elif event.type == SPAWNENEMY:
                    enemys = eSpawner.spawn(player.position, enemys)
                    eSpawner.time += 1
                #enemy dies
                elif event.type == ENEMYDIE:
                    audio.SfxObjs[5].play()
                    highscore = gameScore.updateScore(event.enemy.score)
                    gameScore.updateCombo()
                    eSpawner.entityCount[event.enemy.id] -= 1
                #enemy attacks
                elif event.type == ENEMYFIRE:
                    Proj = EnemyProj1(event.enemy.playerAngle, event.enemy.position.copy())
                    projectiles.add(Proj)

                #quitting
                elif event.type == pygame.QUIT:
                    action = "quit"
                    run = False 


            #updating sprites and game objects
            player.update(playerCam.position, delta)
            if shield:
                #manages shield
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
                        audio.SfxObjs[4].play()
                        #shield actions
                        if p == shield:
                            shield.hitCount += 1
                            highscore = gameScore.updateScore(1)
                            #heals player
                            player.hp = math.floor(clamp(player.hp + shield.hitCount/24 , 0, 50))
                        #manages piercing
                        elif p.pierce <= 0:
                            usedProj.append(p)
                            p.kill()
                        else:
                            p.pierce -= 1
            
            #player vs Enemy
            playerCols = pygame.sprite.spritecollide(player, enemys, False, pygame.sprite.collide_circle)
            if playerCols:
                #damges player
                e = playerCols[0]
                
                player.damage(e.atk, e)

            #player vs enemy projectiles
            playerProjCols = pygame.sprite.spritecollide(player, projectiles, False, pygame.sprite.collide_circle)
            if playerProjCols:
                for p in playerProjCols:
                    if p.layer == 1:
                        player.damage(p.atk, p)
                        p.kill()
                    
            

            #--Rendering--

            blitList = []

            #only blit if on screen
            for enemy in enemys:
                ePos = Vector2(enemy.rect.topleft)

                #loops enemys around it too far away
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
                if abs(pPos.x - HWIDTH) <= WIDTH and abs(pPos.y - HHIEGHT) <= HEIGHT :
                    blitList.append((projectile.image, pPos))


            #parralax BG
            bgList = []
            for bg in range(len(BACKGROUND)):
                
                bgList.append((BACKGROUND[bg], (playerCam.position.x * ((bg + 1)/6) %256 - HWIDTH, playerCam.position.y * ((bg + 1)/6) %256 - HHIEGHT)))

            screenSurf.blits(bgList)
            screenSurf.blits(blitList)


            screenSurf.blit(player.image, player.rect)
            screenSurf.blit(pHealthBar.image, pHealthBar.rect)
            screenSurf.blit(gameScore.image, (448, 0))
            screen.blit(screenSurf, (0, 0))

            #setsup death screen
            if player.hp == 0:
                if highscore > loadHighscore():
                    saveHighscore(highscore)
                pHealthBar.update(player.hp)
                screenSurf.blit(pHealthBar.image, pHealthBar.rect)
                deathImage = screenSurf.copy()
                deathImage.set_alpha(100)
                Retry = Button((HWIDTH, HHIEGHT+128), RETRY, 2, BUTTONPRESSED)
                Back = Button((48, HEIGHT - 48), EXIT, 3, BUTTONPRESSED)
        #death screen
        else:
            for event in pygame.event.get():
                #quitting
                if event.type == pygame.QUIT:
                    action = "quit"
                    run = False
    
                if event.type == BUTTONPRESSED:
                    #restart
                    if event.id == 2:
                        action = 1
                        run = False
                        #menu
                    elif event.id == 3:
                        action = 0 
                        run = False
            text = pygame.Surface((512, 256), SRCALPHA)
            text.fill((0, 0, 0, 0))
        
            #display score
            scoreText = FONTDD.render(f"{gameScore.score}", (255, 255, 255), size = 96)
            text.blit(scoreText[0], (256 - scoreText[1].width//2, 0))

            highText = FONTDD.render(f"{loadHighscore()}", (255, 255, 255), size = 64)
            text.blit(highText[0], (256 - highText[1].width//2, 80))

            Retry.update()
            Back.update()
            screen.fill((0, 0, 0))
            screen.blit(deathImage, (0, 0))
            screen.blit(Retry.image, Retry.rect)
            screen.blit(Back.image, Back.rect)
            screen.blit(text, (HWIDTH-256, HHIEGHT-64))


        pygame.display.update()
    return(action)


def main():

    scene = 0
    run = True

    #scenes are functions and they return the nect scene
    while run:
        if scene == 0:
            scene = start()
        elif scene == 1:
            scene = game()
        elif scene == "quit":
            run = False
        

        

#fail save if wrong file is run
if __name__ == '__main__':
    main()

# Quits PyGame
pygame.quit()
