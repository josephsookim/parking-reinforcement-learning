from assets import ParkingEnv
from assets.utils.helpers import distance
from ppo_pytorch import PPO

import pygame
import numpy as np
from collections import deque
import random
import math
import torch

import matplotlib.pyplot as plt

TOTAL_GAMETIME = 1000  # Max game time for one episode
N_EPISODES = 100000
REPLACE_TARGET = 50

episodes = []
rewards = []
hit_rates = []

# Create a figure and axis for plotting
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Reward')
line2, = ax.plot([], [], label='Loss')

# Customize the plot
ax.set_xlabel('Epoch')
ax.set_ylabel('Average Reward')


def update_plot(episode, reward, hit_rate):
    episodes.append(episode)
    rewards.append(reward)
    hit_rates.append(hit_rate)

    line1.set_data(episodes, rewards)
    line2.set_data(episodes, hit_rates)
    ax.relim()
    ax.autoscale_view()
    plt.draw()


game = ParkingEnv.ParkingEnv()
game.fps = 30

GameTime = 0
GameHistory = []
renderFlag = False

ppo_agent = PPO(state_dim=12, action_dim=game.action_space.n, lr_actor=0.0003, lr_critic=0.0003,
                gamma=0.99, K_epochs=80, eps_clip=0.2, has_continuous_action_space=False, action_std_init=0.6)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten

continue_train = False
if continue_train:
    ppo_agent.load('model.h5')
    print('model loaded')

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
        avg_score = np.mean(ppo_scores[max(0, e-100):(e+1)])

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ppo_agent.policy_old.load_state_dict(ppo_agent.policy.state_dict())

        if e % 10 == 0 and e > 10:
            ppo_agent.save('model.h5')
            print("Saved model")

        print(f'episode {e}: {score}')
        print(f'hit rate: {hit_count / (e+1) * 100}% | {hit_count} / {e+1}')
        print('----')

        update_plot(e, score, hit_count)


run()
