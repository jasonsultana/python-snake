from coord import Coord

class Square(Coord):
    def __init__(self, x, y, size):
        super().__init__(x, y)
        self.size = size