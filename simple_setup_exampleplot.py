# -*- coding: utf-8 -*-
"""
Created on Sat May  9 10:50:13 2020

@author: alejandro
"""
import numpy as np
from simulation import simulation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

#Fig
fig=plt.figure()
ax = fig.add_subplot(1,2,1)
ax2 =fig.add_subplot(1,2,2)

#Shapes
imageE1=plt.imread("enf1.png")
imageE2=plt.imread("enf2.png")
imageE3=plt.imread("enf3.png")
imageE4=plt.imread("enf4.png")
imageN=plt.imread("noenf.png")
imagefond=plt.imread("fondo.png")

#Mascara 
s=[len(imagefond),len(imagefond[1])]
mask=np.zeros(s)
A=np.where(imagefond[:,:,0]<0.1)
for e in range(len(A[0])):
    a=A[0][e]
    b=A[1][e]
    mask[a,b]=1
 
#data       
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
    S.run(1)
    #print(S.epoch)
    x_pos = []
    y_pos = []
    state = []
    enfermos=0
    no_enfermos=0
    
    for part in S.particles:
        x_pos.append(part.position[-1][0])
        y_pos.append(part.position[-1][1])
        part.destiny_position = [simulation_size*np.cos(2*np.pi*S.epoch/1000),
                                 simulation_size*np.sin(2*np.pi*S.epoch/1000)]
        if part.viral_state == False:
            state.append('b')
            no_enfermos=no_enfermos+1
        else:
            state.append(dictionary[part.disease_level])
            enfermos=enfermos+1
    state = np.array(state)
    
    
    resumen=[enfermos,no_enfermos]
    names=['Enfermos','No Enfermos']
    aa=['r','b'] 
 
    
    
    print(S.epoch)
    ax.clear()
    ax.imshow(imagefond, extent=[-simulation_size,simulation_size,-simulation_size,simulation_size],alpha=0.5 )
    ax.scatter(x_pos,y_pos)
    
    o=0
    for xi, yi in zip(x_pos,y_pos):
        if S.particles[o].disease_level==1:
            im = OffsetImage(imageE1, zoom=12/ax.figure.dpi)
            im.image.axes = ax
            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
        elif S.particles[o].disease_level==2:
            im = OffsetImage(imageE2, zoom=12/ax.figure.dpi)
            im.image.axes = ax
            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
        elif S.particles[o].disease_level==3:
            im = OffsetImage(imageE3, zoom=12/ax.figure.dpi)
            im.image.axes = ax
            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
        elif S.particles[o].disease_level==4:
            im = OffsetImage(imageE4, zoom=12/ax.figure.dpi)
            im.image.axes = ax
            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
        else:
            im = OffsetImage(imageN, zoom=12/ax.figure.dpi)
            im.image.axes = ax
            ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
        ax.add_artist(ab)
        o=o+1


    ax.set_xlim(-simulation_size, simulation_size)
    ax.set_ylim(-simulation_size, simulation_size)
     
    ax2.clear()
    ax2.bar(names,resumen,color=aa)
    ax2.set_ylim(0, 50) 
    
    
anim=[]    
anim.append( FuncAnimation(fig, plot_data, init_func=init, frames = 25,interval = 1))  
anim.append( FuncAnimation(fig, plot_data, init_func=init, frames = 25,interval = 1))
plt.show()

    



    