import pygame
import sys
import random
import time
import data.code.cutscene as c
clock = pygame.time.Clock()

fps = 60

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("A Collector's Rollercoaster")

WINDOW_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) 

display = pygame.Surface((350,250)) 

moving_right = False
moving_left = False
moving_front = False
moving_back = False

true_scroll = [1248,128]

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0,0,0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

font = pygame.font.Font('data/font/Peepo.ttf',18)
def render_textrect(string, font, rect, text_color):
    words = [word.split(' ') for word in string.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = rect.size

    lines = []
    for line in words:
        for word in line:
            if lines:
                if font.size(' '.join(lines[-1] + [word]))[0] <= max_width:
                    lines[-1].append(word)
                else:
                    lines.append([word])
            else:
                lines.append([word])

    y = rect.top
    for line in lines:
        text_surface = font.render(' '.join(line), True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (rect.left + max_width // 2, y)
        display.blit(text_surface, text_rect)
        y += font.size('Tg')[1]

    screen.blit(pygame.transform.scale(display,(WINDOW_SIZE)),(0,0))

def display_dialogue(dialogues,speaker,gender,right,left):
    img = pygame.transform.scale(pygame.image.load('data/images/dialogues/dialogue_box.png'), (300, 148)).convert_alpha()
    counter = 0
    if speaker != None:
        speaker_img = pygame.transform.scale(pygame.image.load(f'data/images/dialogues/{speaker}.png'), (64, 64)).convert_alpha()
        if right:
            speaker_x, speaker_y = 200, 100
        if left:
            speaker_x, speaker_y = 0, 110
        x, y = 57, 100
    else:
        x, y = 60, 100
        
    text_rect = pygame.Rect(x + 10, y + 30, img.get_width() - 20, img.get_height() - 20)

    dialogue_blip = pygame.mixer.Sound(f'data/audio/{gender}_dialogue_blip.ogg')
    dialogue_blip.set_volume(0.3)

    flag = True
    for dialogue in dialogues:
        text = dialogue['text']
        wait_time = 1400

        text_complete = False
        play_sound = False

        for i in range(len(text) + 2):
            display.blit(img, (x, y))
            if speaker != None:
                display.blit(speaker_img, (speaker_x, speaker_y))
            render_textrect(text[:i], font, text_rect, (0, 0, 0))
            pygame.display.update()
            time.sleep(0.03)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(pygame.transform.scale(display, (WINDOW_SIZE)), (0, 0))

            if i == len(text):
                text_complete = True
                flag = False
                break

            if not play_sound:
                dialogue_blip.play()
                play_sound = True

        if text_complete:
            dialogue_blip.stop()
            play_sound = False
            
        pygame.time.wait(wait_time)

animation_database = {}

animation_database['back'] = load_animation('data/images/player/back',[7,7,7,7,7])
animation_database['front'] = load_animation('data/images/player/front',[7,7,7,7,7])
animation_database['right'] = load_animation('data/images/player/right',[7,7,7,7,7])
animation_database['left'] = load_animation('data/images/player/left',[7,7,7,7,7])
animation_database['idle'] = load_animation('data/images/player/idle',[40,7,7,7,7,7,7,7])

game_map = load_map('data/maps/map1')

grass_img = pygame.image.load('data/images/grass.png')
paved_grass_h_img = pygame.image.load('data/images/paved_grass_h.png')
paved_grass_v_img = pygame.image.load('data/images/paved_grass_v.png')
corner_img = pygame.image.load('data/images/paved_grass_c.png')
corner2_img = pygame.image.load('data/images/paved_grass_c2.png')
house_img = pygame.image.load('data/images/house.png')
tree_img = pygame.image.load('data/images/tree.png')
tall_tree_img = pygame.image.load('data/images/tall_tree.png')
boss_img = pygame.image.load('data/images/grimshade.png')
cave_img = pygame.image.load('data/images/dealers base.png')

player_action = 'idle'
player_frame = 0
player_flip = False

player_rect = pygame.Rect(1248,128,32,32)

last_time = time.time()
pos = 0
dt = 0

def fade_in():
    display.fill((0,0,0))
    for alpha in range(0, 300):
        display.set_alpha(alpha)
        screen.blit(pygame.transform.scale(display,(WINDOW_SIZE)),(0,0))
        pygame.display.update()
        pygame.time.delay(5)

def level_1():
    global moving_right, moving_left, moving_front, moving_back, player_rect, player_action, player_frame, player_flip, game_map, last_time,dt,pos
    pygame.mixer.music.load('data/audio/chill_background.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    font = pygame.font.Font('data/font/ThaleahFat.ttf',18)
    text = font.render("Objective: Get to the Dealer's Base",False,(255,255,255))
    text_x, text_y = 40,180
    counter = 0

    dialogues1 = [{'text': "Hello I would like to make a deal for the cookie"}]
    dialogues2 = [{'text': "Kid, do you think that someone can make a deal with you"}]
    dialogues3 = [{'text': "Why do you think I have the Blast Proof Armor 3000 that Im wearing."},
                  {'text': "I only had to trade my Wubble Bubbles Gum 3.0, Belphador's Strand of Hair an-"}]
    dialogues4 = [{'text': "Yea yea kiddo I get it, now stop yapping."},
                  {'text': "If you want to enter this cave, You gotta fight me"}]
    dialogues5 = [{'text': "Thank god I got my Gun Blastor 4.0"}]

    while True:
        
        clock.tick(fps)

        if not (clock.get_fps() == 0):
            dt = fps/clock.get_fps()
        dt += 80
        last_time = time.time()

        display.fill((121, 229, 126))
        
        pos += 3 * dt

        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        
        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(grass_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == '2':
                    display.blit(paved_grass_h_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == '3':
                    display.blit(paved_grass_v_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == '4':
                    #rect = pygame.Rect(x*32,y*32,32,32)
                    display.blit(tree_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == '5':
                    display.blit(tall_tree_img,(x*32-scroll[0],y*32-scroll[1]-10))
                if tile == 'v':
                    display.blit(corner_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == 'c':
                    display.blit(corner2_img,(x*32-scroll[0],y*32-scroll[1]))
                if tile == 'n':
                    display.blit(paved_grass_v_img,(x*32-scroll[0],y*32-scroll[1]))
                    n_rect = pygame.Rect(x*32,y*32,32,32)

                if tile == 'C':
                    display.blit(cave_img,(x*32-scroll[0]-10,y*32-scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*32,y*32,32,32))
                x += 1
            y += 1
        
        display.blit(house_img,(1205-scroll[0],6-scroll[1]))
        
        boss_rect = pygame.Rect(2045,486,64,48)
        display.blit(boss_img,(boss_rect.x-scroll[0],boss_rect.y-scroll[1]))

        if n_rect.colliderect(player_rect):
            counter += 1

            if counter == 65:
                pygame.mixer.music.stop()
                display_dialogue(dialogues1,'alex','boy',False,True)
                display_dialogue(dialogues2,'grimshade','boy',False,True)
                display_dialogue(dialogues3,'alex','boy',False,True)
                display_dialogue(dialogues4,'grimshade','boy',False,True)
                display_dialogue(dialogues5,'alex','boy',False,True)
                fade_in()
                c.boss_fight_1()

        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        if moving_back == True:
            player_movement[1] -= 2
        if moving_front == True:
            player_movement[1] += 2

        if player_movement == [0,0]:
            player_action,player_frame = change_action(player_action,player_frame,'idle')
        if player_movement[0] > 0:
            player_action,player_frame = change_action(player_action,player_frame,'right')
        if player_movement[0] < 0:
            player_action,player_frame = change_action(player_action,player_frame,'left')
        if player_movement[1] > 0:
            player_action,player_frame = change_action(player_action,player_frame,'front')
        if player_movement[1] < 0:
            player_action,player_frame = change_action(player_action,player_frame,'back')

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT] or keys[K_d]:
            moving_right = True
        else:
            moving_right = False
        if keys[K_LEFT] or keys[K_a]:
            moving_left = True
        else:
            moving_left = False
        if keys[K_DOWN] or keys[K_s]:
            moving_front = True
        else:
            moving_front = False
        if keys[K_UP] or keys[K_w]:
            moving_back = True
        else:
            moving_back = False
        
        if keys[K_s] and keys[K_d]:
            moving_front = False
            moving_right = False
        
        if keys[K_s] and keys[K_a]:
            moving_front = False
            moving_left = False

        if keys[K_w] and keys[K_d]:
            moving_back = False
            moving_right = False
        
        if keys[K_w] and keys[K_a]:
            moving_back = False
            moving_left = False
        
        player_rect.x += player_movement[0]
        player_rect.y += player_movement[1]
        
        display.blit(text,(text_x,text_y))
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        #clock.tick(fps)
