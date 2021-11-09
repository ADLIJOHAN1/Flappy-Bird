import pygame
import sys
import random

#Create pipe
def pipe_create():
    pipe_bottom=pipe_img.get_rect(midtop=(288,pipe_pos()))
    pipe_top=pipe_img.get_rect(midbottom=(288,pipe_pos()-180))
    return pipe_bottom,pipe_top

#Move pipe
def pipe_move():
    global plist
    for pipe in plist:
        pipe.centerx -=5
    return plist

#Draw pipe
def pipe_draw():
    global plist
    for pipe in plist:
        if pipe.bottom >=510:
            screen.blit(pipe_img,pipe)
        else:
            pipe_flip=pygame.transform.flip(pipe_img,False,True)
            screen.blit(pipe_flip,pipe)
    
#Pipe position
def pipe_pos():
    lst=[255,300,355]
    pipe_y=random.choice(lst)
    return pipe_y

#Check for collisions:
def collision_check(plist):
    global bird_rect
    for pipe in plist:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 490:
        return False
    return True

#Adding rotation
def bird_rotate(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_move*4,1)
    return new_bird

#Bird animation
def animated_bird():
    new_bird=frames[index]
    new_bird_rect=new_bird.get_rect(center=(50,bird_rect.centery))
    return new_bird,new_bird_rect

#Score text
def score_display(game_state):
    if game_state == 'main_game':
        score_img=font_game.render(str(int(score)),True,(255,255,255))
        score_rect=score_img.get_rect(center=(144,50))
        screen.blit(score_img,score_rect)
    else:
        score_img=font_game.render(f'Score:  {int(score)}',True,(255,255,255))
        score_rect=score_img.get_rect(center=(144,50))
        screen.blit(score_img,score_rect)

        highscore_img=font_game.render(f'Highscore: {int(highscore)}',True,(255,255,255))
        highscore_rect=highscore_img.get_rect(center=(144,400))
        screen.blit(highscore_img,highscore_rect)

#Update scores
def score_update(score,highscore):
    if score>highscore:
        highscore=score
    return highscore

pygame.init()

#Window
screen=pygame.display.set_mode((288,510))
clock=pygame.time.Clock()

#Background
bg=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/background-day.png").convert()

#Floor
floor1=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/base.png").convert()
floor2=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/base.png").convert()
floor1_pos=0
floor2_pos=288

#Score font
font_game=pygame.font.SysFont("Times",30,"bold")

#Variables
force=0.125
bird_move=0
active = True
score=0
highscore=0

#Bird
bird_midflap=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/yellowbird-midflap.png").convert()
bird_downflap=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/yellowbird-downflap.png").convert()
bird_upflap=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/yellowbird-upflap.png").convert()
index=0
frames=[bird_downflap,bird_midflap,bird_upflap]
bird=frames[index]
bird_rect=bird.get_rect(center=(50,245))
flap=pygame.USEREVENT +1
pygame.time.set_timer(flap,200)

#Pipe
pipe_img=pygame.image.load("/Users/adlijohan/Desktop/Flappy bird/sprites/pipe-green.png").convert()
plist=[]
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_move=0
                bird_move-=6
            if event.key == pygame.K_SPACE and active == False:
                plist.clear()
                bird_rect.center = (50,245)
                score=0
        if event.type == spawnpipe:
            plist.extend(pipe_create())
        if event.type == flap:
            if index < 2:
                index+=1
            else:
                index=0
            bird,bird_rect=animated_bird()

    #Floor movement
    floor1_pos-=1
    floor2_pos-=1
    if floor1_pos == -288:
        floor1_pos=0
    if floor2_pos == 0:
        floor2_pos=288
    
    #Display bg
    screen.blit(bg,(0,0))

    #Bird movement
    bird_move+=force
    bird_rect.centery += bird_move
    bird_rotated = bird_rotate(bird)
    if active:
    #Displaying bird
        screen.blit(bird_rotated,bird_rect)

        #Pipe movement
        plist=pipe_move()
        pipe_draw()
        score+=0.01
        score_display('main_game')
    
    else:
        score_display('game_over')
    highscore=score_update(score,highscore)
    #Displaying floor
    screen.blit(floor1,(floor1_pos,440))
    screen.blit(floor2,(floor2_pos,440))

    active=collision_check(plist)

    pygame.display.update()
    clock.tick(60)