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

# some global variables colors, block size (sets game grid), and window (sets pygame screen size - square)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BlockSize = 25
WINDOW = 1000


class Snake(object):
    """ The snake class is a model of our snake object.

        length: number of blocks which make up the snake (default 5)
        x: x position of the snake's head (default 0)
        y: y position of the snake's head (default 600)
        direction: direction of movement of snake's head (left 'l', right 'r', down 'd' or up 'u') (default down 'd')
    """
    def __init__(self, length=5, x=0, y=600, direction='d'):
        self.x = x
        self.y = y
        self.direction = direction
        self.blocks = []
        k = self.scale_factors()  # finds scale factors (0, -1 or 1) based on direction to determine where to build trailing blocks
        for i in range(length):  # populates slef.blocks with list of block rect objects to be drawn by SnakeView
            ypos = y - BlockSize*i*k[1]
            xpos = x - BlockSize*i*k[0]
            block = pygame.Rect(xpos, ypos, BlockSize, BlockSize)
            self.blocks.append(block)

    def step(self):
        """ Each step (each run of the while loop in the main function) the snake will move one block in the direction
            of the head. Our model to control this goes through the list of blocks starting at the end and replaces
            each block's x and y positions with those of the block in front of it up through the 2nd block in the list.
            The head block is then moved according the scale_factors determined by the direction.
        """
        k = self.scale_factors()
        for i in range(len(self.blocks)-1):
            self.blocks[len(self.blocks)-(i+1)].x = self.blocks[len(self.blocks)-(i+2)].x
            self.blocks[len(self.blocks)-(i+1)].y = self.blocks[len(self.blocks)-(i+2)].y
        self.blocks[0].x = self.blocks[0].x + k[0]*BlockSize
        self.blocks[0].y = self.blocks[0].y + k[1]*BlockSize

    def scale_factors(self):
        """ Helper func which determines scale_factors depending on the direction of movement of the snake's head.
            example: if down the y position is decreasing (-1) and the x position is staying the same (0)

            returns: [x scale factor, y scale factor] in other words, a scale factor is the number of block sizes
            to move based on the direction
        """
        if self.direction == 'd':
            # down
            yfact = 1
            xfact = 0
        elif self.direction == 'u':
            # up
            yfact = -1
            xfact = 0
        elif self.direction == 'l':
            # left
            yfact = 0
            xfact = -1
        elif self.direction == 'r':
            # right
            yfact = 0
            xfact = 1
        return [xfact, yfact]

    def grow_snake(self, num):
        """ This function runs when the snake eats the food block. It adds num (in this case always 3) blocks to the
            end of the snake in the same direction of the tail at the time of growth.
            It finds the direction based on the position of the last block in the block list relative to the second
            to last block and adds new blocks in that direction.
        """
        difx = self.blocks[-1].x-self.blocks[-2].x
        dify = self.blocks[-1].y-self.blocks[-2].y

        """ the following if statement looks much like scale factors, there is probably a good way to combine them to avoid
            duplicate code but at this time the important difference is that in this case we do not wan to change the
            attribute self.direction and therefore can't use the scale_factors function in its current form
        """
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

        for i in range(num):  # generate and add blocks to self.blocks list in proper direction
            ypos = self.blocks[-1].y + BlockSize*i*yfact
            xpos = self.blocks[-1].x + BlockSize*i*xfact
            block = pygame.Rect(xpos, ypos, BlockSize, BlockSize)
            self.blocks.append(block)

    def check_collision(self):
        """ Goes through each block in list and determines if head block is in same position as that body block.
            If any block is in the same position as the head block the function returns true. If it goes through
            the for loop without finding any collision if defaults to returning fales.
        """
        count = 0
        for block in self.blocks:
            if count != 0 and self.blocks[0].x == block.x and self.blocks[0].y == block.y:
                return True
            count += 1
        return False

    def check_boundary(self):
        """ Determines if head block exits pygame screen window (if x or y position is < 0 or > window size)
            Defaults to returning false.
        """
        x = self.blocks[0].x
        y = self.blocks[0].y
        if x < 0 or y < 0 or x >= WINDOW or y >= WINDOW:
            return True
        return False

    def check_food(self, food):
        """ Checks if head block is in the same x and y position as the food block. Takes the food block as an input argument
            to use its x and y position.
            Defaults to returning false.
        """
        if self.blocks[0].x == food.x and self.blocks[0].y == food.y:
            return True
        return False

    def reset(self):
        self.__init__()


