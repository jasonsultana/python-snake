import pygame
import random
from square import Square

class Apple(Square):
    def __init__(self, size, surface, color):
        super().__init__(0, 0, size)

        self.surface = surface
        self.color = color
        self.reset()

    def reset(self):
        max_x = self.surface.get_width() - self.size
        max_y = self.surface.get_height() - self.size

        self.x = self.round_to(random.randint(0, max_x), 50) + 12.5
        self.y = self.round_to(random.randint(0, max_y), 50) + 12.5

        print(f"Apple x: {self.x}, Apple y: {self.y}")

    def draw(self):            
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.size, self.size))

    def round_to(self, x, base = 5):
        return base * round(x/base)