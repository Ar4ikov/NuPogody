from pygame import *
import random
from enum import Enum


LEFT_UP_POSITIONS = [(60, 120), (90, 140), (120, 160)]
LEFT_DOWN_POSITIONS = [(60, 260), (90, 275), (120, 290)]
RIGHT_UP_POSITIONS = [(520, 120), (495, 135), (460, 160)]
RIGHT_DOWN_POSITIONS = [(520, 260), (495, 270), (460, 290)]

EGG_POSITIONS = [LEFT_UP_POSITIONS, LEFT_DOWN_POSITIONS,
                 RIGHT_UP_POSITIONS, RIGHT_DOWN_POSITIONS]


class EggLocation(Enum):
    LEFT_UP = 0
    LEFT_DOWN = 1
    RIGHT_UP = 2
    RIGHT_DOWN = 3


class Egg(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = image.load('images/newEgg.png')
        self.egg_location = EggLocation(
            random.randint(0, len(EGG_POSITIONS)-1))
        self.positions = EGG_POSITIONS[self.egg_location.value]
        self.index = 0

    def update(self):
        self.index += 1
        return self.index >= len(self.positions)

    def draw(self, screen):
        drawIndex = self.index
        if drawIndex >= len(self.positions):
            drawIndex = len(self.positions)-1
        screen.blit(self.image, self.positions[drawIndex])
