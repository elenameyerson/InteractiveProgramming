'''
pygame notes:
-easy to define windows
-easy to handle events (key presses, mouse motion)
-drawing rectangles is well documented

opencv:
-easy to open camera
-already has facial recognition code
-can likely map that to tongue recognition

classes:

MVP
window (the window in which the game is played which defines the boundaries)
    length, width

food (the block the snake has to eat to grow)
    xpos, ypos, point_value

snake (the snake)
    xpos, ypos, direction, length
    method ideas:
        move
            move each block to the position of the block in front of it
        turn
            change in direction as response to keypress
        grow
            identify when snake overlaps food
            add certain number of blocks to back
            add points to score and point_value

block (defines the shape of a single block for food and snake)
    length, width, color

VISION and OTHER STUFF
functions:
open camera
identify tongue
identify movement of tongue
translate movements into game commands

classes:
scoreboard (displays score to player, possibly also high score)
'''

import pygame
from pygame.locals import *


class Window:
    """Represents the window that the game is played in.
    Attributes include board length and width.
    """
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 750, 750

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        food = Food()
        food.showBlock()
        pygame.display.update()
        keys=pygame.key.get_pressed()
        #got another rectangle to show up when key was pressed, but the other one doesnt go away
        #need to implement move function
        if keys[K_LEFT]:
            food.moveBlock(100,100)
            pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.on_init()
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class Block(pygame.Rect):
    """Represents the blocks that appear in the window and make up the food and
    the parts of the snake.
    """
    def __init__(self, height=100, width=100, x=0, y=0, color=(240, 240, 240)):
        pygame.Rect.__init__(self, x, y, width, height)
        self.color = color

    def showBlock(self):
        pygame.draw.rect(screen._display_surf, self.color, self)

    def moveBlock(self, dx, dy):
        pygame.Rect.move(dx, dy)


class Food(Block):
    """Represents the food that randomly appears in the window. Made up of randomly
    placed blocks.
    """
    def __init__(self, height=100, width=100, x=0, y=0, color=(240, 240, 240), point_value=10):
        Block.__init__(self, height, width, x, y, color)
        self.point_value = point_value

    def random_placement(self):
        pass


if __name__ == "__main__":
    screen = Window()
    screen.on_execute()
