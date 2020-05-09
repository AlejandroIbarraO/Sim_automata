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
    self.DOF = DOF  #degree of freedom""""
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
  def __init__(self,x_len,y_len, temp = 0.0, boundary = 'none',boundary_len = 20.0):
    self.particles = []
    self.shapes = []
    self.time_step = 0.001
    self.epoch = 0
    self.plot_out = True
    self.f_c = [0,0]
    self.boundary_interaction = boundary # 3 types of boundaries none, reflect, periodic
    self.boundary_len = boundary_len
  def add_particle(self,position,velocity,charge = 1.0, radius = 1.0):
    self.particles.append(particle(len(self.particles),position,velocity,charge,radius,self.epoch))
  def add_shape(self,position,lenght,angle):
    self.shapes.append(particle(len(self.shape),lenght,angle,self.epoch))
  
  def interaction_definition(self):
    pass
  
  
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
      """
      Boundary system detector-corrector
      """
      if self.boundary_interaction != 'none':
        for j in range(2):
          if abs(self.particles[i].position[-1][j])>self.boundary_len:
            if self.boundary_interaction == 'reflection':
               self.particles[i].position[-1][j] = self.boundary_len * self.particles[i].position[-1][j] / abs(self.particles[i].position[-1][j])
               self.particles[i].speed[-1][j] = self.particles[i].speed[-1][0] * -1.0
            elif self.boundary_interaction == 'periodic': 
               self.particles[i].position[-1][j] = -1 * self.boundary_len * self.particles[i].position[-1][j] / abs(self.particles[i].position[-1][j])
  def run(self, times):
    for i in range(times):
      self.epoch = self.epoch + 1
      self.interaction_definition()
      self.integrator() 

