from pygame import *


class Wolf(sprite.Sprite):
    def __init__(self, player_position):
        sprite.Sprite.__init__(self)
        self.bodyLeft = image.load('images/WolfBodyLeft.png')
        self.bodyRight = image.load('images/WolfBodyRight.png')
        self.armDownLeft = image.load('images/Arms/armDownLeft.png')
        self.armDownRight = image.load('images/Arms/armDownRight.png')
        self.armUpLeft = image.load('images/Arms/armUpLeft.png')
        self.armUpRight = image.load('images/Arms/armUpRight.png')

        self.player_position = player_position
        self.arms_position = (0, 0)

    def draw(self, screen, left, up):
        if left:
            screen.blit(self.bodyLeft, self.player_position)
            if up:
                screen.blit(self.armUpLeft, self.arms_position)
            else:
                screen.blit(self.armDownLeft, self.arms_position)
        else:
            screen.blit(self.bodyRight, self.player_position)
            if up:
                screen.blit(self.armUpRight, self.arms_position)
            else:
                screen.blit(self.armDownRight, self.arms_position)
