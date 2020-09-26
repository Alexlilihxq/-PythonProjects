# -*- coding: utf-8 -*-
"""
Created on 2020.09.20
@author: Alexlilihxq
"""
import pygame
from pygame.locals import *
from sys import exit
from config import *
from gameRole import *
from resource import *

BACKGROUND_IMAGE_HEIGHT = 800

class ScreenInfo:
    """用于展示score，bomb_num等信息"""
    def __init__(self, bomb_surface, plane_surface):
        self.score = 0
        self.bomb_surface = bomb_surface
        self.plane_surface = plane_surface
        self.gift_score = 0

    def addScore(self, score):
        self.score += score
        self.gift_score += score

    def getScore(self, score):
        return  self.score

    def shouldCreateGift(self):
        if self.gift_score > 20000:
            self.gift_score -= 20000
            return True
        return False

    def displayInfo(self, screen, game_over, bomb_num, plane_life):
        def dispalyScore(screen, score):
            score_font = pygame.font.Font(None, 36)     # 分数字体
            score_text = score_font.render(str(score), True, (128, 128, 128))
            text_rect = score_text.get_rect()
            text_rect.topleft = [SCREEN_WIDTH//2 - 35, 10]
            screen.blit(score_text, text_rect)
        dispalyScore(screen, self.score)

        if not game_over:
            bomb_rect = self.bombs_surface.get_rect()
            bomb_rect.topleft = [10, 0]
            screen.blit(self.bomb_surface, bomb_rect)

            bomb_font = pygame.font.Font(None, 36)
            bomb_text = bomb_font.render(" : " + str(bomb_num), True, (128, 128, 128))
            text_rext = bomb_text.get_rect()
            text_rext.topleft = [30, 10]
            screen.blit(bomb_text, text_rext)

            for i in range(plane_life):
                plane_rect = self.plane_surface.get_rect()
                plane_rect.topleft = [SCREEN_WIDTH - 120 + (i * 40), 0]
                screen.blit(self.plane_surface, plane_rect)


class Game:
    def __init__(self, caption, hero, screen_info):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        pygame.display.set_caption(caption)
        self.hero = hero
        self.clock = pygame.time.Clock()
        self.screen_info = screen_info
        self.ticks = 0
        self.pause = False
        self.background_y = SCREEN_HEIGHT - background.get_height()
















