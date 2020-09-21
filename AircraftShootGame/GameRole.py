# -*- coding: utf-8 -*-
"""
Created on 2020.09.20
@author: Alexlilihxq
"""
import pygame
from random import randint
from enum import Enum
from Config import *


class GameGift(Enum):
    Bomb = 0
    PowerBullet = 1
    Laser = 2


class BulletType(Enum):
    OneWay = 1
    TwoWay = 2
    ThreeWay = 3


class EnemyType(Enum):
    EnemyType1 = 1
    EnemyType2 = 2
    EnemyType3 = 3


bullet_type = [BulletType.OneWay, BulletType.TwoWay, BulletType.ThreeWay]


class Weapon(pygame.sprite.Sprite):
    """武器精灵类"""
    def __init__(self, weapon_surface, weapon_init_pos, direction):
        super().__init__(self)
        self.image = weapon_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = weapon_init_pos     # 左上方坐标
        self.direction = direction

    def update(self):
        # direction[0]:x , direction[1]:y
        if self.direction[0] == 0:
            self.rect.y += self.direction[1]    # 纵向位置改变
            if self.direction[1] > 0:
                if self.rect.y > SCREEN_HEIGHT:
                    self.kill()
            else:
                if self.rect.y < 0:         # 此处有改动
                    self.kill()
        else:
            self.rect.x += self.direction[0]    # 横向位置改变
            if self.direction[0] > 0:
                if self.rect.x > SCREEN_WIDTH:
                    self.kill()
            else:
                if self.rect.x < 0:         # 此处有改动
                    self.kill()


