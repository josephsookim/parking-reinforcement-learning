import pygame
from assets.models.Point import Point


class Goal:
    def __init__(self, x1, y1, x2, y2):
        self.pt = Point((x1 + x2) / 2, (y1 + y2) / 2)
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.active = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x1, self.y1,
                         self.x2 - self.x1, self.y2 - self.y1))
        if self.active:
            pygame.draw.rect(win, (0, 255, 0), (self.x1, self.y1,
                             self.x2 - self.x1, self.y2 - self.y1))


def getGoals():
    goals = []

    for i in range(200, 600, 100):
        goals.append(Goal(i + 30, 220, i + 70, 280))
        goals.append(Goal(i + 30, 320, i + 70, 380))

    print(len(goals))

    return goals
