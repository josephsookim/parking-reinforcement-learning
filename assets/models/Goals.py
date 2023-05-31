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

    for i in range(200, 650, 50):
        goals.append(Goal(i + 15, 230, i + 35, 270))
        goals.append(Goal(i + 15, 330, i + 35, 370))
        goals.append(Goal(i + 15, 630, i + 35, 670))
        goals.append(Goal(i + 15, 730, i + 35, 770))

    for i in range(850, 1300, 50):
        goals.append(Goal(i + 15, 230, i + 35, 270))
        goals.append(Goal(i + 15, 330, i + 35, 370))
        goals.append(Goal(i + 15, 630, i + 35, 670))
        goals.append(Goal(i + 15, 730, i + 35, 770))

    return goals
