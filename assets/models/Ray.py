import math

from assets.models.Point import Point
from assets.utils.helpers import rotate

class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def cast(self, wall):
        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        vec = rotate(Point(0, 0), Point(0, -1000), self.angle)

        x3 = self.x
        y3 = self.y
        x4 = self.x + vec.x
        y4 = self.y + vec.y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if (denom == 0):
            denom = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = Point(math.floor(x1 + t * (x2 - x1)),
                           math.floor(y1 + t * (y2 - y1)))

                # intersection point
                return (pt)
