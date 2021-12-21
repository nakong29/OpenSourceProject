#시작하려면 터미널에 "python .\fruitgame.py"를 입력
import pygame
from pygame.rect import *
import random

def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(poop)):
        recPoop[i].y = -1
    for i in range(len(fruit)):
        recFruit[i].y = -1

def eventProcess():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_r:
                restart()

def movePlayer():
    if not isGameOver:
        recPlayer.x += move.x
    if recPlayer.x < 0:
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH-recPlayer.width:
        recPlayer.x = SCREEN_WIDTH-recPlayer.width
    SCREEN.blit(player, recPlayer)

def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True
    time_delay_500ms += 1
    return False

def makePoop():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(poop)-1)
        if recPoop[idex].y == -1:
            recPoop[idex].x = random.randint(0, SCREEN_WIDTH)
            recPoop[idex].y = 0

def movePoop():
    makePoop()
    for i in range(len(poop)):
        if recPoop[i].y == -1:
            continue
        if not isGameOver:
            recPoop[i].y += 1
        if recPoop[i].y > SCREEN_HEIGHT:
            recPoop[i].y = 0
        SCREEN.blit(poop[i], recPoop[i])

def makeFruit():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(fruit)-1)
        if recFruit[idex].y == -1:
            recFruit[idex].x = random.randint(0, SCREEN_WIDTH)
            recFruit[idex].y = 0

def moveFruit():
    makeFruit()
    for i in range(len(fruit)):
        if recFruit[i].y == -1:
            continue
        if not isGameOver:
            recFruit[i].y += 1
        if recFruit[i].y > SCREEN_HEIGHT:
            recFruit[i].y = 0
        SCREEN.blit(fruit[i], recFruit[i])

def CheckCollision():
    global score, isGameOver
    if isGameOver:
        return
    for rec in recPoop:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
        and recPlayer.top < rec.bottom \
        and rec.left < recPlayer.right \
        and recPlayer.left < rec.right:
            isGameOver = True
            break

def CheckCollisionFruit():
    global score, isGameOver
    if isGameOver:
        return
    for rec in recPlayer:
        #if rec.x == -1:
        #    continue
        for recF in recFruit:
            if recF.y == -1:
                continue
            if recPlayer.top < recF.bottom \
            and recF.top < recPlayer.bottom \
            and recPlayer.left < recF.right \
            and recF.left < recPlayer.right:
            #    rec.x = -1
                recF.y = -1
                score += 10
                break

def blinking():
    global time_delay_4sec, toggle
    time_delay_4sec += 1
    if time_delay_4sec > 40:
        time_delay_4sec = 0
        toggle = ~toggle
    return toggle   
    
def setText():
    mFont = pygame.font.SysFont("arial", 20, True, False)
    SCREEN.blit(mFont.render(f'score: {score}', True, 'green'), (10,10,0,0))
    if isGameOver and blinking():
        SCREEN.blit(mFont.render('Game Over!!', True, 'red'), (150,150,0,0))
        SCREEN.blit(mFont.render('press R - Restart', True, 'red'), (140,170,0,0))

#변수
isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
move = Rect(0,0,0,0)
time_delay_500ms = 0
time_delay_4sec = 0
toggle = False
score = 0
isGameOver = False

#스크린 생성
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Opensource Project 20101265 이나경')

#player 생성
player = pygame.image.load('basket.png')
player = pygame.transform.scale(player,(20,30))
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH/2)
recPlayer.centery = (SCREEN_HEIGHT-15)

#poop 생성
poop = [pygame.image.load('poop.png') for i in range(15)]
recPoop = [None for i in range(len(poop))]
for i in range(len(poop)):
    poop[i] = pygame.transform.scale(poop[i],(20, 20))
    recPoop[i] = poop[i].get_rect()
    recPoop[i].y = -1

#fruit 생성
fruit = [pygame.image.load('fruit.png') for i in range(5)]
recFruit = [None for i in range(len(fruit))]
for i in range(len(fruit)):
    fruit[i] = pygame.transform.scale(fruit[i],(20, 20))
    recFruit[i] = fruit[i].get_rect()
    recFruit[i].y = -1

#기타
clock = pygame.time.Clock()

while isActive:
    SCREEN.fill((0,0,0))
    eventProcess()
    movePlayer()
    movePoop()
    moveFruit()
    CheckCollision()
    CheckCollisionFruit()
    setText()
    pygame.display.flip()
    clock.tick(100)