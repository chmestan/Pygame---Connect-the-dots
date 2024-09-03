# TIME.SLEEP BEFORE CLEAR
# CORRECTED HITBOX ISSUES WITH DOTS
# CHANGED LINE SPRITE IMAGE
# ADDED TWEENING

import pygame
from sys import exit
from random import randint, choice
import time

pygame.init()

# Dimensions
WIDTH = 1000
HEIGHT = 700
border = 20
play_zone = ((345, 685),(130,570))

def DotPlacements(spacing):
    spacing = spacing

    width0_placement = int(play_zone[0][0]/spacing) + 2
    height0_placement = int(play_zone[1][0]/spacing) + 2
    width1_placement = int(play_zone[0][1]/spacing) - 2
    height1_placement = int(play_zone[1][1]/spacing) -2

    pos_list = []
    for x in range (width0_placement,width1_placement):
        for y in range (height0_placement, height1_placement):
            if (x%2 == y%2):
                pos_list.append((x*spacing,y*spacing))

    return pos_list
dot_placements = DotPlacements(30)

# INITIALISATIONS - pas toucher
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect the dots")
clock = pygame.time.Clock()

# Visuels text & bg
index_font_1 = pygame.font.Font ('font/Pixeltype.ttf', 50)
bgImage = pygame.image.load('graphics/draftbg1.png')

# Placer player au centre de la zone de jeu
player_pos_x = (play_zone[0][1]-play_zone[0][0])/2
player_pos_y = (play_zone[1][1]-play_zone[1][0])/2

# initialisation du nombre de dots 
STARTINGNBOFDOTS = 3
numberOfDots = STARTINGNBOFDOTS

class Dot(pygame.sprite.Sprite):

    def __init__(self, index):
        super().__init__()
        self.image =  pygame.image.load('graphics/dot.png').convert_alpha()
        self.coord = choice(dot_placements)
        dot_placements.remove(self.coord)
        self.coord = (self.coord[0] + randint (-8,8), self.coord[1] + randint (-8,8))
        self.rect = self.image.get_rect(topleft = (self.coord[0], self.coord[1])) 
        self.index = index
        self.collision_flag = False
        self.timer = 0
        self.pos = (self.coord[0], 800)
        self.pos_index = (self.coord[0], 800)

    def IndexDisplay(self):

        if (self.collision_flag == True and self.timer < 6):
            self.dot_index = pygame.transform.rotozoom(self.dot_index, 0, 1.001)
        elif (self.collision_flag == True and self.timer < 6):
            self.dot_index = pygame.transform.rotozoom(self.dot_index, 0, 0.999)
        else:
            self.dot_index = index_font_1.render(f'{self.index+1}', False, (0,0,0))
        self.dot_index_rect = self.dot_index.get_rect(bottomleft = (self.coord[0], self.coord[1]))
        self.pos_index = (self.dot_index_rect[0], self.pos_index[1]+(self.dot_index_rect[1]- self.pos_index[1])*.15) #tweening
        screen.blit(self.dot_index, self.pos_index)

    def CollisionFlag(self):
        if self.collision_flag == True:
            self.timer += 1
        
        if self.timer >= 100 :
            self.collision_flag = False
            self.timer = 0

    def DotDisplay(self):
        self.pos = (self.coord[0], self.pos[1]+(self.coord[1]- self.pos[1])*.15) #tweening
        screen.blit(self.image, self.pos)

    def update(self):
        self.DotDisplay()
        self.IndexDisplay()
        self.CollisionFlag()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = (WIDTH/2,HEIGHT/2))
        self.speed = 2.5
        self.position = pygame.math.Vector2(self.rect.center)

    def playerMovement(self):
        player_pos_x = self.position.x 
        player_pos_y = self.position.y

        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        
        if keys[pygame.K_UP] and self.rect.top > play_zone[1][0]:
            move_y = -self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < play_zone[1][1]:
            move_y = self.speed
        if keys[pygame.K_LEFT] and self.rect.left > play_zone[0][0]:
            move_x = -self.speed
        if keys[pygame.K_RIGHT] and self.rect.left < play_zone[0][1]:
            move_x = self.speed

        # Adjust diagonal movement speed by a smaller factor
        if move_x != 0 and move_y != 0:
            diagonal_factor = 0.75  # Adjust this factor as needed
            move_x *= diagonal_factor
            move_y *= diagonal_factor

        # Update the position using floats for precision
        self.position.x += move_x
        self.position.y += move_y

        # Update the rect position from the float position
        self.rect.center = (int(self.position.x), int(self.position.y))

    def update(self):
        self.playerMovement()

class Line(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/line.png').convert_alpha()
        self.rect = self.image.get_rect(center = (player.sprite.rect.x, player.sprite.rect.y))

    def LineDisplay(self):
        screen.blit(self.image, self.rect)


dots_reached = []
def CollisionIndex():
    if player.sprite and dotGroup:
        sprites_collision = pygame.sprite.spritecollide(player.sprite, dotGroup, False)
        if sprites_collision:
            dot_index = sprites_collision[0].index
            if dot_index not in dots_reached:
                sprites_collision[0].collision_flag = True
                dots_reached.append(dot_index)
        return dots_reached

def LevelOneCheck():
    completion_checklist = []
    for i in range(numberOfDots):
        if i not in completion_checklist:
            completion_checklist.append(i)
    if dots_reached == completion_checklist:
        return True
    return False

#Intialisation des instances player, line et dots:
def SetUp(howmanydots):
    global player
    global lineGroup
    global dotGroup

    player = pygame.sprite.GroupSingle()
    player.add(Player())

    dotGroup = pygame.sprite.Group()
    for i in range(howmanydots):
        dotGroup.add(Dot(i))    

    lineGroup = pygame.sprite.Group()

def Clear():
    player.empty()
    lineGroup.empty()
    dotGroup.empty()
    dots_reached.clear()



####################################################################################

#écran tuto

SetUp(numberOfDots)

while True:
    screen.blit(bgImage,(0,0))
    # screen.blit(player.image, player.rect)

    for i in dotGroup:
        i.update()

    CollisionIndex()

    if player.sprite and (player.sprite.position.x != player_pos_x or player.sprite.position.y != player_pos_y):
        lineGroup.add(Line())
    for i in lineGroup:
        i.LineDisplay()

    for i in range(len(dots_reached)):
        if dots_reached[i] != i: #ECHEC
            numberOfDots = STARTINGNBOFDOTS
            time.sleep(0.3)
            Clear()
            SetUp(numberOfDots)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # opposite to pygame.init()
            exit()

    if not LevelOneCheck():
        player.draw(screen)
        player.update()

    else: 
        time.sleep(0.3)
        Clear()
        numberOfDots +=1
        SetUp(numberOfDots)

    pygame.display.update()
    clock.tick(60)
