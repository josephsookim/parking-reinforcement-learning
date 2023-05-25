import math


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
