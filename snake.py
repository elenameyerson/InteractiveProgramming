'''
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

classe:
scoreboard (displays score to player, possibly also high score)
'''
