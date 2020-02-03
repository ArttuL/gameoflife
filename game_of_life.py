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
    def run(self,duration=10):
        # One game of life run
        steps=[]
        steps_static=[]
        world_array=self.initial_state.copy()
        kernel = np.ones((3,3), dtype=int)
        kernel[1,1] = 0
        steps.append(world_array.copy())
        for i in range(1,duration):
            # Very clever way of checking cells neighbors with convolution (not my own invention :)
            neighbors_array = signal.convolve2d(world_array, kernel, mode="same",boundary='wrap')
            # Check the rules of life and death
            # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Any live cell with two or three live neighbours lives on to the next generation.
            # Any live cell with more than three live neighbours dies, as if by overpopulation.
            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

            # Check which cells will die and which ones will live
            death_mask=np.logical_or(neighbors_array<2, neighbors_array>3) 
            birth_mask=neighbors_array==3
            # Update the array
            np.place(world_array, death_mask, [0])
            np.place(world_array, birth_mask, [1])
            steps.append(world_array.copy())
           # Check if the world is static or not
            steps_static.append(np.all(steps[i-1]==steps[i]))
         # save results   
        self.steps_static=steps_static
        self.steps=steps
        return steps


# Visualization functions
def gol_animation(steps):
    # Animates gameoflife runs
    # input steps=list of numpy arrays of an GoL game

    fig = plt.figure()
    ax = plt.axes()
    #line, = ax.plot([], [], lw=2)

    # initialization function: plot the background of each frame
    def init():
        ax.set_data([], [])
        return ax

    # animation function.  This is called sequentially
    def animate(i):
        frame=steps[i]
        print(i)
        size=frame.shape[0]
        #G is a NxNx3 matrix
        G = np.zeros((size,size,3))
        #Where we set the RGB for each pixel
        G[frame>0.5] = [0,0,0]
        G[frame<0.5] = [1,1,1]
    
        ax.imshow(G,interpolation='nearest',origin='upper')
         # For some reason imshow inverts in relation to y-axis
        #ax.invert_yaxis()

        # Major ticks
        ax.set_xticks(np.arange(0,size, 1))
        ax.set_yticks(np.arange(0, size, 1))

        # Labels for major ticks
        ax.set_xticklabels(np.arange(1, size+1, 1))
        ax.set_yticklabels(np.arange(1, size+1, 1))

        # Minor ticks
        ax.set_xticks(np.arange(-.5, size, 1), minor=True)
        ax.set_yticks(np.arange(-.5, size, 1), minor=True)

        ax.grid(color='grey', linewidth=2,which='minor')
        ax.set_title("Game of life. Step : "+str(i))
        return ax

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=None,
                                   frames=len(steps)-1, interval=500, blit=False)
    return anim       

def plot_step(gol_step):
    size=gol_step.shape[0]
    ax = plt.axes()

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
    ax.set_yticklabels(np.arange(1, size+1, 1))

    # Minor ticks
    ax.set_xticks(np.arange(-.5, size, 1), minor=True)
    ax.set_yticks(np.arange(-.5, size, 1), minor=True)
    ax.grid(color='grey', linewidth=2,which='minor')


    ax.set_title("Game of life step")

    return ax    


