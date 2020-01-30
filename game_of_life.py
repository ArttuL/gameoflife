import numpy as np
import pandas as pd
import scipy
import os
import sys
from scipy import signal

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
            death_mask=np.logical_or(neighbors_array==2, neighbors_array==3) 
            birth_mask=neighbors_array==3
            # Update the array
            np.place(world_array, death_mask, [0])
            np.place(world_array, birth_mask, [1])
            steps.append(world_array.copy())
           # Check if the world is static or not
            steps_static=append(np.all(steps[i-1]==steps[i]))
         # save results   
        self.steps_static=steps_static
        self.steps=steps
        return steps
