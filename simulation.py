# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:42:41 2020

@author: alejandro
"""

"""

"""
class particle:
  def __init__(self,index = 0, position = np.array([0.0,0.0]),speed = np.array([0.0,0.0]),charge = 0.0, radius = 1.0,intro_epoch = 0.0):
    self.index = index
    self.charge = charge
    self.position = position
    self.speed = speed
    self.radius = radius
    self.intro_epoch = intro_epoch
class shape:        
  import numpy as np
  def __init__(self,index = 0,position = np.array([0.0,0.0]),lenght = 1.0,angle = 0,intro_epoch = 0):
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
    self.
        
  def add_particle(self,position,velocity,charge = 1.0, radius = 1.0):
    self.particles.append(particle(len(self.particles),position,velocity,charge,radius,self.epoch))
  def add_shape(self,position,lenght,angle):
    self.shapes.append(particle(len(self.shape),lenght,angle,self.epoch))
  