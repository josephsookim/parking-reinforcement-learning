import pygame


class Goal:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.active = False

    def draw(self, win):
        pygame.draw.line(win, (0, 255, 0), (self.x1, self.y1),
                         (self.x2, self.y2), 2)
        if self.isactiv:
            pygame.draw.line(win, (255, 0, 0),
                             (self.x1, self.y1), (self.x2, self.y2), 2)
