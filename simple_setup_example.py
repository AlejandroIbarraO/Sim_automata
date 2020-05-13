# -*- coding: utf-8 -*-
"""
Created on Sat May  9 10:50:13 2020

@author: alejandro
"""
import numpy as np
from simulation import simulation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
xdata, ydata = [], []
simulation_size = 25
nn = 50
n_sick = 3
S = simulation(boundary_len = simulation_size,boundary ='periodic',viral_particles= True)
S.time_step = .05
S.contagion_prob = 0.1
speed_m = 3.0
x_pos = 1.9*simulation_size*(np.random.rand(nn)-0.5)
y_pos = 1.9*simulation_size*(np.random.rand(nn)-0.5)
x_vel = speed_m*(np.random.rand(nn)-0.5)
y_vel = speed_m*(np.random.rand(nn)-0.5)
sick = np.full(nn,False)
sick[0:n_sick] = True
np.random.shuffle(sick)
for i in range(nn):
    S.add_particle(position = [x_pos[i],y_pos[i]], velocity = [x_vel[i],y_vel[i]], viral_state=sick[i])
def init():
    ax.set_xlim(-simulation_size, simulation_size)
    ax.set_ylim(-simulation_size, simulation_size)
def plot_data(i):
    S.run(5)
    #print(S.epoch)
    x_pos = []
    y_pos = []
    state = []
    
    for part in S.particles:
        x_pos.append(part.position[-1][0])
        y_pos.append(part.position[-1][1])
        if part.viral_state == False:
            state.append('b')
        else:
            state.append('r')
    state = np.array(state)
    ax.clear()
    ax.scatter(x_pos,y_pos, c = state)
    ax.set_xlim(-simulation_size, simulation_size)
    ax.set_ylim(-simulation_size, simulation_size)
    
anim = FuncAnimation(fig, plot_data, init_func=init, frames = 25,interval = 1)
plt.show()

    



    