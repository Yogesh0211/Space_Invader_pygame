import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invader")

backgroundImg = pygame.image.load("background1.png")

playerImg = pygame.image.load("Ufo.png")
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(5)
    enemyY_change.append(30)

bulletImg = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 470
bulletX_change = playerX_change
bulletY_change = 10
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 32)


def game_over(x, y):
    over = over_font.render("GAME OVER" + str(score), True, (255, 255, 255))
    screen.blit(over, (200, 250))


def showscore(X, Y):
    score_show = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_show, (X, Y))


def player(X, Y):
    screen.blit(playerImg, (playerX, playerY))


def enemy(X, Y, i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def background():
    screen.blit(backgroundImg, ())


def bullet(X, Y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (X, Y))


def bullet2(X, Y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (X + 33, Y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 40:
        return True
    else:
        return False


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_UP:
                playerY_change = -10
            if event.key == pygame.K_DOWN:
                playerY_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet(playerX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))

    pygame.display.update()

    # player movement
    playerY += playerY_change
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY > 536:
        playerY = 536

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bulletX = playerX
        bullet_state = "ready"

    if bullet_state == "Fire":
        bullet(bulletX, bulletY)
        bullet2(bulletX, bulletY)
        bulletY -= bulletY_change
        bulletX == playerX

    # enemy movement

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 800
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bulletX = playerX
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    showscore(textX, textY)
    pygame.display.update()
