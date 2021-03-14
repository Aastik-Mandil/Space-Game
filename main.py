import pygame
import random
import math
from pygame import mixer

pygame.init() # initialise the pygame module
pygame.display.set_caption("Space Invaders") # setting the game title

icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon) # setting the game logo

screen = pygame.display.set_mode((800,600)) # creating the screen

backgroundImg = pygame.image.load("background.png")
# mixer.music.load("background.wav")
# mixer.music.play(-1) # to play continuously we write -1

playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
#bulletX_change = 0.4
bulletY_change = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf",64)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

def player(x,y):
    screen.blit(playerImg, (x,y)) # blitting the image on the surface of screen

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y)) # blitting the image on the surface of screen

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire" # changing the state of bullet
    screen.blit(bulletImg, (x+16,y-5)) # blitting the image on the surface of screen

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance <= 27:
        return True
    return False

def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,green)
    screen.blit(score, (x,y))

def isTouch(enemyX,enemyY,playerX,playerY):
    if abs(enemyY-playerY)<64 or abs(enemyX-playerX)<64:
        return True
    return False

def game_over_text():
    over_text = over_font.render("Score: "+str(score_value),True,green)
    screen.blit(over_text, (250,250))

# game loop
running = True
while running:
    screen.fill(white)
    screen.blit(backgroundImg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_UP:
                playerY_change = -5
            elif event.key == pygame.K_DOWN:
                playerY_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet_sound = mixer.Sound("laser.wav")
                    # bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    if playerX < 0:
        playerX = 0
    elif playerX > 730:
        playerX = 730
    if playerY < 0:
        playerY = 0
    elif playerY > 536:
        playerY = 536

    for i in range(num_of_enemies):
        if enemyY[i] > 480 : # or isTouch(enemyX[i],enemyY[i],playerX,playerY)
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            # explosion_sound = mixer.Sound("explosion.wav")
            # explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,730)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

pygame.quit()
quit()
