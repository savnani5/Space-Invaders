# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:45:03 2020
@author: Paras
Space Invaders

"""

import pygame
import random
import sys

pygame.init()

#________________________________________________________

# Game Functions

def player(pl_image, px, py):
    screen.blit(pl_image, (px, py))
    
def enemy(ex, ey, i):
    screen.blit(en_image[i], (ex, ey))
    
def fire_bullet(bl_image, bx, by):
    screen.blit(bl_image, (bx+16, by+10))
    global bullet_state
    bullet_state = 'fire'
    
def collision(ex, ey, bx, by):
    distance = ((ex-bx)**2 + (ey-by)**2)**0.5
    if distance < 27:
        return True
    return False

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
    
def game_over():
     game_over_text = game_over_font.render('GAME OVER', True, (255,255,255))
     screen.blit(game_over_text, (200, 250))
    
#_________________________________________________________

# Create Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')

# Background
background = pygame.image.load('background.png')
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)


# Player Variables
pl_image = pygame.image.load('spaceship.png')
pl_image = pygame.transform.scale(pl_image, (64, 64))
px = 300
py = 480
pl_x_change = 0

# Enemy Variables

en_image = []
ex = []
ey = []
en_x_change = []
en_y_change = []
no_of_enemies = 5

for i in range(no_of_enemies):
    image = pygame.image.load('enemy.png')
    image = pygame.transform.scale(image, (50, 50))
    en_image.append(image)
    ex.append(random.randint(0, 735))
    ey.append(random.randint(20, 100)) 
    en_x_change.append(5) 
    en_y_change.append(40) 

# Bullet Variables
bl_image = pygame.image.load('bullet.png')
bl_image = pygame.transform.scale(bl_image, (32, 32))
bx = 0
by = 480
bx_x_change = 0
by_y_change = 40
bullet_state = 'ready'

# Score variable
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over font
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#Game Loop
while True:
    
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl_x_change = -30
                # print('left arrow pressed')
            if event.key == pygame.K_RIGHT:
                pl_x_change = 30
                # print('right arrow pressed')    
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # Get current X coordinate of the spaceship
                    bx = px
                    # Bullet Sound
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Fire Bullet
                    fire_bullet(bl_image, bx, by)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pl_x_change = 0
                # print('arrow released')   
    
    # Enemy boundary
    for i in range(no_of_enemies):   

        # Game Over
        if ey[i] > 440:
            for j in range(no_of_enemies):
                ey[j] = 2000
            game_over()
            break

        ex[i] += en_x_change[i]
        if ex[i] <= 0:
            en_x_change[i] = 15
            ey[i] += en_y_change[i]
        elif ex[i] >= 736:
            en_x_change[i] = -15  
            ey[i] += en_y_change[i]
            
         #Collision Check
        coll = collision(ex[i], ey[i], bx, by)
        if coll:
            # Explosion Sound
            exp_sound = pygame.mixer.Sound('explosion.wav')
            exp_sound.play()
            by = 480
            bullet_state = 'ready'
            score_value += 10
            ex[i] = random.randint(0, 735)
            ey[i] = random.randint(20, 100)
            
        enemy(ex[i] ,ey[i], i)
    
    # player boundary
    px += pl_x_change
    if px <= 0:
        px = 0
    elif px >= 736:
        px = 736     
        
    # bullet Movement    
    if by <= 0:
        by = 480
        bullet_state = 'ready'
        
    if bullet_state == 'fire':
        fire_bullet(bl_image, bx, by)
        by -= by_y_change
        
            
    player(pl_image, px, py)
    show_score(text_x, text_y)
    pygame.display.update()
    