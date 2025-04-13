import pygame
import sys
import random
import time
import data.code.normal as n
import data.code.menu as m

clock = pygame.time.Clock()
fps = 60

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.mixer.music.stop()

pygame.display.set_caption("A Collector's Rollercoaster")

width,height = (pygame.display.Info().current_w, pygame.display.Info().current_h)

screen = pygame.display.set_mode((width,height),0,32) 
display = pygame.Surface((300,200))

font = pygame.font.Font('data/font/Peepo.ttf',18)
font_2 = pygame.font.Font('data/font/BmAztecA12-5qv.ttf',18)

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

    screen.blit(pygame.transform.scale(display,(width,height)),(0,0))

def display_dialogue(dialogues,speaker,gender,right,left):
    img = pygame.transform.scale(pygame.image.load('data/images/dialogues/dialogue_box.png'), (255, 99)).convert_alpha()
    counter = 0
    if speaker != None:
        speaker_img = pygame.transform.scale(pygame.image.load(f'data/images/dialogues/{speaker}.png'), (64, 64)).convert_alpha()
        if right:
            speaker_x, speaker_y = 200, 170
        if left:
            speaker_x, speaker_y = 5, 170
        x, y = 10, 100
    else:
        x, y = 20, 100
        
    text_rect = pygame.Rect(x + 10, y + 20, img.get_width() - 20, img.get_height() - 20)

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

            screen.blit(pygame.transform.scale(display, (width, height)), (0, 0))

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

def fade_in():
    display.fill((0,0,0))
    for alpha in range(0, 300):
        display.set_alpha(alpha)
        screen.blit(pygame.transform.scale(display,(width,height)),(0,0))
        pygame.display.update()
        pygame.time.delay(5)

