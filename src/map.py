import pygame
from constants import *
import utils

class Map():
    def __init__(self):
        self.entities = [
            # utils.makeDummy(300, 250),
            utils.makePlayer(100, 250)
        ]
        self.platforms = [
            pygame.Rect(100, SCREEN_HEIGHT - 100, 550, 50),
            pygame.Rect(0, 250, 50, 50),
            pygame.Rect(SCREEN_WIDTH-100, 250, 50, 50)

        ]