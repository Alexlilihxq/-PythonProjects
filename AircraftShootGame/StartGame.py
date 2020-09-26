# -*- coding: utf-8 -*-
"""
Created on 2020.09.20
@author: Alexlilihxq
"""
import pygame
from pygame.locals import *
from sys import exit
from Config import *
from GameRole import *
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

    def getScore(self):
        return self.score

    def shouldCreateGift(self):
        if self.gift_score > 20000:
            self.gift_score -= 20000
            return True
        return False

    def displayInfo(self, screen, game_over, bomb_num, plane_life):
        def dispalyScore(screen, score):
            score_font = pygame.font.Font(None, 36)  # 分数字体
            score_text = score_font.render(str(score), True, (128, 128, 128))
            text_rect = score_text.get_rect()
            text_rect.topleft = [SCREEN_WIDTH // 2 - 35, 10]
            screen.blit(score_text, text_rect)

        dispalyScore(screen, self.score)

        if not game_over:
            bomb_rect = self.bomb_surface.get_rect()
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
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(caption)
        self.hero = hero
        self.clock = pygame.time.Clock()
        self.screen_info = screen_info
        self.ticks = 0
        self.pause = False
        self.background_y = SCREEN_HEIGHT - background.get_height()

    # 符合条件时create a new enemy
    def createEnemy(self, enemy_groups, ticks, score):
        # limit enemy2 and enemy3 numbers
        def getEnemyIndex(enemy_groups, enemy_range):
            index = randint(0, enemy_range)
            if index == 2:
                if len(enemy_groups[index].group) > 0:
                    index = 0
            elif index == 1:
                if len(enemy_groups[index].group) > 2:
                    index = 0
            return index

        if ticks % CREATE_CYCLE == 0:
            if score < 10000:
                enemy_range = 0
            elif score < 20000:
                enemy_range = 1
            else:
                enemy_range = 2

            index = getEnemyIndex(enemy_groups, enemy_range)
            enemy_groups[index].createEnemy()

    # 符合条件时create a new gift
    def createGift(self, gift_groups, ticks, Screen_info):
        if ticks % CREATE_CYCLE == 0 and Screen_info.shouldCreateGift():
            score = Screen_info.getScore()
            if score < 20000:
                gift_range = 0
            elif score < 40000:
                gift_range = 1
            else:
                gift_range = 1

            gift_size = 0
            for group in gift_group:
                gift_size += len(group.group)
            if gift_size == 0:
                if self.hero.bomb_num >= 3:
                    index = randint(1, gift_range)
                else:
                    index = randint(0, gift_range)
                gift_groups[index].createGift()

    def play(self, enemy_groups, gift_groups):
        def updateBackground(screen, image_height, current_y):
            if current_y <= 0:
                screen.blit(background, (0, 0), (0, -current_y, SCREEN_WIDTH, SCREEN_HEIGHT))
            elif current_y < SCREEN_HEIGHT:
                screen.blit(background, (0, 0), (0, image_height - current_y, SCREEN_WIDTH, current_y))
                screen.blit(background, (0, current_y), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - current_y))

        def checkBulletCollide(enemy_group, bullets_group, screen, ticks):
            score = 0
            for group in enemy_group:
                for bullet_group in bullets_group:
                    score += group.checkBulletCollide(bullet_group, screen, ticks)
            return score

        def checkHeroCollide(hero, enemy_group):
            collide = False
            for group in enemy_group:
                if group.checkHeroCollide(hero):
                    collide = True
                    break
            return collide

        self.clock.tick(FRAME_RATE)
        if self.background_y == SCREEN_HEIGHT:
            self.backrgound_y = SCREEN_HEIGHT - background.get_height()
        updateBackground(self.screen, background.get_height(), self.background_y)
        self.background_y += 1

        if self.ticks >= FRAME_RATE:
            self.ticks = 0

        self.hero.play()

        self.createEnemy(enemy_groups, self.ticks, self.screen_info.getScore())
        self.createGift(gift_groups, self.ticks, self.screen_info)

        self.screen_info.addScore(
            checkBulletCollide(enemy_groups, self.hero.weapon_groups, self.screen, self.ticks))

        if checkHeroCollide(self.hero, enemy_groups):
            if self.hero.isHeroCrash():
                game_over_sound.play()

        for gift_group in gift_groups:
            gift_group.checkHeroCollide(self.hero)

        for weapon_group in self.hero.weapon_groups:
            weapon_group.draw(self.screen)

        for enemy_group in enemy_groups:
            enemy_group.update()
            enemy_group.draw(self.screen)

        for gift_group in gift_groups:
            gift_group.update()
            gift_group.draw(self.screen)

        self.screen.blit(self.hero.image, self.hero.rect)
        self.ticks += 1

        self.screen_info.displayInfo(self.screen, 0, self.hero.bomb_num, self.hero.life)

    def isGameOver(self):
        if self.hero.down_index >= len(self.hero.down_surface):
            if self.hero.life <= 0:
                return 1
            else:
                self.hero.restart()
        return 0

    def showGameOver(self):
        self.screen.blit(gameover, (0, 0))
        self.screen_info.displayInfo(self.screen, 1, self.hero.bomb_num, self.hero.life)

    def setPause(self):
        self.pause = not self.pause

    def isPause(self):
        return self.pause


offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

pygame.init()       # 初始化

(background, gameover, game_over_sound, bomb_surface, plane_surface) = initGame()   # 变量初始化
screen_info = ScreenInfo(bomb_surface, plane_surface)               # 展示游戏初始信息
myGame = Game('Air Craft Shooter!', initHero(), screen_info)        # 开始游戏，实例化初始英雄， 屏幕
enemy_groups = initEnemyGroups()                                    # 实例初始化敌机精灵组
gift_groups = initGiftGroups()                                      # 实例初始化道具精灵组

while True:
    if myGame.isGameOver():
        myGame.showGameOver()
    elif not myGame.isPause():
        myGame.play(enemy_groups, gift_groups)

    pygame.display.update()                                         # 更新屏幕

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                               # 退出游戏
            pygame.quit()
            exit()
        # get keyboard input
        if event.type == pygame.KEYDOWN:                            # 按下键盘时
            if event.key in offset:                                 # 移动
                offset[event.key] = 3
            elif event.key == pygame.K_SPACE:                       # 空格使用Bomb
                myGame.hero.useBomb()
            # press z to pause or resume game
            elif event.key == pygame.K_z:                           # Z键暂停
                myGame.setPause()
        elif event.type == pygame.KEYUP:                            # 松开键盘时
            if event.key in offset:
                offset[event.key] = 0

    if not myGame.hero.is_hit:
        myGame.hero.move(offset)