def cutscene_1():
    news_background = pygame.image.load('data/images/news_background.png')
    cookie = pygame.transform.scale(pygame.image.load('data/images/sceleratus cookie.png'),(64,64))
    font = pygame.font.Font('data/font/ThaleahFat.ttf',15)
    title = font.render("SCELERATUS'S COOKIE IS BACK!",False,(0,0,0))
    news_background.set_alpha(10)
    counter = 0

    dialogues = [{"text": "Hmm, wonder if I can trade this"}]

    while True:
        counter += 1
        #fade_in(window,screen)
        display.blit(news_background,(0,0))

        display.blit(cookie,(215,(300/2-cookie.get_height()/2)-60))
        display.blit(title,(1,30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if counter == 300:
            news_background.set_alpha(100)
            display_dialogue(dialogues,None,'boy',True,False)    
            fade_in()
            n.level_1()

        screen.blit(pygame.transform.scale(display,(width,height)),(0,0))
        pygame.display.update()
        clock.tick(fps)

moving_right = False
moving_left = False
moving_front = False
moving_back = False

true_scroll = [1248,128]
air_timer = 0

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


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

animation_database = {}

animation_database['idle'] = load_animation('data/images/bosses/grimshade/idle',[7,7,7,7,7])
animation_database['attack'] = load_animation('data/images/bosses/grimshade/attack',[40,7,7,7,7,7,7,7,7,7,7,3000])
animation_database['stop'] = load_animation('data/images/bosses/grimshade/attack',[40,7,7,7,7,7,7,3000])
animation_database['idler'] = load_animation('data/images/player/idler',[7,7,7,7,7])
animation_database['beem'] = load_animation('data/images/beem/beem',[7,7,7,7,7])
animation_database['stopb'] = load_animation('data/images/beem/stopb',[7,7,7])

jump_sound = pygame.mixer.Sound('data/audio/jump.wav')

game_map = load_map('data/maps/map1')

dirt_img = pygame.image.load('data/images/dirt.png')
gun_img = pygame.image.load('data/images/gun.png')

bg = pygame.image.load('data/images/boss_background.png')

vertical_momentum = 0

boss_action = 'idle'
boss_frame = 0
boss_flip = False

beem_action = 'beem'
beem_frame = 0
beem_flip = False

player_action = 'idler'
player_frame = 0
player_flip = False

boss_rect = pygame.Rect(200,60,128,128)
player_rect = pygame.Rect(37,160,32,32)
bullet_img = pygame.image.load('data/images/bullet.png')
bullet_rect = pygame.Rect(player_rect.x+20,player_rect.y+15,bullet_img.get_width(),bullet_img.get_height())
x_change = 0
y_change = 0
bullet_state = 'ready'
bullet_sound = pygame.mixer.Sound('data/audio/gun.wav')

def fire_bullet(x,y):
    global bullet_state

    bullet_state = 'fire'
    display.blit(bullet_img,(x,y))


def boss_fight_1():
    global beem_flip,beem_action,beem_frame,bullet_state,bullet_rect,bullet_img,player_rect,air_timer,vertical_momentum,boss_frame,boss_flip,boss_action,player_frame,player_flip,player_action,moving_right,moving_left

    pygame.mixer.music.load('data/audio/boss_fight.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    green_rect = pygame.Rect(300/2-150/2,20,150,8)
    red_rect = pygame.Rect(green_rect.x,green_rect.y,green_rect.width,green_rect.height)
    boss_health_bar = pygame.image.load('data/images/boss_health_bar.png')
    name = font_2.render("Grimshade",False,(0,0,0))

    game_map = load_map('data/maps/map2')

    beem_x = 1500
    beem_y = 1600

    attack = random.randint(100,500)
    stop = random.randint(100,500)
    c = 0
    c2 = 0
    att = True
    while True:
        display.blit(bg,(0,0))
    
        if boss_rect.colliderect(bullet_rect):
            green_rect.width -= 1

        pygame.draw.rect(display,(255,0,0),red_rect)
        pygame.draw.rect(display,(0,255,0),green_rect)
        display.blit(boss_health_bar,(green_rect.x-3,green_rect.y-3))
        display.blit(name,(300/2-name.get_width()/2,1))
             
        beem_frame += 1
        if beem_frame >= len(animation_database['beem']):
            beem_frame = 0
        beem_img_id = animation_database['beem'][beem_frame]
        beem_img = animation_frames[beem_img_id]
        display.blit(pygame.transform.scale(beem_img,(64,64)),(beem_x,beem_y))

        if att == True:
            c += 1
            if c == attack:
                c = attack
                boss_action,boss_frame = change_action(boss_action,boss_frame,'attack')
                #boss_frame += 1
                #if boss_frame >= len(animation_database['attack']):
                #    boss_frame = len(animation_database['attack'])

                if c2 != stop and c >= attack:
                    beem_action,beem_frame = change_action(beem_action,beem_frame,'attack')
                    beem_x,beem_y = 150,160
        
        c2 += 1
        if c2 == stop:
            att = False
            boss_action,boss_frame = change_action(boss_action,boss_frame,'stop')
            beem_action,beem_frame = change_action(beem_action,beem_frame,'stopb')
            att = True

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '2':
                    display.blit(dirt_img,(x*32,y*32))
                if tile == 'w':
                    rect = pygame.Rect(x*32,y*32,32,32)
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*32,y*32,32,32))

                x += 1
            y += 1

        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        player_rect,collision_types = move(player_rect,player_movement,tile_rects)

        if collision_types['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
            jump_count = 0
        else:
            air_timer += 1

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(player_img,(player_rect.x,player_rect.y))
        
        boss_frame += 1
        if boss_frame >= len(animation_database[boss_action]):
            boss_frame = 0
        boss_img_id = animation_database[boss_action][boss_frame]
        boss_img = animation_frames[boss_img_id]
        boss_rect.width = boss_img.get_width()-50
        display.blit(boss_img,(150,53))

        display.blit(gun_img,(player_rect.x+20,player_rect.y+15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                if event.key == K_UP or event.key == K_w:
                    jump_count += 1

                    if jump_count > 0 and jump_count < 3:
                        vertical_momentum = -6
                        jump_sound.play()
                    
                    if air_timer < 6:
                        vertical_momentum = -5
                        jump_sound.play()
                
                if event.key == K_SPACE:
                    if bullet_state == 'ready':
                        bullet_sound.play()
                        bullet_rect.x = player_rect.x+20
                        bullet_rect.y = player_rect.y+15
                        fire_bullet(bullet_rect.x,bullet_rect.y)

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
        
        if bullet_rect.x >= 300 or boss_rect.colliderect(bullet_rect):
            bullet_rect.x = player_rect.x+20
            bullet_rect.y = player_rect.y+15
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bullet_rect.x, bullet_rect.y)
            bullet_rect.x += 5

        screen.blit(pygame.transform.scale(display,(width,height)),(0,0))
        pygame.display.update()
        clock.tick(fps)