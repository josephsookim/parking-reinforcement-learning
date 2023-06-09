import math
import pygame

from assets.models.Point import Point
from assets.models.Line import Line
from assets.models.Ray import Ray
from assets.utils.helpers import rotate, rotateRect, distance

# CONSTANTS
GOALREWARD = 10


class Car:
    def __init__(self, x: int, y: int, goal_pt: Point):
        # Passed parameters
        self.pt = Point(x, y)
        self.x = x
        self.y = y
        self.goal_pt = goal_pt

        # Hard coded variables
        self.width = 1
        self.height = 1
        self.points = 0
        self.dvel = 2
        self.vel = 5
        self.velX = 0
        self.velY = 0
        self.maxvel = 10
        self.angle = math.radians(-90)
        self.soll_angle = self.angle

        self.angle_change = 0

        self.original_image = pygame.image.load('assets/img/car.png').convert()
        # This will reference the rotated image.
        self.image = self.original_image
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect().move(self.x, self.y)

        self.pt1 = Point(self.pt.x - self.width / 2,
                         self.pt.y - self.height / 2)
        self.pt2 = Point(self.pt.x + self.width / 2,
                         self.pt.y - self.height / 2)
        self.pt3 = Point(self.pt.x + self.width / 2,
                         self.pt.y + self.height / 2)
        self.pt4 = Point(self.pt.x - self.width / 2,
                         self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

        self.distances = []

    def action(self, choice: int):
        if choice == 4:
            self.turn(-1)
            self.angle_change -= 15
        elif choice == 6:
            self.turn(1)
            self.angle_change += 15
        else:
            pass
        '''
        elif choice == 8:
            self.accelerate(self.dvel)
        elif choice == 2:
            self.accelerate(-self.dvel)
        '''


    def accelerate(self, dvel):
        self.vel += dvel

        if self.vel > self.maxvel:
            self.vel = self.maxvel

        if self.vel < 2:
            self.vel = 2

    def turn(self, dir):
        self.soll_angle = self.soll_angle + dir * math.radians(15)

    def update(self):
        self.angle = self.soll_angle

        vec_temp = rotate(Point(0, 0), Point(0, self.vel), self.angle)
        self.velX, self.velY = vec_temp.x, vec_temp.y

        self.x = self.x + self.velX
        self.y = self.y + self.velY
        self.pt = Point(self.x, self.y)

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

    def cast(self, walls):
        self.rays = []

        for i in range(0, 8):
            self.rays.append(
                Ray(self.x, self.y, self.soll_angle + math.radians(45) * i))

        observations = []
        self.closestRays = []
        max_distance = 0  # Initialize the maximum distance

        for ray in self.rays:
            closest = None  # myPoint(0,0)
            record = math.inf
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    dist = distance(Point(self.x, self.y), pt)
                    if dist < record:
                        record = dist
                        closest = pt
            if closest:
                # append distance for current ray
                self.closestRays.append(closest)
                observations.append(record)
                if record > max_distance:
                    max_distance = record
            else:
                observations.append(1000)

        for i in range(len(observations)):
            # invert observation values 0 is far away 1 is close
            observations[i] = ((max_distance - observations[i]) / max_distance)

        observations.append(self.x)
        observations.append(self.y)
        observations.append(self.angle)
        observations.append(distance(self.pt, self.goal_pt))

        return observations

    def collision(self, wall):
        lines = [Line(self.p1, self.p2), Line(self.p2, self.p3),
                 Line(self.p3, self.p4), Line(self.p4, self.p1)]

        x1 = wall.x1 - 10
        y1 = wall.y1 - 10
        x2 = wall.x2 + 10
        y2 = wall.y2 + 10

        for line in lines:
            x3 = line.pt1.x - 10
            y3 = line.pt1.y - 10
            x4 = line.pt2.x + 10
            y4 = line.pt2.y + 10

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if denom != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

                if 0 < t < 1 and 0 < u < 1:
                    return True

        return False

    def score(self, goal):
        line1 = Line(self.p1, self.p3)

        vec = rotate(Point(0, 0), Point(0, -50), self.angle)
        line1 = Line(Point(self.x, self.y), Point(
            self.x + vec.x, self.y + vec.y))

        x1 = goal.x1 - 30
        y1 = goal.y1 - 20
        x2 = goal.x2 + 30
        y2 = goal.y2 + 20

        x3 = line1.pt1.x - 5
        y3 = line1.pt1.y - 5
        x4 = line1.pt2.x + 5
        y4 = line1.pt2.y + 5

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if (den == 0):
            den = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = math.floor(x1 + t * (x2 - x1)
                                ), math.floor(y1 + t * (y2 - y1))

                d = distance(Point(self.x, self.y), Point(pt[0], pt[1]))
                if d < 20:
                    # pygame.draw.circle(win, (0,255,0), pt, 5)
                    self.points += GOALREWARD
                    return (True)

        return (False)

    def reset(self):
        self.x = 50
        self.y = 300
        self.velX = 0
        self.velY = 0
        self.vel = 0
        self.angle = math.radians(180)
        self.soll_angle = self.angle
        self.points = 0

        self.pt1 = Point(self.pt.x - self.width / 2,
                         self.pt.y - self.height / 2)
        self.pt2 = Point(self.pt.x + self.width / 2,
                         self.pt.y - self.height / 2)
        self.pt3 = Point(self.pt.x + self.width / 2,
                         self.pt.y + self.height / 2)
        self.pt4 = Point(self.pt.x - self.width / 2,
                         self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

    def draw(self, win):
        win.blit(self.image, self.rect)
