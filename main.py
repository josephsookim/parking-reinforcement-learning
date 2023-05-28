from assets import ParkingEnv
import pygame

game = ParkingEnv.ParkingEnv()
game.fps = 60


def run():
    game.reset()

    done = False

    while not done:

        action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                action = event.key - 1073741913 + 1
                print(action)

        observation_, reward, done = game.step(action)
        game.render('bruh')


run()
