import pygame
import os
import math
import random
from sys import exit
import spritesheet

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
S_WIDTH = 1200
S_HEIGHT = 500

screen = pygame.display.set_mode((S_WIDTH,S_HEIGHT),vsync=1)
pygame.display.set_caption('ROYVENTURE')
clock = pygame.time.Clock()

text_font = pygame.font.Font(os.path.join(BASE_DIR, 'Pixeltype.ttf') , 60)
text_surface = text_font.render('ROYVENTURE',  True, 'purple')
button_font = pygame.font.Font(os.path.join(BASE_DIR, 'Pixeltype.ttf'), 30)
game_font = pygame.font.Font(os.path.join(BASE_DIR, 'Pixeltype.ttf') , 60)
game_surface = game_font.render('ROYVENTURE', True, 'purple')
game_over_text = text_font.render('GAME OVER', True, 'purple')
roy_overlay = pygame.Surface((1200, 500))
roy_overlay.set_alpha(160)
roy_overlay.fill('black')


MENU = 'menu'
PLAYING = 'playing'
QUIT = 'quit'
ROY_STATE = MENU
GAME_OVER = 'game_over'


bg_image = pygame.image.load(os.path.join(BASE_DIR,'graphics','elements','background_default.png')).convert()
bg_surface = pygame.transform.scale(bg_image,(1200, 500))
bg_surface_xpos = 0
bg_width = bg_surface.get_width()

scroll = 0

tiles = math.ceil(S_WIDTH / bg_width) + 1

tileset = pygame.image.load(os.path.join(BASE_DIR, 'graphics', 'elements', 'tilesetgrass.png')).convert()
grass_part = tileset.subsurface(pygame.Rect(286, 96, 34, 26))
grass_size = pygame.transform.scale_by(grass_part, 4.5)
grass_width = grass_size.get_width()

grass_x = 0
grass_speed = 6
ground_y = 410       
jump_strength = -20
vertical_velocity = 0
gravity = 1.2
is_jumping = False
min_gap = 300   
max_gap = 800



cac = pygame.image.load(os.path.join(BASE_DIR, 'graphics' , 'elements' , 'Cactus_Sprite_Sheet.png' )).convert_alpha()
cac_part = cac.subsurface(pygame.Rect(338, 20, 30, 27))
cac_size = pygame.transform.scale_by(cac_part, 3)
cac_mask = pygame.mask.from_surface(cac_size) 
cac_rect = cac_size.get_rect(midbottom=(1300, ground_y))
cac_x = 1200
cac_speed = 6

roy_shit = spritesheet.SpriteSheet(
    pygame.image.load(os.path.join(BASE_DIR,'graphics', 'characters', 'sheets', 'character_doux.png')).convert_alpha())



play_button = pygame.Rect(0, 0, 200, 60)
play_button.center = (950, 220)

restart_button = pygame.Rect(0, 0, 200, 60)
restart_button.center = (600, 300)

quit_button = pygame.Rect(0, 0, 200, 60)
quit_button.center = (600, 370)

IDLE, RUN, JUMP = 0, 1, 2
roy_frames = []
shit_index = 0
for how_many in [4, 6, 3]:
    row = []
    for _ in range(how_many):
        row.append(roy_shit.get_image(shit_index, 24, 24, 3, 'BLACK'))
        shit_index += 1
    roy_frames.append(row)    

roy_rect = roy_frames[IDLE][0].get_rect(midbottom=(100, ground_y))
action = IDLE
frame = 0
frame_delay = 70
last_frame_time = pygame.time.get_ticks()

def draw_button(text, rect):
    pygame.draw.rect(screen, 'purple', rect, border_radius=10)
    label = button_font.render(text, True, 'pink' )
    screen.blit(label, label.get_rect(center=rect.center))
    

def sound_effect(filename, volume):
    sound = pygame.mixer.Sound(os.path.join(BASE_DIR, 'music', filename))
    sound.play()
    sound.set_volume(volume)

def bg_sound(filename, volume):
    pygame.mixer.music.load(os.path.join(BASE_DIR, 'music', filename))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)

def update_animation():
    global frame, last_frame_time
    current_tick = pygame.time.get_ticks()
    if current_tick - last_frame_time >= frame_delay:
        last_frame_time = current_tick
        frame += 1
        if frame >= len(roy_frames[action]):
            frame = 0
            
def music_player(filename, volume, times):
    pygame.mixer.music.load(os.path.join(BASE_DIR, 'music', filename))
    pygame.mixer.music.play(times)
    pygame.mixer.music.set_volume(volume)

def reset_game():
    global vertical_velocity, is_jumping, action
    roy_rect.midbottom = (100, ground_y)
    vertical_velocity = 0
    action = IDLE
    is_jumping = False
    reset_cac()

    
def reset_cac():
    global cac_x
    cac_x = 1200
    
    



#main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                vertical_velocity = jump_strength
                is_jumping = True
                sound_effect('jump.WAV', 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if ROY_STATE == MENU and play_button.collidepoint(event.pos):
                ROY_STATE = PLAYING
                bg_sound('bgm.ogg', 1)
            if ROY_STATE == GAME_OVER and restart_button.collidepoint(event.pos):
                reset_game()
                ROY_STATE = PLAYING
                bg_sound('bgm.ogg', 1)

    for i in range(0, tiles):
        screen.blit(bg_surface, ((i * bg_width + scroll), 0))

   
    cac_rect.x = cac_x
    cac_rect.y = 323

    screen.blit(cac_size, cac_rect)
    if ROY_STATE == GAME_OVER:
        draw_button('RESTART', restart_button)

            
                    

    if ROY_STATE == MENU:
        screen.blit(game_surface,(900, 50)) 
        action = IDLE
        reset_game()
        draw_button('START', play_button)
        update_animation()

    if ROY_STATE == PLAYING:
        vertical_velocity += gravity
        roy_rect.y += vertical_velocity
        if roy_rect.bottom >= ground_y:
            roy_rect.bottom = ground_y
            vertical_velocity = 0
            is_jumping = False

        grass_x -= grass_speed
        if grass_x <= -grass_width:
            grass_x += grass_width   

        if abs(scroll) > bg_width:
            scroll = 0
        scroll -= 5

        cac_x -= cac_speed
        if cac_x < -cac_size.get_width():
            cac_x = S_WIDTH + random.randint(min_gap, max_gap)

        new_action = JUMP if is_jumping else RUN   
        if new_action != action:
            action = new_action
            frame = 0
        update_animation()  
        
    roy_mask = pygame.mask.from_surface(roy_frames[action][frame])
    offset = (cac_rect.x - roy_rect.x, cac_rect.y - roy_rect.y)
    if roy_mask.overlap(cac_mask, offset):
        ROY_STATE = GAME_OVER
        print("COLLISION")
        pygame.draw.rect(screen, 'red', roy_rect, 2)
        pygame.draw.rect(screen, 'blue', cac_rect, 2)

    
    
    for x in range(0, 1200 + grass_width, grass_width):
        screen.blit(grass_size, (x + grass_x, 400))

    screen.blit(roy_frames[action][frame], roy_rect)
    print(offset)
    
   

    pygame.display.update()
    clock.tick(60)  