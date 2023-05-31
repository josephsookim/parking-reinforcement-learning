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
    walls.append(Wall(200, 700, 650, 700))

    for i in range(200, 650 + 1, 50):
        # Top Side
        walls.append(Wall(i, 700, i, 600))

        # Bottom Side
        walls.append(Wall(i, 700, i, 800))

    # Lower Right Parking Lot
    walls.append(Wall(850, 700, 1300, 700))

    for i in range(850, 1300 + 1, 50):
        # Top Side
        walls.append(Wall(i, 700, i, 600))

        # Bottom Side
        walls.append(Wall(i, 700, i, 800))

    # Top Border
    walls.append(Wall(0, 0, 1500, 0))

    # Right Border
    walls.append(Wall(1500, 0, 1500, 1000))

    # Bottom Border
    walls.append(Wall(0, 1000, 1500, 1000))

    # Left Border
    walls.append(Wall(0, 0, 0, 1000))

    return walls