class Enemy(pygame.sprite.Sprite):
    """敌机精灵类"""
    def __init__(self, enemy_surface, enemy_init_pos, direction, weapon_group):
        super().__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos  # 初始位置
        self.direction = direction
        self.down_index = 0
        self.damage = 0         # 坠毁标识
        self.is_down = 0        # 底端标识
        self.is_hit = 0         # 撞击标识
        self.ticks = 0          #
        self.weapon_group = weapon_group

    def update(self, enemy_surface, hit_surface=0):
        def shootWeapon(weapon_group, position, direction):
            weapon_group.shootWeapon(position, direction)

        # direction[0]:x , direction[1]:y
        should_kill = False      # 是否销毁精灵判断标识
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            should_kill = True
        if self.rect.y > SCREEN_HEIGHT or self.rect.y < 0:
            should_kill = True

        if should_kill:
            self.kill()
        else:
            if self.ticks >= ENEMY_SHOOT_CYCLE:
                self.ticks = 0

            if self.is_hit:
                self.is_hit -= 1
                self.image = hit_surface    # 撞击后将敌机图像切换成爆炸效果
            elif len(enemy_surface) >= 2:
                self.image = enemy_surface[self.ticks//(ENEMY_SHOOT_CYCLE//2)]      # 爆炸效果动画切换
            else:
                self.image = enemy_surface[0]

            self.ticks += 1
            if self.weapon_group is not None:
                if self.ticks % ENEMY_SHOOT_CYCLE == 0:
                    shootWeapon(self.weapon_group, [self.rect.centerx, self.image.get_height()], [0, ENEMY_SHOOT_SPEED])


class Gift(pygame.sprite.Sprite):
    """道具精灵类"""
    def __init__(self, gift_surface, gift_init_pos, speed):
        super().__init__(self)
        self.image = gift_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = gift_init_pos
        self.speed = speed

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Hero(pygame.sprite.Sprite):
    """英雄精灵类"""
    def __init__(self, hero_surface, hero_down_surface, hero_init_pos, weapon_groups, life):
        super().__init__(self)
        self.surface = hero_surface
        self.down_surface = hero_down_surface
        self.image = hero_surface[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.hero_init_pos = hero_init_pos
        self.weapon_groups = weapon_groups
        self.life = life
        self.reset()

    def reset(self):
        """英雄战机重置"""
        self.ticks = 0
        self.is_hit = 0
        self.down_index = 0
        self.bullet_type_index = 0
        self.bomb_num = 0
        self.use_bomb = 0
        self.immune_ticks = 0       # 重生免疫时间

    def moving(self, offset):
        """英雄移动方法，offset为事件"""
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]

        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

    def useBomb(self):
        if self.bomb_num:
            self.use_bomb = 1

    def getBomb(self):
        """获取Bomb数量"""
        return self.bomb_num

    def addGift(self, types):
        """道具强化"""
        if types == GameGift.Bomb:
            self.bomb_num += 1
        elif types == GameGift.PowerBullet:
            if self.bullet_type_index < len(bullet_type):
                self.bullet_type_index = self.bullet_type_index+1
            else:
                self.bullet_type_index = self.bullet_type_index
        # else: self.Laser_num += 1

    def HeroCrash(self):
        if self.immune_ticks <= 0 and not self.is_hit:
            self.is_hit = True
            self.life -= 1
            return 1
        else:
            return 0

    def restart(self):
        """英雄重生"""
        self.reset()
        self.immune_ticks = 180
        self.rect.topleft = self.hero_init_pos

    def play(self):
        """"""
        def getBulletPosition(rect, position_type):
            if position_type == 0:
                return [rect.centerx-3, rect.centery]
            elif position_type == 1:
                return [rect.x + 10, rect.centery]
            else:
                return [rect.x + rect.width - 20, rect.centery]

        def shootWeapon(types, rect, weapon_groups):
            weapon_index = 0
            weapon_dirction = [[0, -SHOOT_SPEED], [-SHOOT_SPEED, 0], [SHOOT_SPEED, 0]]
            if types == BulletType.OneWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
            elif types == BulletType.TwoWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])
            elif types == BulletType.ThreeWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])

        if self.immune_ticks > 0:
            self.immune_ticks -= 1
        if not self.is_hit:
            if self.use_bomb:
                self.use_bomb = 0
                if self.bomb_num > 0:
                    self.bomb_num -= 1
                    self.weapon_groups[2].shootWeapon(self.rect.midtop, [0, -SHOOT_SPEED])
            elif self.ticks % SHOOT_CYCLE == 0:
                shootWeapon(bullet_type[self.bullet_type_index], self.rect, self.weapon_groups)

        # 更新武器库
        for weapon_group in self.weapon_groups:
            weapon_group.update()

        if self.ticks >= ANIMATE_CYCLE:
            self.ticks = 0
        if self.is_hit:
            # 英雄战机撞毁特效
            assert self.down_index < len(self.down_surface)     # 校验当前图片不是最后一个
            self.image = self.down_surface[self.down_index]
            if self.ticks % (ANIMATE_CYCLE//2) == 0:
                self.down_index += 1
        else:
            # 英雄存活时特效
            self.image = self.surface[self.ticks//(ANIMATE_CYCLE//2)]
        self.ticks += 1


class EnemyGroup:
    """敌机精灵组"""
    def __init__(self, surface, hit_surface, down_surface, down_sound,
                 score, health, speed, enemy_type, weapon_group):
        self.surface = surface
        self.hit_surface = hit_surface
        self.down_surface = down_surface
        self.group = pygame.sprite.Group()
        self.down_group = pygame.sprite.Group()
        self.down_sound = down_sound
        self.score = score
        self.health = health
        self.speed = speed
        self.enemy_type = enemy_type
        self.weapon_group = weapon_group

    def craeteEnemy(self):
        """产生敌机精灵"""
        def getDirection(surface, spend, enemy_type):
            if enemy_type == EnemyType.EnemyType3:
                # 大型敌机
                enemy_init_pos = [randint(0, SCREEN_WIDTH-surface.get_width()), -surface.get_height()]
                direction = [0, spend]      # 方向速度
            else:
                # 中小型敌机能够从两侧出现
                appearSide = randint(0, 2)
                if appearSide == 0:     # 顶端
                    enemy_init_pos = [randint(0, SCREEN_WIDTH - surface.get_width()), -surface.get_height()]
                    direction = [0, spend]
                elif appearSide == 1:   # 左侧
                    enemy_init_pos = [-surface.get_width(), randint(0, (ENEMY_APPEAR_HEIGHT-surface.get_height()))]
                    direction = [randint(1, spend), randint(1, spend)]
                elif appearSide == 1:   # 右侧
                    enemy_init_pos = [randint(0, (ENEMY_APPEAR_HEIGHT-surface.get_height())), -surface.get_width()]
                    direction = [randint(-spend, -1), randint(-spend, -1)]
            return enemy_init_pos, direction
        # 创建敌机并加入精灵组
        (enemy_init_pos, direction) = getDirection(self.surface[0], self.speed, self.enemy_type)
        enemy = Enemy(self.surface[0], enemy_init_pos, direction, self.weapon_group)
        self.group.add(enemy)

    def update(self):
        self.group.update(self.surface, self.hit_surface)
        if self.weapon_group is not None:
            self.weapon_group.update()  # 递归更新

    def draw(self, screen):
        self.group.draw(screen)         # 绘制到地图
        if self.weapon_group is not None:
            self.weapon_group.draw(screen)

    def checkBulletCollide(self, bullets, screen, ticks):
        score = 0
        self.down_group.add(pygame.sprite.groupcollide(self.group, bullets.group, False, True))
        for enemy_down in self.down_group:  # 遍历所有被子弹击中的敌机
            if enemy_down.is_down:          # 敌机被击毁产生动画效果
                screen.blit(self.down_surface[enemy_down.down_index], enemy_down.rect)
                if ticks % (ANIMATE_CYCLE//2) == 0:
                    if enemy_down.down_index < (len(self.down_surface)-1):
                        if enemy_down.down_index == 0:
                            self.down_sound.play()
                        enemy_down.down_index += 1
                    else:
                        self.down_group.remove(enemy_down)
                        score += self.score
            else:                           # 未击毁减血量
                enemy_down.damage += bullets.damage     # 受损量
                enemy_down.is_hit = ANIMATE_CYCLE //3
                if enemy_down.damage >= self.health:
                    enemy_down.is_down = 1
                    self.group.remove(enemy_down)
                else:
                    self.down_group.remove(enemy_down)
        return  score

    def checkHeroCollide(self, hero):
        enemy_down_list = pygame.sprite.spritecollide(hero, self.group, False)
        collide = False
        if len(enemy_down_list) > 0:
            for enemy_down in enemy_down_list:
                if pygame.sprite.collide_circle_ratio(0.7)(enemy_down, hero):
                    # 英雄和敌机的精准碰撞检测
                    self.group.remove(enemy_down)
                    self.down_group.add(enemy_down)
                    enemy_down.is_down = 1
                    collide = True

        if not collide and self.weapon_group is not None:
            bullet_hit_list = pygame.sprite.spritecollide(hero,self.weapon_group.group, False)
            if len(bullet_hit_list) > 0:
                for bullet_hit in bullet_hit_list:
                    if pygame.sprite.collide_circle_ratio(0.7)(bullet_hit,hero):
                        # 英雄和子弹的碰撞检测
                        self.weapon_group.group.remove(bullet_hit)
                        collide = True
        return collide


class GiftGroup:
    def __init__(self, surface, gift_sound, spend, types):
        self.surface = surface
        self.group = pygame.sprite.Group()
        self.gift_sound = gift_sound
        self.spend = spend
        self.types = types

    def update(self):
        self.group.update()

    def draw(self,screen):
        self.group.update()

    def createGift(self):
        gift = Gift(self.surface, [randint(0,SCREEN_WIDTH-self.surface.get_width()), -self.surface.get_hight()], self.spend)
        self.group.add(gift)

    def checkHeroCollide(self,hero):
        gift_hit_list = pygame.sprite.spritecollide(hero, self.group, False)
        if len(gift_hit_list) > 0:
            for gift in gift_hit_list:
                if pygame.sprite.collide_circle_ratio(0.8)(gift, hero):
                    self.group.remove(gift)
                    self.gift_sound.play()
                    hero.addGift(self.types)


class WeaponGroup:
    def __init__(self, weapon_surface, weapon_sound, damage):
        self.surface = weapon_surface
        self.group = pygame.sprite.Group()
        self.weapon_sound = weapon_sound
        self.damage = damage

    def shootWeapon(self, position, direction):
        weapon = Weapon(self.surface, position, direction)
        self.group.add(weapon)
        self.weapon_sound.play()

    def update(self):
        self.group.update()

    def draw(self, screen):
        self.group.draw(screen)


class EnemyWeaponGroup:
    def __init__(self, weapon_surface, weapon_sound, damage):
        self.surface = weapon_surface
        self.group = pygame.sprite.Group()
        self.weapon_sound = weapon_sound
        self.damage = damage

    def shootWeapon(self, position, direction):
        assert (direction[0] != 0) or (direction[1] != 0)
        weapon = Weapon(self.surface, position, direction)
        self.group.add(weapon)
        self.weapon_sound.play()

    def update(self):
        self.group.update()

    def draw(self, screen):
        self.group.draw(screen)



