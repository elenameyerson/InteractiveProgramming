"""Snake game.

Author : Elena, Lucky
Course : Olin Software Design Spring 2017
Date   : 2017-03-05
"""

import pygame
from pygame.locals import *
import time
import random
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BlockSize = 25
WINDOW = 1000


class Snake(object):
    def __init__(self, length=5, x=0, y=600, direction='d'):
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

    def grow_snake(self, num):
        difx = self.blocks[-1].x-self.blocks[-2].x
        dify = self.blocks[-1].y-self.blocks[-2].y

        if difx == 0:
            if dify < 0:
                # up
                yfact = -1
                xfact = 0
            else:
                # down
                yfact = 1
                xfact = 0
        elif difx < 0:
            # left
            yfact = 0
            xfact = -1
        else:
            # right
            yfact = 0
            xfact = 1

        for i in range(num):
            ypos = self.blocks[-1].y + BlockSize*i*yfact
            xpos = self.blocks[-1].x + BlockSize*i*xfact
            block = pygame.Rect(xpos, ypos, BlockSize, BlockSize)
            self.blocks.append(block)

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

    def check_food(self, food):
        if self.blocks[0].x == food.x and self.blocks[0].y == food.y:
            return True
        return False

    def reset(self):
        self.__init__()


class SnakeView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        for rect in model.blocks:
            pygame.draw.rect(surface, BLUE, rect)


class Food(object):
    def __init__(self):
        self.x = random.randint(0, WINDOW/BlockSize-1)*BlockSize
        self.y = random.randint(0, WINDOW/BlockSize-1)*BlockSize
        self.rect = pygame.Rect(self.x, self.y, BlockSize, BlockSize)

    def step(self):
        pass

    def reset(self):
        self.__init__()


class FoodView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.rect(surface, RED, model.rect)


class Score(object):
    def __init__(self, val=0):
        self.val = val

    def add_point(self, points=1):
        self.val += points

    def step(self):
        pass

    def reset(self):
        self.__init__()


class ScoreView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        score = self.model.val
        font = pygame.font.SysFont("monospace", 15)
        label = font.render("Score: " + str(score), 1, WHITE)
        surface.blit(label, (5, 5))


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

    score = Score()
    food = Food()
    snake = Snake()
    models = [snake, food, score]

    views = []
    views.append(SnakeView(snake))
    views.append(FoodView(food))
    views.append(ScoreView(score))

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
            for model in models:
                model.reset()

        if snake.check_boundary():
            for model in models:
                model.reset()

        if snake.check_food(food):
            on_snake = True
            while on_snake:
                food.__init__()
                on_snake = False
                for block in snake.blocks:
                    if block.x == food.x and block.y == food.y:
                        this = True
                    else:
                        this = False
                    on_snake = on_snake or this
            snake.grow_snake(3)
            score.add_point()
            print(score.val)

        if score.val == 99:
            running = False

        pygame.display.update()
        time.sleep(.1-.01*math.sqrt(score.val))

    pygame.quit()


if __name__ == '__main__':
    main()
