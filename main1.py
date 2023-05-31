from assets import ParkingEnv

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
game.fps = 60

GameTime = 0
GameHistory = []
renderFlag = True

ppo_agent = PPO(state_dim=19, action_dim=game.action_space.n, lr_actor=0.01, lr_critic=0.01, gamma=0.99, K_epochs=10, eps_clip=0.2, has_continuous_action_space=False, action_std_init=0.6)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
# ppo_agent.load(checkpoint_path)

ppo_scores = []
eps_history = []


def run():
    for e in range(N_EPISODES):
        game.reset()  # reset env

        done = False
        score = 0
        counter = 0

        observation_, reward, done = game.step(0)
        observation = np.array(observation_)

        gtime = 0  # set game time back to 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            action = ppo_agent.select_action(observation)
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)

            # This is a countdown if no reward is collected the car will be done within 100 ticks
            '''
            if reward <= 0:
                counter += 1
                if counter > 100:
                    done = True
            else:
                counter = 0
            '''

            score += reward

            ppo_agent.buffer.rewards.append(reward)
            ppo_agent.buffer.is_terminals.append(done)

            observation = observation_

            gtime += 1

            if gtime >= TOTAL_GAMETIME:
                done = True

            if renderFlag:
                game.render()

        ppo_agent.update()

        eps_history.append(0.0)
        ppo_scores.append(score)
        avg_score = np.mean(ppo_scores[max(0, e-100):(e+1)])

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ppo_agent.policy_old.load_state_dict(ppo_agent.policy.state_dict())

        if e % 10 == 0 and e > 10:
            ppo_agent.save('model.h5')
            print("Saved model")

        print('episode: ', e, 'score: %.2f' % score,
              'average score %.2f' % avg_score,
              'memory size', len(ppo_agent.buffer.rewards))


run()
