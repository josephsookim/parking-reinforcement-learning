from assets import ParkingEnv
from assets.utils.helpers import distance

import pygame
import numpy as np
from collections import deque
import random
import math
import torch

from ppo_pytorch import PPO

TOTAL_GAMETIME = 1000  # Max game time for one episode
N_EPISODES = 10000
REPLACE_TARGET = 50

game = ParkingEnv.ParkingEnv()
game.fps = 30

GameTime = 0
GameHistory = []
renderFlag = True

ppo_agent = PPO(state_dim=13, action_dim=game.action_space.n, lr_actor=0.0001, lr_critic=0.0001, gamma=0.99, K_epochs=20, eps_clip=0.2, has_continuous_action_space=False, action_std_init=0.6)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
#ppo_agent.load('model.h5')

ppo_scores = []


def run():
    hit_count = 0
    for e in range(N_EPISODES):
        game.reset()  # reset env

        done = False
        score = 0

        observation_, reward, done = game.step(0)
        observation = np.array(observation_)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            action = ppo_agent.select_action(observation)
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)

            if done:
                # distance reward
                current_distance = distance(game.car.pt, game.goal.pt)
                normalized_distance = current_distance / game.max_distance

                reward += (1 - normalized_distance)

            if game.madeGoal:
                hit_count += 1

            score += reward

            ppo_agent.buffer.rewards.append(reward)
            ppo_agent.buffer.is_terminals.append(done)

            observation = observation_

            if renderFlag:
                game.render()

        ppo_agent.update()

        ppo_scores.append(score)

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ppo_agent.policy_old.load_state_dict(ppo_agent.policy.state_dict())

        if e % 100 == 0 and e > 10:
            ppo_agent.save('model.h5')
            print("Saved model")

        print(f'episode {e}: {score}')
        print(f'hit rate: {hit_count / (e+1)}% | {hit_count} / {e+1}')
        print('----')


run()
