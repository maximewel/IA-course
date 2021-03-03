import gym
import numpy as np
import math
from collections import deque
import random

class CartPole():
    def __init__(self, buckets=(1, 1, 6, 12,), n_episodes=1000, n_win_ticks=195, min_alpha=0.1, min_epsilon=0.1, gamma=1.0, ada_divisor=25, max_env_steps=None, monitor=False):
        self.buckets = buckets # down-scaling feature space to discrete range
        # NOTE: buckets=(1, 1, 6, 12,) means that the first 2 observations are not used, the third is discretized on 6 values and the third on 12
        self.n_episodes = n_episodes # training episodes
        self.n_win_ticks = n_win_ticks # average ticks over 100 episodes required for win
        self.min_alpha = min_alpha # learning rate
        self.min_epsilon = min_epsilon # exploration rate
        self.gamma = gamma # discount factor
        self.ada_divisor = ada_divisor # only for development purposes

        self.env = gym.make('CartPole-v0')
        if max_env_steps is not None: self.env._max_episode_steps = max_env_steps
        if monitor: self.env = gym.wrappers.Monitor(self.env, 'tmp/cartpole-1', force=True) # record results for upload

        # initialising Q-table
        self.Q = np.zeros(self.buckets + (self.env.action_space.n,)) # change the '1'
        # TODO 1: select the right size of the Q table - before start implementing read and understand the discretize method
        # you will use the following code to access the table
        # self.Q[state][action]
        # ex. self.Q[(0, 0, 1, 1)][2]
        # where a 'state' is a tuple representing the bucket, ex:
        # (0, 0, 3, 7)

    # Discretizing input space to make Q-table and to reduce dimmensionality
    def discretize(self, obs):
        # cart position is bound to self.env.observation_space.high[0] (+4.8 -4.8)
        # cart velocity is bound to (0.5)
        # cart angle is bound to self.env.observation_space.high[2] (-24 24)
        # cart Velocity At Tip is bound to -math.radians(50) +math.radians(50)
        upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50)]
        lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50)]

        # normalize (min max) the observation between 0 and 1 * bin size (as intergers)
        # first line: min-max normalization
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        # second line: normalization * bit size => keep only the integer part
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]

        # limit the max value
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)

    # Choosing action based on epsilon-greedy policy
    def choose_action(self, state, epsilon):
        # TODO 2:  change the greedy policy to an epsilon-greedy policy
        # Note 1: return np.argmax(self.Q[state])
        # numpy.argmax(a, axis=None, out=None) returns the indices of the maximum values along an axis.
        # Note 2: look at env.action_space.sample()
        if random.Random() > epsilon :
            return np.argmax(self.Q[state]) 
        return random.choice(self.Q[state])


    # Updating Q-value of state-action pair based on the Bellman update equation
    def update_q(self, state_old, action, reward, state_new, alpha):
        self.Q[state_old][action] += 1  # TODO 3:  implement the right side of this equation

    # Adaptive learning of Exploration Rate
    def get_epsilon(self, t):
        return max(self.min_epsilon, min(1, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    # Adaptive learning of Learning Rate
    def get_alpha(self, t):
        return max(self.min_alpha, min(1.0, 1.0 - math.log10((t + 1) / self.ada_divisor)))

    def run(self):

        for e in range(self.n_episodes):
            # As states are continuous, discretize them into buckets
            current_state = self.discretize(self.env.reset())

            # Get adaptive learning alpha and epsilon decayed over time
            alpha = self.get_alpha(e)
            epsilon = self.get_epsilon(e)
            done = False
            i = 0

            while not done:
                # Render environment
                self.env.render()

                action = 1; # TODO 4: Choose action according to epsilon-greedy policy and take it

                obs, reward, done, _ = self.env.step(action)
                new_state = self.discretize(obs)

                # Update Q-Table
                self.update_q(current_state, action, reward, new_state, alpha)
                current_state = new_state
                i += 1

if __name__ == "__main__":

    # Make an instance of CartPole class
    solver = CartPole()
    solver.run()
