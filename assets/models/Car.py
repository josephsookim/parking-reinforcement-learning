import math
import pygame

from assets.models.Point import Point
from assets.utils.helpers import rotate, rotateRect


class Car:
    def __init__(self, x: int, y: int):
        # Passed parameters
        self.x = x
        self.y = y

        # Hard coded variables
        self.width = 1
        self.height = 1
        self.points = 0
        self.dvel = 1
        self.vel = 0
        self.velX = 0
        self.velY = 0
        self.maxVel = 15
        self.angle = math.radians(180)
        self.soll_angle = self.angle

        # self.original_image = pygame.image.load("car.png").convert()
        # self.image = self.original_image  # This will reference the rotated image.
        # self.image.set_colorkey((0,0,0))
        # self.rect = self.image.get_rect().move(self.x, self.y)

    def action(self, choice: int):
        match choice:
            case 7:
                self.accelerate(self.dvel)
                self.turn(-1)

            case 8:
                self.accelerate(self.dvel)

            case 9:
                self.accelerate(self.dvel)
                self.turn(1)

            case 4:
                self.turn(-1)

            case 6:
                self.turn(1)

            case 1:
                self.accelerate(-self.dvel)
                self.turn(-1)

            case 2:
                self.accelerate(-self.dvel)

            case 3:
                self.accelerate(-self.dvel)
                self.turn(1)

            case _:
                pass

    def accelerate(self, dvel):
        dvel = dvel * 2

        self.vel = self.vel + dvel

        if self.vel > self.maxvel:
            self.vel = self.maxvel

        if self.vel < -self.maxvel:
            self.vel = -self.maxvel

    def turn(self, dir):
        self.soll_angle = self.soll_angle + dir * math.radians(15)

    def update(self):
        self.angle = self.soll_angle

        vec_temp = rotate(Point(0, 0), Point(0, self.vel), self.angle)
        self.velX, self.velY = vec_temp.x, vec_temp.y

        self.x = self.x + self.velX
        self.y = self.y + self.velY

        self.rect.center = self.x, self.y

        self.pt1 = Point(self.pt1.x + self.velX, self.pt1.y + self.velY)
        self.pt2 = Point(self.pt2.x + self.velX, self.pt2.y + self.velY)
        self.pt3 = Point(self.pt3.x + self.velX, self.pt3.y + self.velY)
        self.pt4 = Point(self.pt4.x + self.velX, self.pt4.y + self.velY)

        self.p1, self.p2, self.p3, self.p4 = rotateRect(
            self.pt1, self.pt2, self.pt3, self.pt4, self.soll_angle)

        self.image = pygame.transform.rotate(
            self.original_image, 90 - self.soll_angle * 180 / math.pi)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)
