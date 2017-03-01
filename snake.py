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

class Window:
    """Represents the window that the game is played in.
    Attributes include board length and width.
    """

    def __init__(self,length=1000,width=1000):
        self.length = length
        self.width = width
        pass

    #use pygame to implement showing window

class Block:
    """Represents the blocks that appear in the window and make up the food and
    the parts of the snake.
    """
    def __init__(self, length = 10, width = 10, x, y, color):
        self.length = length
        self.width = width
        self.x = x
        self.y = y
        self.color = color
        pass

    def showBlock(self):
        pass

    def moveBlock(self, dx, dy):
        pass
    #use pygame again lol

class Food(Block):
    """Represents the food that randomly appears in the window. Made up of randomly
    placed blocks.
    """
    def __init__(self, color, point_value = 10):
        self.color = color
        self.point_value = point_value
        pass

    def random_placement(self):
        
