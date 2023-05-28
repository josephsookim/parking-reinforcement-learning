from assets import ParkingEnv
import pygame

game = ParkingEnv.ParkingEnv()
game.fps = 60


def run():
    game.reset()

    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        game.render()


run()
