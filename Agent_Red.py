import numpy as np
import pandas as pd

#Q-update formula:
'''
Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])
'''

class QLearningTable: #reward_decay is dicount rate aka gamma, and episolon greedy value = 0.1
    def __init__(self, actions, learning_rate = 0.01, reward_decay = 0.9, e_greedy = 0.1):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        #we create the q table
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        #we add states while we go to experiment


    def choose_action(self, observation):
        #adding observation into the table
        self.add_state(observation)
        #now we will check with the epsilon, it will tell what path to choose exploit or exploration
        if np.random.uniform() < self.epsilon:
            action = np.random.choice(self.actions) #explore
        else:
            state_action = self.q_table.loc[observation, :] #exploit
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        return action

    def learn(self, s, a, r, s_):
        #we need to add next state to our q table
        self.add_state(s_)
        #now we need to choose the best q value for a given pair of s and a
        #we need to look for the respective row s and respective column a
        q_predict = self.q_table.loc[s, a]
        #now, we need to check the next state is terminal or not. (if yes, we will end)
        if s_ != 'terminal':
            #we use bellman equation, we wil update q value. For that, we need current reward + gamma and the max of the q state
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()
        else:
            q_target = r
        self.q_table.loc[s,a] += self.lr * (q_target - q_predict)


    def add_state(self, state):
        #states will be at the index of our q table dataframe
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series([0]*len(self.actions),
                          index=self.q_table.columns,
                          name=state)
            )