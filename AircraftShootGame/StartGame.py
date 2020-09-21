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
    def