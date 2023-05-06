import pygame
from coord import Coord
from direction import Direction
from square import Square

class Snake(Square):
    def __init__(self, size, surface, color):
        super().__init__(0, 0, size)
        self.surface = surface
        self.color = color

        self.die_sound = pygame.mixer.Sound("./assets/lose.wav")
        self.eat_sound = pygame.mixer.Sound("./assets/eat.wav")
        self.cancel_sound = pygame.mixer.Sound("./assets/cancel.mp3")

        self.reset()

    def die(self):
        self.die_sound.play()
        self.reset()

    def eat(self):
        self.eat_sound.play()
        self.length = self.length + 1

        # add another block
        last_block = self.blocks[len(self.blocks) - 1]
        new_block_pos = Coord(last_block.x, last_block.y)
        self.blocks.append(new_block_pos) # will this work?

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
        # You can't move in the OPPOSITE direction to the direction you're currently facing
        if (self.direction == Direction.LEFT and direction == Direction.RIGHT):
            self.cancel_sound.play()
            return
        elif (self.direction == Direction.RIGHT and direction == Direction.LEFT):
            self.cancel_sound.play()
            return
        elif (self.direction == Direction.UP and direction == Direction.DOWN):
            self.cancel_sound.play()
            return
        elif (self.direction == Direction.DOWN and direction == Direction.UP):
            self.cancel_sound.play()
            return

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
    
    def eating_apple(self, apple):
        first_block = self.blocks[0]

        top_left_collision = self.did_collide(Coord(first_block.x, first_block.y), apple)
        top_right_collision = self.did_collide(Coord(first_block.x, first_block.y), apple)
        bottom_left_collision = self.did_collide(Coord(first_block.x, first_block.y), apple)
        bottom_right_collision = self.did_collide(Coord(first_block.x, first_block.y), apple)

        return top_left_collision or top_right_collision or bottom_left_collision or bottom_right_collision

    def did_collide(self, coord, apple):
        point_x = apple.x
        point_y = apple.y

        # We look for collisions between the apple and the snake instead? Since the apple is smaller?
        return (point_x > coord.x and point_x < coord.x + self.size) and (point_y > coord.y and point_y < coord.y + self.size)
