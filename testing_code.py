"""Snake game.

Author : Elena, Lucky
Course : Olin Software Design Spring 2017
Date   : 2017-03-05
"""

import pygame
import time

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BlockSize = 50


# class Food(pygame.Rect):


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


class SnakeView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        for rect in model.blocks:
            pygame.draw.rect(surface, BLUE, rect)


class FoodView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        pass


class SnakeController(object):
    def __init__(self, models):
        self.models = models

    def handle_event(self, event):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))

    # food = Food()
    snake = Snake()
    models = [snake]

    views = []
    views.append(SnakeView(snake))
    # views.append(FoodView(food))

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

        pygame.display.update()
        time.sleep(.25)

    pygame.quit()

if __name__ == '__main__':
    main()
