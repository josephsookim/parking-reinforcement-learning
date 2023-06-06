from assets import ParkingEnv
from assets.utils.helpers import distance
from dqn import DQN

import pygame
import numpy as np

import matplotlib.pyplot as plt

TOTAL_GAMETIME = 1000  # Max game time for one episode
N_EPISODES = 100000
REPLACE_TARGET = 50

episodes = []
rewards = []
hit_counts = []

game = ParkingEnv.ParkingEnv()
game.fps = 60

GameTime = 0
GameHistory = []
renderFlag = False

dqn_agent = DQN(state_dim=12, action_dim=game.action_space.n, lr=0.0001, gamma=0.99, batch_size=64)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten

continue_train = False
if continue_train:
    dqn_agent.load('dqn_model.h5')
    print('model loaded')

dqn_scores = []

def update_plot(episode, reward, hits):
    episodes.append(episode)
    rewards.append(reward)
    hit_counts.append(hits)

    plt.figure(1)
    plt.clf()
    plt.plot(episodes, rewards, label='Reward')
    plt.plot(episodes, hit_counts, label='Hits')
    plt.xlabel('Epoch')
    plt.ylabel('Average Reward')
    plt.legend()
    plt.pause(0.001)


def run_game():
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

            action = dqn_agent.select_action(observation)
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)

            if game.madeGoal:
                hit_count += 1

            score += reward

            dqn_agent.remember(observation, action, reward, observation_, done)

            observation = observation_

            if renderFlag:
                game.render()

        dqn_agent.learn()

        dqn_scores.append(score)
        avg_score = np.mean(dqn_scores[max(0, e - 100):(e + 1)])

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            dqn_agent.update_network_parameters()

        if e % 1000 == 0 and e > 10:
            dqn_agent.save('dqn_model.h5')
            print("Saved model")

        hit_rate = hit_count / (e+1) * 100
        print(f'episode {e}: {score}')
        print(f'hit rate: {hit_rate}% | {hit_count} / {e+1}')
        print('----')

        if e % 10 == 0:
            update_plot(e, score, hit_count)

        plt.pause(0.001)


# Initialize the plot
plt.ion()
plt.show()

# Run the game loop and matplotlib plot updates on the main thread
run_game()
plt.savefig("dqn.png")
