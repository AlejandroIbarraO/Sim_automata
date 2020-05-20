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
simulation_size = 10
nn = 25
n_sick = 3
S = simulation(boundary_len = simulation_size,boundary ='none',viral_particles= True)
S.time_step = .01
S.contagion_prob = 0.1
S.contagion_distance = 3.0
S.random_amp = 0.01
S.death_probability = 0.001
speed_m = 0.1
x_pos = 1.9*simulation_size*(np.random.rand(nn)-0.5)
y_pos = 1.9*simulation_size*(np.random.rand(nn)-0.5)
x_vel = speed_m*(np.random.rand(nn)-0.5)
y_vel = speed_m*(np.random.rand(nn)-0.5)
sick = np.full(nn,False)
sick[0:n_sick] = True

np.random.shuffle(sick)
dictionary = {1:'g',2:'r',3:'c',4:'k'}
for i in range(nn):
    S.add_particle(position = [x_pos[i],y_pos[i]], velocity = [x_vel[i],y_vel[i]], viral_state=sick[i])
    S.particles[-1].charge = 1.0
    S.particles[-1].set_destiny = True
#    S.particles[-1].destiny_position = [x_pos[i]/simulation_size,y_pos[i]/simulation_size]
def init():
    ax.set_xlim(-simulation_size, simulation_size)
    ax.set_ylim(-simulation_size, simulation_size)
def plot_data(i):
    S.run(10)
    #print(S.epoch)
    x_pos = []
    y_pos = []
    state = []
    for part in S.particles:
        x_pos.append(part.position[-1][0])
        y_pos.append(part.position[-1][1])
        part.destiny_position = [simulation_size*np.cos(2*np.pi*S.epoch/1000),
                                 simulation_size*np.sin(2*np.pi*S.epoch/1000)]
        if part.viral_state == False:
            state.append('b')
        else:
            state.append(dictionary[part.disease_level])
    state = np.array(state)
    print(S.epoch)
    ax.clear()
    ax.scatter(x_pos,y_pos, c = state)
    ax.set_xlim(-simulation_size, simulation_size)
    ax.set_ylim(-simulation_size, simulation_size)
anim = FuncAnimation(fig, plot_data, init_func=init, frames = 25,interval = 1)
plt.show()

    



    