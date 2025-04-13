import pygame
import sys
import random
import data.code.normal as n
import data.code.menu as m
import data.code.cutscene as c
clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("A Collector's Rollercoaster")

WINDOW_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) 
display = pygame.Surface((300,200))

n.level_1()
#m.main_menu()
#c.boss_fight_1()