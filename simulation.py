# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:42:41 2020

@author: alejandro
"""

"""

"""
class particle:
  def __init__(self,index = 0, position = [0.0,0.0],speed = [0.0,0.0],charge = 0.0, radius = 1.0,intro_epoch = 0.0,DOF = [True,True]):
    self.index = index
    self.charge = charge
    self.position = position
    self.speed = speed
    self.radius = radius
    self.intro_epoch = intro_epoch
    self.DOF = DOF  "degree of freedom"
class shape:        
  import numpy as np
  def __init__(self,index = 0,position = [0.0,0.0],lenght = 1.0,angle = 0,intro_epoch = 0):
    self.index = index
    self.position = position
    self.angle = angle
    self.lenght = lenght
    self.normal_vector = np.array([np.sin(angle),-np.cos(angle)])
    self.intro_epoch = intro_epoch
class simulation:
  def __init__(self,x_len,y_len, temp ):
    self.temp = temp
    self.particles = []
    self.shapes = []
    self.time_step = 0.001 ## tiempo termico, relacionado con la energia termica del sistema
    self.epoch = 0
    self.plot_out = True
    self.f_c = [0,0]
  def add_particle(self,position,velocity,charge = 1.0, radius = 1.0):
    self.particles.append(particle(len(self.particles),position,velocity,charge,radius,self.epoch))
  def add_shape(self,position,lenght,angle):
    self.shapes.append(particle(len(self.shape),lenght,angle,self.epoch))
  
  
  def integrator(self):
    for i in range(len(self.particles)):
      """
      Add a interaction manager, who calculate the net force over the particle i
      the comunication variable must be f_c
      """
      f_x = self.f_c[0]   
      f_y = self.f_c[1]
      if self.particles.DOF[0] == True:
        v_x = f_x*self.time_step + self.particles[i].velocity[-1][0]
      else:
        v_x = self.particles[i].velocity[-1][0]
      if self.particles.DOF[1]== True:
        v_y = f_y*self.time_step + self.particles[i].velocity[-1][1]
      else:
        v_y = self.particles[i].velocity[-1][1]
      p_x = v_x*self.time_step + self.particles[i].position[-1][0]
      p_y = v_y*self.time_step + self.particles[i].position[-1][1]
      """
      Add a shape cross detector detector a corrector 
      """
      self.particles[i].velocity.append([v_x,v_y])
      self.particles[i].position.append([p_x,p_y])
      