import numpy as np
import pandas as pd
import scipy
import os
import sys
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib import animation, rc

class GameOfLife:
    def __init__(self,initial_state=None):
        print(initial_state)
        self.initial_state=initial_state
        self.steps=None
        self.steps_static=None
        # Default mode is Conways Game  B3S23 
        self.rule={'birth':[3],'survive':[2,3]}

    def run(self,duration=10,rule={'birth':[3],'survive':[2,3]}):
        # One game of life run
        # Duration is the number of steps of one game
        # Rule decides how different cells live or die. 'birth' defines the amount of living neighbor cells required
        # to make a dead cell to come alive. 'survive' defines minimum and maximum number of neighbors that are required to the cell keep on living 

        steps=[]
        steps_static=[]
        world_array=self.initial_state.copy()
        kernel = np.ones((3,3), dtype=int)
        kernel[1,1] = 0
        steps.append(world_array.copy())
        for i in range(1,duration):
            # Very clever way of checking cells neighbors with convolution (not my own invention :). 
            # Takes automatically care of periodic boundaries
            neighbors_array = signal.convolve2d(world_array, kernel, mode="same",boundary='wrap')

            # Check the rules of life and death
            # Any live cell with fewer than survive[0] live neighbours dies, as if by underpopulation.
            # Any live cell with survive[0] or survive[1] live neighbours lives on to the next generation.
            # Any live cell with more than survive[1] live neighbours dies, as if by overpopulation.
            # Any dead cell with exactly birth[:] live neighbours becomes a live cell, as if by reproduction.

            # Check which cells will die and which shall live
            death_mask=np.logical_or(neighbors_array<rule['survive'][0], neighbors_array>rule['survive'][1])
            # Boolean masks for empty cells which come alive at this step 
            birth_conditions_masks=[neighbors_array==i for i in rule['birth']]
            birth_mask=np.logical_or.reduce(birth_conditions_masks)

            #birth_mask=neighbors_array==3
            # Update the array
            np.place(world_array, death_mask, [0])
            np.place(world_array, birth_mask, [1])
            steps.append(world_array.copy())
           # Check if the world is static or not
            steps_static.append(np.all(steps[i-1]==steps[i]))
         # save results   
        self.steps_static=steps_static
        self.steps=steps
        self.rule=rule
        return steps


# Visualization functions
def gol_animation(steps):
    # This functuion animates gameoflife runs
    # input: steps=list of numpy arrays of an GoL game steps
    fig, ax = plt.subplots(figsize=(10, 10))
    # initialization function: plot the background of each frame
    def init():
        
        _=ax.set_data([], [])
        return ax

    # Animation function.  This is called sequentially
    def animate(i):
        frame=steps[i]
        size=frame.shape[0]
        #G is a NxNx3 matrix
        G = np.zeros((size,size,3))
        #Where we set the RGB for each pixel
        G[frame>0.5] = [0,0,0]
        G[frame<0.5] = [1,1,1]
    
        _=ax.imshow(G,interpolation='nearest',origin='upper')
         # For some reason imshow inverts in relation to y-axis
        #ax.invert_yaxis()

        # Major ticks
        _=ax.set_xticks(np.arange(0,size, 1))
        _=ax.set_yticks(np.arange(0, size, 1))

        # Labels for major ticks
        _=ax.set_xticklabels(np.arange(1, size+1, 1))
        _=ax.set_yticklabels(np.arange(size, 0, -1))

        # Minor ticks
        _=ax.set_xticks(np.arange(-.5, size, 1), minor=True)
        _=ax.set_yticks(np.arange(-.5, size, 1), minor=True)

        _=ax.grid(color='grey', linewidth=2,which='minor')
        _=ax.set_title("Game of life. Step : "+str(i))
        return 

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=None,
                                   frames=len(steps)-1, interval=500, blit=False)
    return anim       

def plot_step(gol_step):
    size=gol_step.shape[0]
    fig, ax = plt.subplots(figsize=(10, 10))
    #ax = plt.axes()

    #G is a NxNx3 matrix
    G = np.zeros((size,size,3))
    #Where we set the RGB for each pixel
    G[gol_step>0.5] = [0,0,0]
    G[gol_step<0.5] = [1,1,1]
    ax.imshow(G,interpolation='nearest',origin='upper')
    # For some reason imshow inverts in relation to y-axis
    #ax.invert_yaxis()

   # Major ticks
    ax.set_xticks(np.arange(0,size, 1))
    ax.set_yticks(np.arange(0, size, 1))

    # Labels for major ticks
    ax.set_xticklabels(np.arange(1, size+1, 1))
    ax.set_yticklabels(np.arange(size, 0, -1))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, size, 1), minor=True)
    ax.set_yticks(np.arange(-.5, size, 1), minor=True)
    ax.grid(color='grey', linewidth=2,which='minor')


    ax.set_title("Game of life step")

    return fig    


