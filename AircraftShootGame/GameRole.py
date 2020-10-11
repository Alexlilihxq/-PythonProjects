# -*- coding: utf-8 -*-
"""
Created on 2020.09.20
author: Alexlilihxq
About : 关于游戏图片元素、音效资源
GitHub : https://github.com/Alexlilihxq
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
    OneWay = 0
    TwoWay = 1
    ThreeWay = 2


class EnemyType(Enum):
    EnemyType1 = 0
    EnemyType2 = 1
    EnemyType3 = 2


bullet_type = [BulletType.OneWay, BulletType.TwoWay, BulletType.ThreeWay]

class Weapon(pygame.sprite.Sprite):
    """武器精灵类"""

    def __init__(self, weapon_surface, weapon_init_pos, direction):
        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = weapon_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = weapon_init_pos     # 左上方坐标
        self.direction = direction

    def update(self):
        # direction[0]:x , direction[1]:y
        self.rect.y += self.direction[1]
        if self.rect.y > SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()



class Enemy(pygame.sprite.Sprite):
    """敌机精灵类"""

    def __init__(self, enemy_surface, enemy_init_pos, direction, weapon_group):
        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos  # 初始位置
        self.direction = direction
        self.down_index = 0
        self.damage = 0                     # 坠毁标识
        self.is_down = 0                    # 底端标识
        self.is_hit = 0                     # 撞击标识
        self.ticks = 0
        self.weapon_group = weapon_group

    def update(self, enemy_surface, hit_surface=0):
        def shootWeapon(weapon_group, position, direction):
            """
            敌机射击方法
            position    起始位置
            direction   方向（速度）
            """
            # 此处的shootWeapon为武器精灵组的方法
            weapon_group.shootWeapon(position, direction)

        # direction[0]:x , direction[1]:y
        should_kill = False     # 是否销毁精灵判断标识
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        if self.rect.x > SCREEN_WIDTH or self.rect.x < -self.image.get_width():
            should_kill = True
        if self.rect.y > SCREEN_HEIGHT or self.rect.y < -self.image.get_height():
            should_kill = True

        if should_kill:
            self.kill()
        else:
            if self.ticks >= ENEMY_SHOOT_CYCLE:
                self.ticks = 0

            if self.is_hit:
                self.is_hit -= 1
                self.image = hit_surface    # 撞击后将敌机图像切换成爆炸效果
            elif len(enemy_surface) >= 2:   # 爆炸动画效果
                self.image = enemy_surface[self.ticks // (ENEMY_SHOOT_CYCLE // 2)]  # 爆炸效果动画切换
            else:
                self.image = enemy_surface[0]

            self.ticks += 1
            if self.weapon_group is not None:  # 敌机射击动作
                if self.ticks % ENEMY_SHOOT_CYCLE == 0:
                    shootWeapon(self.weapon_group, [self.rect.centerx, self.rect.y + self.image.get_height()], [0, ENEMY_SHOOT_SPEED])


class Gift(pygame.sprite.Sprite):
    """道具精灵类"""

    def __init__(self, gift_surface, gift_init_pos, speed):
        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
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
        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
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
        self.is_hit = False
        self.down_index = 0
        self.bullet_type_index = 0      # 子弹类型索引
        self.bomb_num = 0               # 重置镭弹
        self.use_bomb = 0
        self.immune_ticks = 0           # 重生免疫时间

    def moving(self, offset):
        """英雄移动方法，offset为事件串"""
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
        """使用镭弹状态"""
        if self.bomb_num:
            self.use_bomb = 1

    def getBombNum(self):
        """获取Bomb数量"""
        return self.bomb_num

    def addGift(self, types):
        """道具强化"""
        if types == GameGift.Bomb:
            self.bomb_num += 1
        elif types == GameGift.PowerBullet:
            if self.bullet_type_index < len(bullet_type)-1:
                self.bullet_type_index += 1
        else:
            pass
            # self.Laser_num += 1

    def isHeroCrash(self):
        """Hero撞击"""
        if self.immune_ticks <= 0 and not self.is_hit:
            self.is_hit = True
            self.life -= 1
            return 1
        else:
            return 0

    def restart(self):
        """英雄重生"""
        self.reset()
        self.immune_ticks = 180                 # 3秒无敌金身
        self.rect.topleft = self.hero_init_pos  # 初始化位置

    def update(self):
        def getBulletPosition(rect, position_type):
            """定义Hero武器位置"""
            if position_type == 0:
                return [rect.centerx - 3, rect.centery]
            elif position_type == 1:
                return [rect.x + 10, rect.centery]
            else:
                return [rect.x + rect.width - 20, rect.centery]

        def shootWeapon(types, rect, weapon_groups):
            """英雄射击方法"""
            weapon_index = 0
            weapon_direction = [[0, -SHOOT_SPEED], [-SHOOT_SPEED, 0], [SHOOT_SPEED, 0]]
            if types == BulletType.OneWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
            elif types == BulletType.TwoWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])
            elif types == BulletType.ThreeWay:
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 0), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 1), weapon_direction[0])
                weapon_groups[weapon_index].shootWeapon(getBulletPosition(self.rect, 2), weapon_direction[0])

        if self.immune_ticks > 0:       # 无敌时间削减
            self.immune_ticks -= 1
        if not self.is_hit:
            if self.use_bomb:           # 使用镭弹状态
                self.use_bomb = 0
                if self.bomb_num > 0:   # 使用镭弹
                    self.bomb_num -= 1
                    self.weapon_groups[2].shootWeapon(self.rect.midtop, [0, -SHOOT_SPEED])
            elif self.ticks % SHOOT_CYCLE == 0:  # 普通射击动作
                shootWeapon(bullet_type[self.bullet_type_index], self.rect, self.weapon_groups)

        # 更新武器库状态
        for weapon_group in self.weapon_groups:
            weapon_group.update()

        if self.ticks >= ANIMATE_CYCLE:
            self.ticks = 0
        if self.is_hit:
            # 英雄战机撞毁时动画特效
            assert self.down_index < len(self.down_surface)     # 校验当前图片索引未超过最大索引
            self.image = self.down_surface[self.down_index]
            if self.ticks % (ANIMATE_CYCLE // 2) == 0:
                self.down_index += 1
        else:
            # 英雄存活时动画效果
            self.image = self.surface[self.ticks // (ANIMATE_CYCLE // 2)]
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

    def createEnemy(self):
        """产生敌机精灵"""

        def getDirection(surface, speed, enemy_type):
            """区别敌机而产生的方向速度"""
            if enemy_type == EnemyType.EnemyType3:
                # 大型敌机出现
                enemy_init_pos = [randint(0, SCREEN_WIDTH - surface.get_width()), -surface.get_height()]
                direction = [0, speed]  # 方向速度
            else:
                # 中小型敌机能够从两侧出现
                appearSide = randint(0, 2)
                if appearSide == 0:  # 顶端
                    enemy_init_pos = [randint(0, SCREEN_WIDTH - surface.get_width()), -surface.get_height()]
                    direction = [0, speed]
                elif appearSide == 1:  # 左侧
                    enemy_init_pos = [-surface.get_width(), randint(0, (ENEMY_APPEAR_HEIGHT - surface.get_height()))]
                    direction = [randint(1, speed), randint(1, speed)]
                elif appearSide == 2:  # 右侧
                    enemy_init_pos = [SCREEN_WIDTH, randint(0, (ENEMY_APPEAR_HEIGHT - surface.get_height()))]
                    direction = [randint(-speed, -1), randint(1, speed)]
            return enemy_init_pos, direction

        # 创建敌机并加入精灵组
        (enemy_init_pos, direction) = getDirection(self.surface[0], self.speed, self.enemy_type)
        enemy = Enemy(self.surface[0], enemy_init_pos, direction, self.weapon_group)
        self.group.add(enemy)

    def update(self):
        self.group.update(self.surface, self.hit_surface)
        if self.weapon_group is not None:
            self.weapon_group.update()  # 更新武器库

    def draw(self, screen):
        self.group.draw(screen)         # 绘制到地图
        if self.weapon_group is not None:
            self.weapon_group.draw(screen)

    def checkBulletCollide(self, bullets, screen, ticks):
        """子弹和敌机的碰撞检测"""
        score = 0
        self.down_group.add(pygame.sprite.groupcollide(self.group, bullets.group, False, True))
        for enemy_down in self.down_group:  # 遍历所有被子弹击中的敌机
            if enemy_down.is_down:          # 敌机被击毁产生动画效果
                screen.blit(self.down_surface[enemy_down.down_index], enemy_down.rect)
                if ticks % (ANIMATE_CYCLE // 2) == 0:
                    if enemy_down.down_index < (len(self.down_surface) - 1):
                        if enemy_down.down_index == 0:
                            self.down_sound.play()          # 播放击毁音效
                        enemy_down.down_index += 1
                    else:
                        self.down_group.remove(enemy_down)  # 播放完从坠机组移除
                        score += self.score
            else:                                           # 击中未击毁减血量
                enemy_down.damage += bullets.damage         # 敌机受损量
                enemy_down.is_hit = ANIMATE_CYCLE // 3
                if enemy_down.damage >= self.health:
                    enemy_down.is_down = 1
                    self.group.remove(enemy_down)
                else:
                    self.down_group.remove(enemy_down)      # 敌机未坠毁则不必要加入enemy_down
        return score                                        # 返回本次得分值

    def checkHeroCollide(self, hero):
        """英雄和敌机的碰撞检测"""
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
            bullet_hit_list = pygame.sprite.spritecollide(hero, self.weapon_group.group, False)
            # 英雄和敌机子弹的碰撞检测
            if len(bullet_hit_list) > 0:
                for bullet_hit in bullet_hit_list:
                    if pygame.sprite.collide_circle_ratio(0.7)(bullet_hit, hero):
                        # 英雄和子弹的敏感性碰撞检测
                        # 上面未kill，此处判断撞击后kill
                        self.weapon_group.group.remove(bullet_hit)
                        collide = True
        return collide


class GiftGroup:
    """道具精灵组"""
    def __init__(self, surface, gift_sound, speed, types):
        self.surface = surface
        self.group = pygame.sprite.Group()
        self.gift_sound = gift_sound
        self.speed = speed
        self.types = types

    def update(self):
        self.group.update()

    def draw(self, screen):
        self.group.draw(screen)

    def createGift(self):
        """创建道具，实例化后加入精灵组"""
        gift = Gift(self.surface, [randint(0, SCREEN_WIDTH - self.surface.get_width()), -self.surface.get_height()],
                    self.speed)
        self.group.add(gift)

    def checkHeroCollide(self, hero):
        """英雄和道具的敏感性碰撞检测"""
        gift_hit_list = pygame.sprite.spritecollide(hero, self.group, False)
        if len(gift_hit_list) > 0:              # 同时拾取到多个道具的情况
            for gift in gift_hit_list:
                if pygame.sprite.collide_circle_ratio(0.8)(gift, hero):
                    self.group.remove(gift)
                    self.gift_sound.play()      # 拾取道具音效
                    hero.addGift(self.types)    # 执行道具动作


class WeaponGroup:
    """英雄武器精灵组"""
    def __init__(self, weapon_surface, weapon_sound, damage):
        self.surface = weapon_surface
        self.group = pygame.sprite.Group()
        self.weapon_sound = weapon_sound
        self.damage = damage

    def shootWeapon(self, position, direction):
        # 实例化武器并加入精灵组
        weapon = Weapon(self.surface, position, direction)
        self.group.add(weapon)
        self.weapon_sound.play()  # 射击音效

    def update(self):
        self.group.update()

    def draw(self, screen):
        self.group.draw(screen)


class EnemyWeaponGroup:
    """敌机武器精灵"""
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
