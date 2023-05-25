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

    # Upper Left Parking Lot
    walls.append(Wall(200, 300, 650, 300))

    for i in range(200, 650 + 1, 50):
        # Top Side
        walls.append(Wall(i, 300, i, 200))

        # Bottom Side
        walls.append(Wall(i, 300, i, 400))

    # Upper Right Parking Lot
    walls.append(Wall(850, 300, 1300, 300))

    for i in range(850, 1300 + 1, 50):
        # Top Side
        walls.append(Wall(i, 300, i, 200))

        # Bottom Side
        walls.append(Wall(i, 300, i, 400))

    # Lower Left Parking Lot

    # Lower Right Parking Lot

    return walls
