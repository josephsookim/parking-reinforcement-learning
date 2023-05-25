import pygame

from models.Car import Car


class ParkingEnv:
    def __init__(self):
        pygame.init()

        self.fps = 120
        self.width = 1000
        self.height = 600

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("RACING DQN")
        self.screen.fill((0, 0, 0))
        self.back_image = pygame.image.load("track.png").convert()
        self.back_rect = self.back_image.get_rect().move(0, 0)
        self.action_space = None
        self.observation_space = None
        self.game_reward = 0
        self.score = 0
        self.reset()

        def reset(self):
            # self.screen.fill((0, 0, 0))
            self.car = Car(50, 300)
            # self.walls = getWalls()
            # self.goals = getGoals()
            self.game_reward = 0

        def step(self, action):
            pass

        def render(self, action):
            pass

        def close():
            pygame.quit()
