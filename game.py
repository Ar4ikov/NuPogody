import time as t

import pygame
from pygame import *
import random
import pathlib


basement = pathlib.Path(__file__).parent.absolute()
images = basement / 'images'
sounds = basement / 'sounds'
fonts = basement / 'fonts'


WIDTH = 1000
HEIGHT = 630
FPS = 30

TICK_TIME = 1.
SPEED = 1.05

GRAY = Color(151, 151, 151)


class EggCatcherGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Egg Catcher")
        self.clock = pygame.time.Clock()
        self.running = True

        self.entities = pygame.sprite.Group()
        self.eggs = pygame.sprite.Group()

        self.background = pygame.image.load(images / 'background.png')
        self.grass = pygame.image.load(images / 'grass.png')
        self.right_chicken = pygame.image.load(images / 'right_chicken.png')
        self.life = pygame.image.load(images / 'life.png')

        self.background.set_colorkey(GRAY)
        self.grass.set_colorkey(GRAY)
        self.right_chicken.set_colorkey(GRAY)

        self.player = WolfPlayer(200, 220)
        self.rabbit = Rabbit(110, 0)

        self.entities.add(self.rabbit)
        self.entities.add(self.player)

        self.eggs_left_up = 0
        self.eggs_left_down = 0
        self.eggs_right_up = 0
        self.eggs_right_down = 0

        self.score = 0
        self.lives = 3
        self.enable_sound = True

        self.current_max_eggs = 1
        self.max_eggs = 5

        self.font = pygame.font.Font(fonts / "digital-7.ttf", 72)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(), 42)

        self.egg_ride_sound = pygame.mixer.Sound(str(sounds / 'egg_ride.ogg'))
        self.egg_crack_sound = pygame.mixer.Sound(str(sounds / 'egg_crack.ogg'))
        self.egg_catch_sound = pygame.mixer.Sound(str(sounds / 'egg_catch.ogg'))

    def summon_egg(self, left, up):
        c = min(self.current_max_eggs, self.max_eggs)

        if self.eggs_left_up >= c and left and up:
            return None

        if self.eggs_left_down >= c and left and not up:
            return None

        if self.eggs_right_up >= c and not left and up:
            return None

        if self.eggs_right_down >= c and not left and not up:
            return None

        egg = Egg(self, left, up)

        return egg

    def count_eggs(self):
        self.eggs_left_up = 0
        self.eggs_left_down = 0
        self.eggs_right_up = 0
        self.eggs_right_down = 0

        for egg in self.eggs:
            if egg.left:
                if egg.up:
                    self.eggs_left_up += 1
                else:
                    self.eggs_left_down += 1
            else:
                if egg.up:
                    self.eggs_right_up += 1
                else:
                    self.eggs_right_down += 1

    def play_again(self):
        global TICK_TIME
        TICK_TIME = 1.
        self.score = 0
        self.lives = 3
        self.eggs.empty()

    def main_loop(self):
        global TICK_TIME
        last_time = t.time()

        while self.running:
            self.clock.tick(FPS)
            TICK_TIME = max(1. / max(SPEED ** (self.score // 42 + 1), 1), 0.5)
            self.current_max_eggs = max(1, self.score // 15 + 1)

            if self.lives <= 0:
                self.screen.fill(GRAY)

                text = self.end_font.render(f'Игра окончена! Счет: {self.score}', True, (20, 20, 20))
                text_again = self.end_font.render('Нажмите [SPACE] для повтора', True, (20, 20, 20))

                text_rect = text.get_rect()
                text_rect.center = (WIDTH // 2, HEIGHT // 2)

                text_again_rect = text_again.get_rect()
                text_again_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

                self.screen.blit(text, text_rect)
                self.screen.blit(text_again, text_again_rect)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False

                    if e.type == KEYDOWN:
                        if e.key == K_ESCAPE or e.key == K_q:
                            self.running = False

                        if e.key == K_SPACE:
                            self.play_again()

                pygame.display.flip()
                pygame.display.update()

                continue

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False

                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE or e.key == K_q:
                        self.running = False

                    self.player.update_position(e.key)
                    self.rabbit.update_position(e.key)

            self.screen.fill(GRAY)
            self.screen.blit(self.background, (0, 0))

            if abs(t.time() - last_time) >= TICK_TIME:
                last_time = t.time()
                egg = self.summon_egg(random.choice([True, False]), random.choice([True, False]))

                if egg:
                    self.eggs.add(egg)

                if self.enable_sound:
                    self.egg_ride_sound.play()

            self.count_eggs()

            self.entities.draw(self.screen)
            self.eggs.draw(self.screen)
            self.eggs.update()
            self.entities.update()

            self.screen.blit(self.right_chicken, (0, 0))

            for i in range(abs(self.lives - 3)):
                self.screen.blit(self.life, (500 + i * 80, 50))

            self.screen.blit(self.grass, (0, 530))

            score_text = self.font.render(str(self.score), True, (20, 20, 20))
            self.screen.blit(score_text, (800, 50))

            self.enable_sound = self.rabbit.state

            pygame.display.flip()
            pygame.display.update()

    @staticmethod
    def clean_up():
        pygame.quit()


class WolfPlayer(pygame.sprite.Sprite):
    def __init__(self, left, up):
        super().__init__()

        self.image = pygame.image.load('images/wolf_left_up.png')
        self.image.set_colorkey(GRAY)
        self.rect = self.image.get_rect()

        self.rect.x = left
        self.rect.y = up

        self.left = True
        self.up = True

        names = ["wolf_left_up.png", "wolf_left_down.png", "wolf_right_up.png", "wolf_right_down.png"]
        sides = ['left_up', 'left_down', 'right_up', 'right_down']

        self.images = [pygame.image.load(images / x) for x in names]
        [x.set_colorkey(GRAY) for x in self.images]

        self.images_x_pos = {k: v for k, v in zip(sides, self.images)}

    def update_position(self, _key):
        if _key == K_LEFT or _key == K_a:
            self.left = True

        elif _key == K_RIGHT or _key == K_d:
            self.left = False

        elif _key == K_UP or _key == K_w:
            self.up = True

        elif _key == K_DOWN or _key == K_s:
            self.up = False

    def update(self):
        if self.left:
            if self.up:
                self.image = self.images_x_pos['left_up']

            else:
                self.image = self.images_x_pos['left_down']

        else:
            if self.up:
                self.image = self.images_x_pos['right_up']

            else:
                self.image = self.images_x_pos['right_down']


class Rabbit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(images / 'rabbit_on.png')
        self.image.set_colorkey(GRAY)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.state = True
        names = ["rabbit_on.png", "rabbit_off.png"]
        self.images = [pygame.image.load(images / x) for x in names]
        [x.set_colorkey(GRAY) for x in self.images]

    def update_position(self, _key):
        if _key == K_1:
            self.state = not self.state

    def update(self):
        if self.state:
            self.image = self.images[0]

        else:
            self.image = self.images[1]


class Egg(pygame.sprite.Sprite):
    def __init__(self, _game, left=False, up=False):
        super().__init__()

        self.left, self.up = left, up
        self.game = _game

        self.image = pygame.image.load(images / 'egg_1.png')
        self.image.set_colorkey(GRAY)
        self.rect = self.image.get_rect()

        self.images_left = [pygame.image.load(images / f'egg_{i + 1}.png') for i in range(6)]
        [x.set_colorkey(GRAY) for x in self.images_left]

        self.images_right = self.images_left.copy()
        self.images_right = [pygame.transform.flip(x, True, False) for x in self.images_right]
        [x.set_colorkey(GRAY) for x in self.images_right]

        self.chicken_down_left = [(160, 480), (132, 480), (96, 480), (62, 480), (38, 480)]
        self.chicken_down_right = [(720, 480), (760, 480), (826, 480), (860, 480), (920, 480)]

        self.left_up_xy = [(63, 178), (96, 197), (131, 228), (154, 249), (197, 258)]
        self.left_down_xy = [(63, 324), (96, 343), (131, 364), (154, 395), (197, 404)]
        self.right_up_xy = [(918, 178), (881, 200), (840, 218), (805, 239), (775, 258)]
        self.right_down_xy = [(918, 324), (881, 343), (840, 364), (805, 385), (775, 404)]

        self.left_up = [(x, self.images_left[0]) for x in self.left_up_xy] + \
                       [(x, y) for x, y in zip(self.chicken_down_left, self.images_left[1:])]

        self.left_down = [(x, self.images_left[0]) for x in self.left_down_xy] + \
                         [(x, y) for x, y in zip(self.chicken_down_left, self.images_left[1:])]

        self.right_up = [(x, self.images_left[0]) for x in self.right_up_xy] + \
                        [(x, y) for x, y in zip(self.chicken_down_right, self.images_right[1:])]

        self.right_down = [(x, self.images_left[0]) for x in self.right_down_xy] + \
                          [(x, y) for x, y in zip(self.chicken_down_right, self.images_right[1:])]

        self.right_deg = 30
        self.left_deg = -30

        self.animation = self.set_animation(left, up)
        self.state = 0
        self.dropped = False
        self.time = t.time()

    def set_animation(self, left, up):
        if left:
            if up:
                return self.left_up

            else:
                return self.left_down

        else:
            if up:
                return self.right_up

            else:
                return self.right_down

    def update(self):
        if (self.game.player.left, self.game.player.up) == (self.left, self.up) and self.state == 4:
            self.game.score += 1

            if self.game.enable_sound:
                self.game.egg_catch_sound.play()

            self.kill()

        if self.state > 4 and not self.dropped:
            self.dropped = True
            self.game.lives -= 1

            if self.game.enable_sound:
                self.game.egg_crack_sound.play()

        if self.state >= 10:
            self.kill()
            return

        if abs(self.time - t.time()) >= TICK_TIME and not self.dropped:
            self.time = t.time()

            self.state += 1

        elif abs(self.time - t.time()) >= 0.2 and self.dropped:
            self.time = t.time()
            self.state += 1

        (x, y), img = self.animation[min(self.state, 9)]
        self.image = img
        self.rect.x = x
        self.rect.y = y

        if self.state <= 4:
            if self.left:
                self.image = pygame.transform.rotate(self.image, self.left_deg * self.state)
                self.image.set_colorkey(GRAY)

            else:
                self.image = pygame.transform.rotate(self.image, self.right_deg * self.state)
                self.image.set_colorkey(GRAY)


if __name__ == '__main__':
    game = EggCatcherGame()
    game.main_loop()
    game.clean_up()
