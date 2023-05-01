import pygame

class Grid:
    def __init__(self, size, surface, color):
        self.size = size
        self.surface = surface
        self.color = color

    def draw(self):
        total_height = self.surface.get_height()
        total_width = self.surface.get_width()

        x = self.size
        y = self.size

        while y < total_height:
            pygame.draw.aaline(self.surface, self.color, (0, y), (total_width, y))
            y = y + self.size

        while x < total_width:
            pygame.draw.aaline(self.surface, self.color, (x, 0), (x, total_height))
            x = x + self.size