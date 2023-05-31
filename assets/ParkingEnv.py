import pygame
import gym
import random

from assets.models.Car import Car
from assets.models.Ray import Ray
from assets.models.Walls import Wall, getWalls
from assets.models.Goals import Goal, getGoals
from assets.utils.helpers import distance

# CONSTANTS
DRAW_WALLS = True
DRAW_GOALS = True
DRAW_RAYS = True

GOAL_REWARD = 3
TIME_REWARD = -1
CRASH_REWARD = -1
SPIN_PENALTY = -2
MAX_STEPS = 256
MAX_GAMETIME = 1000


class ParkingEnv:
    def __init__(self):
        pygame.init()

        self.fps = 30
        self.width = 800
        self.height = 600

        self.steps = 0

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Parking PPO')
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = None
        self.score = 0

        self.walls = getWalls()
        self.goals = getGoals()

    def reset(self):
        self.screen.fill((0, 0, 0))
        self.goal = self.goals[0]
        #self.goal = self.goals[random.randint(0, 7)]
        self.car = Car(50, 300, self.goal.pt)
        self.goal.active = True
        self.game_reward = 0
        self.max_distance = distance(self.car.pt, self.goal.pt)
        self.madeGoal = False

    def step(self, action):
        done = False

        action_mapping = {
            0: 4,
            1: 6,
        }

        key = action_mapping[action]

        self.car.action(key)
        self.car.update()
        reward = 0

        if self.car.score(self.goal):
            reward += GOAL_REWARD
            self.madeGoal = True
            print('GOAL')
            done = True

        # check if car crashed in the wall
        for wall in self.walls:
            if self.car.collision(wall):
                reward += CRASH_REWARD
                done = True

        # time limit penalty
        if self.steps == MAX_STEPS:
            reward += TIME_REWARD

        if self.steps > MAX_GAMETIME:
            done = True

        self.steps += 1

        # spin penalty
        if abs(self.car.angle_change) >= 135 and self.car.angle_change != 0:
            reward += SPIN_PENALTY
            done = True

        new_state = self.car.cast(self.walls)

        if done:
            self.goal.active = False
            new_state = None

        return new_state, reward, done

    def render(self):
        pygame.time.delay(10)

        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

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
