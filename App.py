#it controls the update method of the agent and interaction betwene the agent

from maze_env import Maze
from RL_agent import QLearningTable
import matplotlib
matplotlib.use('TkAgg') #for virtual environment
import matplotlib.pyplot as plt


episode_count = 60
episodes = range(episode_count)
rewards = []
movements = []

def run_experiment():
    for episode in episodes:
        print("Episode {0}/{1}".format(episode, episode_count)) #gives the output after every observation i.e. which episode is running, and how many episodes are left.
        observation = env.reset()
        moves = 0 #initialising our moves to 0.

        while True:
            env.render() #render the environment
            action = q_learning_agent.choose_action(str(observation))
            #get state reward from the observation of our environment
            observation_, reward, done = env.get_state_reward(action)
            moves += 1

            #now we need to learn from the transitions
            q_learning_agent.learn(str(observation), action, reward, str(observation_))
            #we will switch the observation
            observation = observation_

            if done:
                movements.append(moves) #at the terminal, we will show all movements
                rewards.append(reward)
                print("Reward is: {0}, Moves is: {1}".format(reward, moves))
                break

    print("************* GAME OVER! *************")
    plot_reward_movements()

def plot_reward_movements():
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(episodes, movements)
    plt.xlabel("Episodes")
    plt.ylabel("No. of movements")

    plt.subplot(2, 1, 2)
    plt.step(episodes, rewards)
    plt.xlabel("Episodes")
    plt.ylabel("Rewards")
    plt.savefig("Reward_movement_qlearning.png")
    plt.show()

if __name__ == "__main__":
    env = Maze()
    q_learning_agent = QLearningTable(actions=list(range(env.n_action)))
    env.window.after(10, run_experiment())
    env.window.mainloop()

