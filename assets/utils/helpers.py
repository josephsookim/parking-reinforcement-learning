import math

from assets.models.Point import Point


def rotate(origin, point, angle):
    qx = origin.x + math.cos(angle) * (point.x - origin.x) - \
        math.sin(angle) * (point.y - origin.y)
    qy = origin.y + math.sin(angle) * (point.x - origin.x) + \
        math.cos(angle) * (point.y - origin.y)
    q = Point(qx, qy)
    return q


def rotateRect(pt1, pt2, pt3, pt4, angle):

    pt_center = Point((pt1.x + pt3.x)/2, (pt1.y + pt3.y)/2)

    pt1 = rotate(pt_center, pt1, angle)
    pt2 = rotate(pt_center, pt2, angle)
    pt3 = rotate(pt_center, pt3, angle)
    pt4 = rotate(pt_center, pt4, angle)

    return pt1, pt2, pt3, pt4
