"""Snake game.

Author : Elena, Lucky
Course : Olin Software Design Spring 2017
Date   : 2017-03-05
"""

import pygame
from pygame.locals import *
import time
import random

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BlockSize = 25
WINDOW = 1000


# class Food(pygame.Rect):


class Snake(object):
    def __init__(self, length=30, x=0, y=600, direction='d'):
        self.x = x
        self.y = y
        self.direction = direction
        self.blocks = []
        k = self.scale_factors()
        for i in range(length):
            ypos = y - BlockSize*i*k[1]
            xpos = x - BlockSize*i*k[0]
            block = pygame.Rect(xpos, ypos, BlockSize, BlockSize)
            self.blocks.append(block)

    def step(self):
        k = self.scale_factors()
        for i in range(len(self.blocks)-1):
            self.blocks[len(self.blocks)-(i+1)].x = self.blocks[len(self.blocks)-(i+2)].x
            self.blocks[len(self.blocks)-(i+1)].y = self.blocks[len(self.blocks)-(i+2)].y
        self.blocks[0].x = self.blocks[0].x + k[0]*BlockSize
        self.blocks[0].y = self.blocks[0].y + k[1]*BlockSize

    def scale_factors(self):
        if self.direction == 'd':
            yfact = 1
            xfact = 0
        elif self.direction == 'u':
            yfact = -1
            xfact = 0
        elif self.direction == 'l':
            yfact = 0
            xfact = -1
        elif self.direction == 'r':
            yfact = 0
            xfact = 1
        return [xfact, yfact]

    def check_collision(self):
        count = 0
        for block in self.blocks:
            if count != 0 and self.blocks[0].x == block.x and self.blocks[0].y == block.y:
                return True
            count += 1
        return False

    def check_boundary(self):
        x = self.blocks[0].x
        y = self.blocks[0].y
        if x < 0 or y < 0 or x >= WINDOW or y >= WINDOW:
            return True
        return False


class SnakeView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        for rect in model.blocks:
            pygame.draw.rect(surface, BLUE, rect)

class Food(object):
    def __init__(self):
        self.x = random.randint(0,40)*25
        self.y = random.randint(0,40)*25
        self.rect = pygame.Rect(self.x, self.y, BlockSize, BlockSize)

class FoodView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.rect(surface, RED, model.rect)


class SnakeController(object):
    def __init__(self, models):
        self.models = models

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                if self.models[0].direction != 'r':
                    self.models[0].direction = 'l'

            if keys[K_RIGHT]:
                if self.models[0].direction != 'l':
                    self.models[0].direction = 'r'

            if keys[K_UP]:
                if self.models[0].direction != 'd':
                    self.models[0].direction = 'u'

            if keys[K_DOWN]:
                if self.models[0].direction != 'u':
                    self.models[0].direction = 'd'


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW, WINDOW))

    # food = Food()
    food = Food()
    models = [food]

    snake = Snake()
    models = [snake]

    views = []
    views.append(SnakeView(snake))
    views.append(FoodView(food))

    controller = SnakeController(models)

    running = True
    while running:
        for event in pygame.event.get():
            controller.handle_event(event)
            if event.type == pygame.QUIT:
                running = False

        for model in models:
            model.step()

        screen.fill(BLACK)
        for view in views:
            view.draw(screen)

        if snake.check_collision():
            running = False

        if snake.check_boundary():
            running = False

        pygame.display.update()
        time.sleep(.1)

    pygame.quit()


if __name__ == '__main__':
    main()