class SnakeView(object):
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        """ For each block in the snake model blocks list SnakeView draws the rect object
            as a blue rectangle which is part of the snake's body.
        """
        model = self.model
        for rect in model.blocks:
            pygame.draw.rect(surface, BLUE, rect)


class Food(object):
    """ The food model contains one rect object which is randomly assigned an x and y position.
        The step function could be used for interesting game funcitonality later on but is
        passed for now.
    """
    def __init__(self):
        self.x = random.randint(0, WINDOW/BlockSize-1)*BlockSize
        self.y = random.randint(0, WINDOW/BlockSize-1)*BlockSize
        self.rect = pygame.Rect(self.x, self.y, BlockSize, BlockSize)

    def step(self):
        pass

    def reset(self):
        self.__init__()


class FoodView(object):
    """ FoodView simply draws the one rectangle which represents the food at the random x and y position its init func generates. """
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        model = self.model
        pygame.draw.rect(surface, RED, model.rect)


class Score(object):
    """ Score model. Starts at 0 by default and add_point adds a point when the snake eats the food. """
    def __init__(self, val=0):  # by default starts at 0
        self.val = val

    def add_point(self, points=1):
        self.val += points

    def step(self):
        pass

    def reset(self):
        self.__init__()


class ScoreView(object):
    """ ScoreView uses blit to draw text on the screen containing the current score. """
    def __init__(self, model):
        self.model = model

    def draw(self, surface):
        score = self.model.val
        font = pygame.font.SysFont("monospace", 15)
        label = font.render("Score: " + str(score), 1, WHITE)
        surface.blit(label, (5, 5))


class SnakeController(object):
    """ The snake controller manages input from the user in the form of keypresses on
        the directional pad. In this case it changes the snake's direction attribute as
        long as the input doesn't cause the snake to perform a 180 deg turn.
    """
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
    screen = pygame.display.set_mode((WINDOW, WINDOW))  # initialize and display window

    # creating model objects
    score = Score()
    food = Food()
    snake = Snake()
    models = [snake, food, score]

    # populating list of views with view objects and their corresponding model attributes
    views = []
    views.append(SnakeView(snake))
    views.append(FoodView(food))
    views.append(ScoreView(score))

    # set up snake controller with all models (currently only controls snake but could be used to perform functions with score and food based on user input)
    controller = SnakeController(models)

    # MAIN WHILE LOOP
    running = True
    while running:
        for event in pygame.event.get():
            controller.handle_event(event)  # runs controller handler if event in pygame.event library happens (keypresses in this case)
            if event.type == pygame.QUIT:
                running = False

        for model in models:  # uses step functions of models to update model through each run of while loop
            model.step()

        screen.fill(BLACK)
        for view in views:  # uses view functions of view objects to draw their respective models
            view.draw(screen)

        if snake.check_collision():  # resets game if snake collides with itself is true
            for model in models:
                model.reset()

        if snake.check_boundary():  # resets game if snake's head exits screen boundary is true
            for model in models:
                model.reset()

        if snake.check_food(food):  # checks if snake has eaten food, if true runs
            on_snake = True
            while on_snake:  # keeps initializing the food until it is not on top of any of the snake blocks
                food.__init__()
                on_snake = False
                for block in snake.blocks:
                    if block.x == food.x and block.y == food.y:
                        this = True
                    else:
                        this = False
                    on_snake = on_snake or this  # or statment such that if food is on any block then on_snake equals true
            # when food initializing is done, grows snake and adds point to score
            snake.grow_snake(3)
            score.add_point()
            print(score.val)

        if score.val == 99:  # ends game when score reaches 99
            running = False

        pygame.display.update()
        time.sleep(.1-.01*math.sqrt(score.val))  # pauses game to make it playable, pause time decreses as a function of score

    pygame.quit()


if __name__ == '__main__':
    main()
