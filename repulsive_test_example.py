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
simulation_size = 2
nn = 2
n_sick = 1
S = simulation(boundary_len = simulation_size,boundary ='reflection',viral_particles= True)
S.time_step = .05
S.contagion_distance = 5.0
S.contagion_prob = 0.1
speed_m = 0.2
angles = np.linspace(0,np.pi,nn)
x_pos = np.cos(angles)
y_pos = np.sin(angles)
x_vel = -speed_m*np.cos(angles)
y_vel = -speed_m*np.sin(angles)
sick = np.full(nn,False)
sick[0:n_sick] = False
np.random.shuffle(sick)
S.random_walk = False
for i in range(nn):
    S.add_particle(position = [x_pos[i],y_pos[i]], velocity = [x_vel[i],y_vel[i]], viral_state=sick[i])
    S.particles[-1].charge = 1.0
S.random_amp = 1.0
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

    



    