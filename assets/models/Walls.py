import pygame

# CONSTANT
WHITE = (255, 255, 255)


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def draw(self, window):
        pygame.draw.line(window, WHITE, (self.x1, self.y1),
                         (self.x2, self.y2), 5)


def getWalls():
    walls = []

    wall1 = Wall(12, 451, 15, 130)
    walls.append(wall1)

    return walls
