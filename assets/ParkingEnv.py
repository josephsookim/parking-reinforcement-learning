import pygame

from assets.models.Car import Car
from assets.models.Ray import Ray
from assets.models.Walls import Wall, getWalls

# CONSTANTS
DRAW_WALLS = True
DRAW_GOALS = False
DRAW_RAYS = False


class ParkingEnv:
    def __init__(self):
        pygame.init()

        self.fps = 120
        self.width = 1500
        self.height = 1000

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Parking PPO")
        # self.back_image = pygame.image.load("track.png").convert()
        # self.back_rect = self.back_image.get_rect().move(0, 0)
        self.action_space = None
        self.observation_space = None
        self.score = 0

        self.walls = getWalls()
        print(self.walls)
        self.reset()

    def reset(self):
        self.screen.fill((0, 0, 0))
        self.car = Car(50, 300)
        # self.goals = getGoals()
        self.game_reward = 0

    def step(self, action):
        pass

    def render(self, action):
        pygame.time.delay(10)

        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

        # self.screen.blit(self.back_image, self.back_rect)

        if DRAW_WALLS:
            for wall in self.walls:
                print('done')
                wall.draw(self.screen)

        self.clock.tick(self.fps)
        pygame.display.update()

    def close():
        pygame.quit()
