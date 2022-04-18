import pygame
import math
import random

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load("Learning/Graphic/background.png")

#Background Music
mixer.music.load("Learning/Music/background2.ogg")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("Learning/Graphic/spaceship.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("Learning/Graphic/player.png")
playerX = 370
playerY = 480
playerXchange = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load("Learning/Graphic/enemy.png"))
    enemyX.append(random.randint(0, 740))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(1)
    enemyYchange.append(40)

#Bullet // Ready = not seen // Fire = Seen and Moving
bulletImg = pygame.image.load("Learning/Graphic/shot.png")
bulletX = 0
bulletY = 430
bulletXchange = 0.3
bulletYchange = 5
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score :" +str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
    



running = True
# Main loop
while running:
    #RGB
    screen.fill((0, 0, 0))
    #background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #keystroke checking left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.8
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.8
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("Learning/Music/laser.wav")
                bullet_sound.play()
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
        
#Checking of boundaries of spaceships
    playerX += playerXchange

    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740
#Enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 400:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 1
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 740:
            enemyXchange[i] = -1  
            enemyY[i] += enemyYchange[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("Learning/Music/explosion.wav")
            explosion_sound.play()
            bulletY = 430
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 740)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

#Shot Movement
    if bulletY <= 0:
        bulletY = 430
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

 
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()