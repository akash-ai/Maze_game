#importing libraries
import numpy as np
import time
import sys

#creating window widgets
if sys.version_info == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40 #40 pixels
MAZE_H = 6
MAZE_W = 6 # we care building 6*6 matrix game

class Maze:
    def __init__(self):
        self.window = tk.Tk()
        #main window of our application
        #need to specify more attributes of our window
        #i.e. geometry
        self.window.title("Maze_Game_akash")
        self.window.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        #'{0}x{1}' ->this is the format to be used.
        #action space i.e. possible actions that my agent will take.

        self.action_space = ['U', 'D', 'L', 'R']
        #no. of actions
        self.n_action = len(self.action_space)
        self.build_maze() #calling the function down mentioned


    #building the maze window. We will put all widgets of our window here.
    def build_maze(self):
        #crating a canvas
        self.canvas = tk.Canvas(self.window, bg = 'white', width = MAZE_W*UNIT, height = MAZE_H*UNIT)


        #creating vertical lines now using loop function.
        for c in range(0, MAZE_W*UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_W*UNIT
            self.canvas.create_line(x0, y0, x1, y1)

        # creating horizontal  lines now using loop function.
        for r in range(0, MAZE_H*UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H*UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        #Now creating a starting or original point
        origin = np.array([20, 20])

        #creating holes now
        #1st is 2 units right and 1 unit down in the maze

        hell1_center = origin + np.array([UNIT*2 , UNIT])

        #creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15, fill = 'black'
        )

        # creating holes now part-2
        # 1st is 2 units down and 1 unit right in the maze
        hell2_center = origin + np.array([UNIT, UNIT * 2])

        # creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15, fill = 'black'
        )


        #creating holes part-3
        #1st is 3 units to the right, 2 units to the down
        hell3_center = origin + np.array([UNIT*3, UNIT * 2])

        # creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15, fill='black'
        )

        # creating holes part-4
        # 1st is 1 units to the right, 1 units to the down
        hell4_center = origin + np.array([UNIT, UNIT])

        # creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15, fill='black'
        )

        #creating holes part-5
        # 1st is 2 units right and 1 unit down in the maze
        hell5_center = origin + np.array([UNIT * 1, UNIT * 3])

        # creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.hell5 = self.canvas.create_rectangle(
            hell5_center[0] - 15, hell5_center[1] - 15,
            hell5_center[0] + 15, hell5_center[1] + 15, fill='black'
        )



        #creating a goal now (target)
        oval_center = origin + UNIT * 2
        # creating a rectangle for that #need to specify the cordinates of the rectangle
        # xcoorediantes - 15 and y-coordinates - 15

        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15, fill = 'yellow'
        )



        #now creating a explorer(AGENT)

        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15, fill = 'red'
        )

        #NoW, it's ready. We need to pack all widgets now together.
        self.canvas.pack()

#PART-2 we need render function to withdraw widgets when we begin new episode.

    def render(self):
        time.sleep(0.1) #0.1seconds sleep
        self.window.update()

#after every episode, we need a clear window of our maze grid with our INITIAL STATE of our system and return the states
    #inside the canvas.
    def reset(self):
        self.window.update() #to withdraw the widgets
        time.sleep(0.4)
        #then delete the red rectangle
        self.canvas.delete(self.rect)
        origin = np.array([20,20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill= 'red'
        )
        #return the coordinate of our rectangle
        return self.canvas.coords(self.rect)

#implementing state and reward PART-3

    def get_state_reward(self, action): #bascially the actions we follow is 0->UP, 1->DOWN, 2->RIGHT, 3->LEFT
        #get the current state. State is defined as the coordinates of the rectangle.
        s = self.canvas.coords(self.rect) #giving the coordinates of our agent where it is located.
        base_action = np.array([0,0]) #this is numbers that we add or decrease the location of the current state to compute the next state.
        if action == 0: #UP
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  #DOWN
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2: #right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:#LEFT
            if s[0] > UNIT:
                base_action[0] -= UNIT

        #now we need to move red rectangle to new position

        self.canvas.move(self.rect, base_action[0], base_action[1])
        #next state is:
        s_ = self.canvas.coords(self.rect)

        #now we can compute the reward for our given state.
        #yellow goal--> 1, black spot--->-1, empty space --> 0

        if s_ == self.canvas.coords(self.oval):#we will check its coordinates with target location first
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),
                    self.canvas.coords(self.hell3), self.canvas.coords(self.hell4),
                    self.canvas.coords(self.hell5)]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        return s_, reward, done


#this basically runs our window application
if __name__ == "__main__":
    maze = Maze()
    maze.build_maze()
    maze.window.mainloop()