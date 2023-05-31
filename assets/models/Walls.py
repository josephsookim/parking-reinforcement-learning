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

    # Top Border
    walls.append(Wall(0, 0, 850, 0))

    # Right Border
    walls.append(Wall(1500, 0, 1500, 600))

    # Bottom Border
    walls.append(Wall(0, 600, 850, 600))

    # Left Border
    walls.append(Wall(0, 0, 0, 600))

    return walls
