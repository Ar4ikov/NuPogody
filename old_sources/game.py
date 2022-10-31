#!/usr/bin/env python

import pygame
from pygame import *
import pygame.freetype
from wolf import Wolf
from egg import *
import random


RESOLUTION = (600, 450)
PLAYER_POSITION = (200, 100)
TIME_PER_STEP = 900


def catch_egg(egg, bodyIsLeft, armsIsUp):
    if egg.egg_location == EggLocation.LEFT_UP:
        return bodyIsLeft and armsIsUp
    elif egg.egg_location == EggLocation.LEFT_DOWN:
        return bodyIsLeft and not armsIsUp
    elif egg.egg_location == EggLocation.RIGHT_UP:
        return not bodyIsLeft and armsIsUp
    else:
        return not bodyIsLeft and not armsIsUp


def main():
    pygame.init()
    random.seed(None)
    font = pygame.freetype.Font(None, 20)
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Nu Pogodi!")
    bg = image.load("images/BackgroundScreen.png")
    chikens = image.load("images/chickens.png")
    wolf = Wolf(PLAYER_POSITION)
    bodyIsLeft = True
    armsIsUp = True
    eggs = []
    time = 0
    timer = pygame.time.Clock()
    running = True
    score = 0
    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_LEFT:
                bodyIsLeft = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                bodyIsLeft = False
            if e.type == KEYDOWN and e.key == K_UP:
                armsIsUp = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                armsIsUp = False

        screen.blit(bg, (0, 0))
        screen.blit(chikens, (0, 0))
        wolf.draw(screen, bodyIsLeft, armsIsUp)
        if running:
            time += timer.get_time()
        if time > TIME_PER_STEP:
            time = 0
            shift = False
            for egg in eggs:
                should_catch = egg.update()
                if should_catch:
                    if catch_egg(egg, bodyIsLeft, armsIsUp):
                        score = score + 1
                        shift = True
                    else:
                        running = False
            if shift:
                eggs.pop(0)
            eggs.append(Egg())

        for egg in eggs:
            egg.draw(screen)

        scoreText, _ = font.render("{}".format(score), Color("#ff0000"))
        if not running:
            scoreText, _ = font.render(
                "Game Over {}".format(score), Color("#ff0000"))
        screen.blit(scoreText, (100, 20))
        pygame.display.update()
        if running:
            timer.tick(60)


if __name__ == "__main__":
    main()
