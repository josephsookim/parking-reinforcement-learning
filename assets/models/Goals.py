import pygame


class Goal:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.active = False

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x1, self.y1,
                         self.x2 - self.x1, self.y2 - self.y1))
        if self.active:
            pygame.draw.rect(win, (0, 255, 0), (self.x1, self.y1,
                             self.x2 - self.x1, self.y2 - self.y1))


def getGoals():
    goals = []

    for i in range(200, 650, 50):
        goals.append(Goal(i + 20, 240, i + 30, 260))
        goals.append(Goal(i + 20, 340, i + 30, 360))
        goals.append(Goal(i + 20, 640, i + 30, 660))
        goals.append(Goal(i + 20, 740, i + 30, 760))

    for i in range(850, 1300, 50):
        goals.append(Goal(i + 20, 240, i + 30, 260))
        goals.append(Goal(i + 20, 340, i + 30, 360))
        goals.append(Goal(i + 20, 640, i + 30, 660))
        goals.append(Goal(i + 20, 740, i + 30, 760))

    return goals
