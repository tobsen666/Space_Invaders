import pygame
import random
import time
import _thread
import multiprocessing
import stopit
import itertools as it
import sys
import os

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


background_url = resource_path("C:/development/Space_Invaders/space_stars_sky_night_116649_800x600.jpg")
icon_url = resource_path("C:/development/Space_Invaders/ufo2.png")
player_url = resource_path("C:/development/Space_Invaders/001-space.png")
enemy_url = resource_path("C:/development/Space_Invaders/space-invader-icon.png")
missile_url = resource_path("C:/development/Space_Invaders/005-missile-3.png")
explosion_url = resource_path("C:/development/Space_Invaders/003-explosion-1.png")

# Background
background = pygame.image.load(background_url)

# Caption and icon
pygame.display.set_caption(">> Tobi's Space-Invaders <<")
icon = pygame.image.load(icon_url)
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load(player_url)
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load(enemy_url))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Missile
# Ready - Missile cannot be seen on screen
# Fire - Missile is moving
missile_image = pygame.image.load(missile_url)
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = -0.3
missile_state = "ready"

explosion_image = pygame.image.load(explosion_url)
explosionX = 0
explosionY = 480
explosionY_change = -0.3

score = 0


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_image, (x + 16, y + 16))


def explosion(x, y):
    # now = time.time()
    # timer = 0
    # while timer != 1:
    # end = time.time()
    # timer = round(end - now)
    global score
    score += 1
    for ex in range(500):
        screen.blit(explosion_image, (x, y))


font = pygame.font.Font(None, 36)  # You can adjust the font size


def show_score():
    score_display = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_display, (10, 10))


# game loop (contains all constantly running things)

running = True
while running:
    # RGB - Red, Green, Blue for screen background
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed, check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            # if event.key == pygame.K_UP:
            # playerY_change = -0.3
            # if event.key == pygame.K_DOWN:
            # playerY_change = 0.3
            # missile
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    # get current x-coordinate of spaceship
                    missileX = playerX
                    fire_missile(missileX, missileY)
        # keystroke released means KEYUP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            # playerY_change = 0

    # Checking for boundaries for spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        if enemy_image[i].get_rect(x=enemyX[i], y=enemyY[i]).colliderect(
                missile_image.get_rect(x=missileX, y=missileY)):
            _thread.start_new_thread(explosion, (missileX, missileY))
            missileY = 480
            missile_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Missile movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY += missileY_change

    player(playerX, playerY)

    # Show the score
    show_score()

    pygame.display.update()
