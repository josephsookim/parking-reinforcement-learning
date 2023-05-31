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
        self.vel = 2
        self.velX = 0
        self.velY = 0
        self.maxvel = 4
        self.angle = math.radians(0)
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
        match choice:
            case 8:
                self.accelerate(self.dvel)

            case 4:
                self.turn(-1)
                self.angle_change -= 15

            case 6:
                self.turn(1)
                self.angle_change += 15

            case 2:
                self.accelerate(-self.dvel)

            case _:
                pass

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

        ray1 = Ray(self.x, self.y, self.soll_angle)
        ray2 = Ray(self.x, self.y, self.soll_angle - math.radians(30))
        ray3 = Ray(self.x, self.y, self.soll_angle + math.radians(30))
        ray4 = Ray(self.x, self.y, self.soll_angle + math.radians(45))
        ray5 = Ray(self.x, self.y, self.soll_angle - math.radians(45))
        ray6 = Ray(self.x, self.y, self.soll_angle + math.radians(90))
        ray7 = Ray(self.x, self.y, self.soll_angle - math.radians(90))
        ray8 = Ray(self.x, self.y, self.soll_angle + math.radians(180))

        ray9 = Ray(self.x, self.y, self.soll_angle + math.radians(10))
        ray10 = Ray(self.x, self.y, self.soll_angle - math.radians(10))
        ray11 = Ray(self.x, self.y, self.soll_angle + math.radians(135))
        ray12 = Ray(self.x, self.y, self.soll_angle - math.radians(135))
        ray13 = Ray(self.x, self.y, self.soll_angle + math.radians(20))
        ray14 = Ray(self.x, self.y, self.soll_angle - math.radians(20))

        ray15 = Ray(self.p1.x, self.p1.y, self.soll_angle + math.radians(90))
        ray16 = Ray(self.p2.x, self.p2.y, self.soll_angle - math.radians(90))

        ray17 = Ray(self.p1.x, self.p1.y, self.soll_angle + math.radians(0))
        ray18 = Ray(self.p2.x, self.p2.y, self.soll_angle - math.radians(0))

        self.rays = []
        self.rays.append(ray1)
        self.rays.append(ray2)
        self.rays.append(ray3)
        self.rays.append(ray4)
        self.rays.append(ray5)
        self.rays.append(ray6)
        self.rays.append(ray7)
        self.rays.append(ray8)

        self.rays.append(ray9)
        self.rays.append(ray10)
        self.rays.append(ray11)
        self.rays.append(ray12)
        self.rays.append(ray13)
        self.rays.append(ray14)

        self.rays.append(ray15)
        self.rays.append(ray16)

        self.rays.append(ray17)
        self.rays.append(ray18)

        observations = []
        self.closestRays = []

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

            else:
                observations.append(1000)

        for i in range(len(observations)):
            # invert observation values 0 is far away 1 is close
            observations[i] = ((1000 - observations[i]) / 1000)

        observations.append(self.vel / self.maxvel)
        observations.append(self.x)
        observations.append(self.y)
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

        x1 = goal.x1 - 5
        y1 = goal.y1 - 5
        x2 = goal.x2 + 5
        y2 = goal.y2 + 5

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
