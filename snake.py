import pygame
from coord import Coord
from direction import Direction
from square import Square

class Snake(Square):
    # Initialisation
    def __init__(self, size, surface, color):
        super().__init__(0, 0, size)

        self.surface = surface
        self.color = color

        self.die_sound = pygame.mixer.Sound("./assets/lose.wav")
        self.eat_sound = pygame.mixer.Sound("./assets/eat.wav")
        self.cancel_sound = pygame.mixer.Sound("./assets/cancel.mp3")

        self.reset()

    def reset(self):
        self.length = 5
        self.direction = Direction.RIGHT
        
        start_x = (self.length * self.size) + self.size
        start_y = self.surface.get_height() / 2 # todo: round this to the closest 50

        # position the blocks
        self.blocks = [Square(start_x, start_y, self.size)]
        current_block = 1
        while current_block < self.length:
            new_x = self.blocks[current_block - 1].x - self.size
            self.blocks.append(Square(new_x, start_y, self.size))
            current_block = current_block + 1

    # Movement
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
    
    # -- Collision detection --
    # Eating apple
    def eating_apple(self, apple):
        first_block = self.blocks[0]

        square = Square(first_block.x, first_block.y, self.size)

        collision = self.did_collide(square, apple)
        return collision
    
    def eat(self):
        self.eat_sound.play()
        self.length = self.length + 1

        # add another block
        last_block = self.blocks[len(self.blocks) - 1]
        new_block_pos = Square(last_block.x, last_block.y, self.size)
        self.blocks.append(new_block_pos)

    # Game over conditions
    def out_of_bounds(self):
        first_block = self.blocks[0]

        return (first_block.x < 0 or
                first_block.y < 0 or
                first_block.x + self.size > self.surface.get_width() or
                first_block.y + self.size > self.surface.get_height())
    
    def eating_self(self):
        # Did the center of the first block collide with any "other" block
        # We use the center since the edges are always touching
        first_block = self.blocks[0]
        first_block_center = Coord(first_block.x + (first_block.size / 2), first_block.y + (first_block.size / 2))
        for block in self.blocks[1:]:
            if (self.did_collide(block, first_block_center)):
                return True
            
        return False    

    def die(self, reason):
        print(f"You died! Reason: {reason}")
        self.die_sound.play()
        self.reset()

    def did_collide(self, square, collider):
        point_x = collider.x
        point_y = collider.y

        return (point_x >= square.x and point_x <= square.x + square.size) and (point_y >= square.y and point_y <= square.y + square.size)
