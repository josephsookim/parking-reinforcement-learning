import pygame

from assets.models.Car import Car
from assets.models.Ray import Ray
from assets.models.Walls import Wall, getWalls
from assets.models.Goals import Goal, getGoals

# CONSTANTS
DRAW_WALLS = True
DRAW_GOALS = True
DRAW_RAYS = True

GOALREWARD = 10


class ParkingEnv:
    def __init__(self):
        pygame.init()

        self.fps = 120
        self.width = 1500
        self.height = 1000

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Parking PPO')
        self.action_space = None
        self.observation_space = None
        self.score = 0

        self.walls = getWalls()
        self.reset()

    def reset(self):
        self.screen.fill((0, 0, 0))
        self.car = Car(50, 300)
        self.goals = getGoals()
        self.game_reward = 0

    def step(self, action):
        done = False
        self.car.action(action)
        self.car.update()
        reward = 0
        # reward = LIFE_REWARD

        for goal in self.goals:
            if goal.active:
                if self.car.score(goal):
                    reward += GOALREWARD
                    done = True

        # check if car crashed in the wall
        for wall in self.walls:
            if self.car.collision(wall):
                # reward += PENALTY
                done = True

        new_state = self.car.cast(self.walls)
        # normalize states
        if done:
            new_state = None

        return new_state, reward, done

    def render(self, action):
        pygame.time.delay(10)

        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

        # self.screen.blit(self.back_image, self.back_rect)

        if DRAW_WALLS:
            for wall in self.walls:
                wall.draw(self.screen)

        if DRAW_GOALS:
            for goal in self.goals:
                goal.draw(self.screen)
                if goal.active:
                    goal.draw(self.screen)

        self.car.draw(self.screen)

        if DRAW_RAYS:
            i = 0
            for pt in self.car.closestRays:
                pygame.draw.circle(self.screen, (0, 255, 0), (pt.x, pt.y), 5)
                i += 1
                if i < 15:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (self.car.x, self.car.y), (pt.x, pt.y), 1)
                elif i >= 15 and i < 17:
                    pygame.draw.line(self.screen, (255, 255, 255), ((
                        self.car.p1.x + self.car.p2.x)/2, (self.car.p1.y + self.car.p2.y)/2), (pt.x, pt.y), 1)
                elif i == 17:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (self.car.p1.x, self.car.p1.y), (pt.x, pt.y), 1)
                else:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                     (self.car.p2.x, self.car.p2.y), (pt.x, pt.y), 1)

        self.clock.tick(self.fps)
        pygame.display.update()

    def close():
        pygame.quit()
