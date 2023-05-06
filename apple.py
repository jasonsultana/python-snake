import pygame
import random
from square import Square

class Apple(Square):
    def __init__(self, size, grid_size, surface, color):
        super().__init__(0, 0, size)

        self.grid_size = grid_size
        self.surface = surface
        self.color = color
        self.reset()

    def reset(self):
        max_x = self.surface.get_width() - self.size
        max_y = self.surface.get_height() - self.size

        buffer = (self.grid_size - self.size) / 2 # divide by 2 since the buffer will be on both the top and bottom, left and right side
        self.x = self.round_to(random.randint(0, max_x), self.grid_size) + buffer
        self.y = self.round_to(random.randint(0, max_y), self.grid_size) + buffer

        print(f"Apple x: {self.x}, Apple y: {self.y}")

    def draw(self):            
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.size, self.size))

    def round_to(self, x, base = 5):
        return base * round(x/base)