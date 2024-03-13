import pygame
from player import *
from pygame import mixer

mixer.init()
pygame.init()

WIDTH = 1200
HEIGHT = 700

SIZE = (WIDTH, HEIGHT)
surface = pygame.display.set_mode(SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
FPS = 60

start_count = 3
previous_count_update = pygame.time.get_ticks()
round_finished = False
round_finished_cooldown = 2500

pygame.mixer.music.load("Lyd/MKchiptune.wav")
pygame.mixer.music.play(-1, 0.0, 5000)

block = "Bilder/shield.png"
KO = pygame.image.load("Bilder/KO.png").convert_alpha()

frames_c1 = ["Bilder/c1frame1.png", "Bilder/c1frame2.png", 
             "Bilder/c1frame3.png","Bilder/c1frame4.png", 
             "Bilder/c1frame5.png", "Bilder/c1frame6.png", 
             "Bilder/c1frameHB.png", "Bilder/c1frameProjectile.png", 
             "Bilder/c1frameThrowable.png", "Bilder/c1frameDead.png"]

frames_c2 = ["Bilder/c2frame1.png", "Bilder/c2frame2.png", 
             "Bilder/c2frame3.png","Bilder/c2frame4.png", 
             "Bilder/c2frame5.png", "Bilder/c2frame6.png", 
             "Bilder/c2frameHB.png","Bilder/c2frameProjectile.png", 
             "Bilder/c2frameThrowable.png", "Bilder/c2frameDead.png"]

t_font = pygame.font.Font("Font/PixelBook-Regular.ttf", 100)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) 
    surface.blit(img, (x, y))

background_image = pygame.image.load("Bilder/background2.png").convert_alpha()
def draw_bg():
    scaled_bg = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    surface.blit(scaled_bg,(0,0))

clock = pygame.time.Clock()

fighter_1 = Player(300, 310, frames_c1, "WASD", surface)
fighter_2 = Player(790, 310, frames_c2, "Arrows", surface)

run = True

while run:
    clock.tick(FPS)
    draw_bg()
    
    
    if start_count <= 0:
        fighter_1.actions(WIDTH, HEIGHT, fighter_2)
        fighter_2.actions(WIDTH, HEIGHT, fighter_1)
    else: 
        draw_text(str(start_count), t_font, RED, 580, HEIGHT / 3)
        if pygame.time.get_ticks() - previous_count_update >= 1000:
            start_count -= 1
            previous_count_update = pygame.time.get_ticks()

    fighter_1.healthbar(40, 40, block, 0, 180, 90)
    fighter_2.healthbar(760, 40, block, 1040, 860, 950)
    fighter_1.draw()
    fighter_2.draw()

    if round_finished == False:
        if fighter_1.health <= 0 or fighter_2.health <= 0:
            round_finished = True
            round_finished_time = pygame.time.get_ticks()
    else:
        surface.blit(KO, (400, 0))
        if pygame.time.get_ticks() - round_finished_cooldown > round_finished_time:
            round_finished = False
            start_count = 4
            fighter_1 = Player(300, 310, frames_c1, "WASD", surface)
            fighter_2 = Player(750, 310, frames_c2, "Arrows", surface)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    pygame.display.flip()

pygame.quit()