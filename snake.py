import pygame
from enum import Enum

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Snake:
    def __init__(self, size, surface, color):
        self.size = size
        self.surface = surface
        self.color = color
        self.die_sound = pygame.mixer.Sound("./assets/lose.wav")

        self.reset()

    def die(self):
        self.die_sound.play()
        self.reset()

    def reset(self):
        self.length = 5
        self.direction = Direction.RIGHT
        
        start_x = (self.length * self.size) + self.size
        start_y = self.surface.get_height() / 2 # todo: round this to the closest 50

        # position the blocks
        self.blocks = [Coord(start_x, start_y)]
        current_block = 1
        while current_block < self.length:
            new_x = self.blocks[current_block - 1].x - self.size
            self.blocks.append(Coord(new_x, start_y))
            current_block = current_block + 1

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        first_block = self.blocks[0]
        prev_pos = Coord(first_block.x, first_block.y)
        
        if self.direction == Direction.LEFT:
            first_block.x -= self.size
        elif self.direction == Direction.RIGHT:
            first_block.x += self.size
        elif self.direction == Direction.UP:
            first_block.y -= self.size
        elif self.direction == Direction.DOWN:
            first_block.y += self.size
        else:
            raise Exception(f"Direction {self.direction} not supported.")
        
        #todo: each block after the first block needs to be set to the co-ords of the block after it
        current_block_index = 1

        while current_block_index < len(self.blocks):
            prev_pos = self.move_block(self.blocks[current_block_index], prev_pos)
            current_block_index = current_block_index + 1
        
    def move_block(self, block, new_pos):
        prev_pos = Coord(block.x, block.y)

        block.x = new_pos.x
        block.y = new_pos.y

        return prev_pos

    def draw(self):            
        #pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.size, self.size))
        
        blocks_drawn = 0
        while blocks_drawn < len(self.blocks):
            current_block = self.blocks[blocks_drawn]
            pygame.draw.rect(self.surface, self.color, (current_block.x, current_block.y, self.size, self.size))
            blocks_drawn += 1

    def out_of_bounds(self):
        first_block = self.blocks[0]

        return (first_block.x < 0 or
                first_block.y < 0 or
                first_block.x + self.size > self.surface.get_width() or
                first_block.y + self.size > self.surface.get_height())