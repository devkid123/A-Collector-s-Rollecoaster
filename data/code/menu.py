import pygame
import sys

import data.code.normal as n
import data.code.cutscene as c
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

WINDOW_SIZE = (pygame.display.Info().current_w,pygame.display.Info().current_h)
window = pygame.display.set_mode((WINDOW_SIZE))
display = pygame.Surface((300,200))
pygame.display.set_caption("A Collector's Rollercoaster")

normal_font = pygame.font.Font('data/font/BmAztecA12-5qv.ttf',48)
#m_font = pygame.font.Font('data/font/BmAztecA12-5qv.ttf',60)
big_font = pygame.font.Font('data/font/ThaleahFat.ttf',120)

background = pygame.image.load('data/images/menu_background.png').convert()


button = pygame.transform.scale(pygame.image.load('data/images/button.png'),(256,72))
button_h = pygame.transform.scale(pygame.image.load('data/images/button_highlighted.png'),(256,72))
title = pygame.transform.scale(pygame.image.load('data/images/title.png'),(1024,512))


def credits():
    title = big_font.render("CREDITS",False,(255,255,255))
    programmer = normal_font.render("Programmer: DevKid",False,(255,255,255))
    art = normal_font.render("Assets: DevKid",False,(255,255,255))
    sfx = normal_font.render("Sound Designer: Wylie Marvici",False,(255,255,255))
    composer = normal_font.render("Music Composer: Riley Dodges",False,(255,255,255))
    flag = True
    while flag:
        window.fill((50,50,50))

        window.blit(title,(WINDOW_SIZE[0]/2-title.get_width()/2,10))

        window.blit(programmer,(2,150))
        window.blit(art,(2,230))
        window.blit(sfx,(2,320))
        window.blit(composer,(2,400))


        for event in pygame.event.get():
            if event.type == QUIT:
                flag = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    flag = False

        pygame.display.update()
        clock.tick(fps)

def fade_in():
    display.fill((0,0,0))
    for alpha in range(0, 300):
        display.set_alpha(alpha)
        window.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        pygame.time.delay(5)

def main_menu():
    pygame.mixer.music.load('data/audio/main_menu.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    background.set_alpha(10)

    play = normal_font.render("PLAY",False,(255,255,255))
    quit = normal_font.render("QUIT",False,(255,255,255))
    credit = normal_font.render("CREDITS",False,(255,255,255))

    play_rect = pygame.Rect(WINDOW_SIZE[0]/2-play.get_width()/2,323,play.get_width(),play.get_height())
    quit_rect = pygame.Rect(WINDOW_SIZE[0]/2-quit.get_width()/2,448,quit.get_width(),quit.get_height())
    credit_rect = pygame.Rect(WINDOW_SIZE[0]/2-credit.get_width()/2,573,credit.get_width(),credit.get_height())

    button1_rect = pygame.Rect(WINDOW_SIZE[0]/2-button.get_width()/2,310,button.get_width(),button.get_height())
    button2_rect = pygame.Rect(button1_rect.x,435,button.get_width(),button.get_height())
    button3_rect = pygame.Rect(button1_rect.x,560,button.get_width(),button.get_height())

    counter = 10
    flag = True
    while flag:
        window.blit(pygame.transform.scale(background,WINDOW_SIZE),(0,0))

        counter += 1
        background.set_alpha(counter)
        if counter == 100:
            background.set_alpha(100)

        mx,my = pygame.mouse.get_pos()

        window.blit(title,((WINDOW_SIZE[0]/2-title.get_width()/2)+100,10))
        
        if button1_rect.collidepoint((mx,my)):
            window.blit(button_h,(button1_rect.x,button1_rect.y))
        else:
            window.blit(button,(button1_rect.x,button1_rect.y))
        
        if button2_rect.collidepoint((mx,my)):
            window.blit(button_h,(button2_rect.x,button2_rect.y))
        else:
            window.blit(button,(button2_rect.x,button2_rect.y))

        if button3_rect.collidepoint((mx,my)):
            window.blit(button_h,(button3_rect.x,button3_rect.y))
        else:
            window.blit(button,(button3_rect.x,button3_rect.y))

        window.blit(play,(play_rect.x,play_rect.y))
        window.blit(quit,(quit_rect.x,quit_rect.y))
        window.blit(credit,(credit_rect.x,credit_rect.y))

        for event in pygame.event.get():
            if event.type == QUIT:
                flag = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button1_rect.collidepoint((mx,my)):
                        pygame.mixer.music.fadeout(1000)
                        fade_in()
                        c.cutscene_1()
                    if button2_rect.collidepoint((mx,my)):
                        pygame.quit()
                        sys.exit()
                    if button3_rect.collidepoint((mx,my)):
                        credits()

        #screen.blit(pygame.transform.scale(window,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(fps)