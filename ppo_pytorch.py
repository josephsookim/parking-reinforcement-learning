import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical


class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_size=64):
        super(ActorCritic, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)

        self.actor = nn.Linear(hidden_size, action_dim)
        self.critic = nn.Linear(hidden_size, 1)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))

        policy = F.softmax(self.actor(x), dim=-1)
        value = self.critic(x)
        return policy, value


class PPOAgent:
    def __init__(self, state_dim, action_dim, lr_actor=0.001, lr_critic=0.001,
                 gamma=0.99, clip_ratio=0.2, entropy_coeff=0.01,
                 value_coeff=0.5, epochs=10, batch_size=32):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        self.gamma = gamma
        self.clip_ratio = clip_ratio
        self.entropy_coeff = entropy_coeff
        self.value_coeff = value_coeff
        self.epochs = epochs
        self.batch_size = batch_size

        self.actor_critic = ActorCritic(state_dim, action_dim)
        self.optimizer_actor = optim.Adam(
            self.actor_critic.actor.parameters(), lr=lr_actor)
        self.optimizer_critic = optim.Adam(
            self.actor_critic.critic.parameters(), lr=lr_critic)

    def get_action(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        policy, _ = self.actor_critic(state)
        dist = Categorical(policy)
        action = dist.sample()
        return action.item()

    def update(self, states, actions, rewards, dones, next_states):
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(-1)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)

        for _ in range(self.epochs):
            # Compute advantages and target values
            _, values = self.actor_critic(states)
            _, next_values = self.actor_critic(next_states)
            advantages = rewards + self.gamma * (1 - dones) * next_values - values

            # Normalize advantages
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

            # Update actor
            log_probs_old, _ = self.actor_critic(states)
            dist_old = Categorical(log_probs_old)
            log_probs_old = log_probs_old.gather(1, actions)
            ratios = (log_probs_old.exp() / dist_old.probs.exp()).clamp(0, 1)

            actor_loss = -torch.min(ratios * advantages,
                                    ratios.clamp(1 - self.clip_ratio,
                                                 1 + self.clip_ratio) * advantages).mean()

            self.optimizer_actor.zero_grad()
            actor_loss.backward()
            self.optimizer_actor.step()

            # Update critic
            _, values = self.actor_critic(states)
            critic_loss = F.mse_loss(values, rewards)

            self.optimizer_critic.zero_grad()
            critic_loss.backward()
            self.optimizer_critic.step()
