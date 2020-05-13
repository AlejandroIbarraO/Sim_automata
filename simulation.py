# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:42:41 2020

@author: alejandro
"""

"""

"""
import numpy as np
class particle:
  def __init__(self,index = 0, position = [0.0,0.0],speed = [0.0,0.0],charge = 0.0, radius = 1.0,intro_epoch = 0.0,DOF = [True,True]):
    self.index = index
    self.charge = charge
    self.position = [position]
    self.speed = [speed]
    self.radius = radius
    self.intro_epoch = intro_epoch
    self.DOF = DOF  #degree of freedom""""
    self.viral_state = False
    self.is_death = False
    self.disease_level = 0
class shape:        
  def __init__(self,index = 0,position = [0.0,0.0],lenght = 1.0,angle = 0,intro_epoch = 0):
      self.index = index
      self.position = position
      self.angle = angle
      self.lenght = lenght
      self.normal_vector = np.array([np.sin(angle),-np.cos(angle)])
      self.intro_epoch = intro_epoch
    
class interaction:
    def __init__(self,particle_i,particle_j):
        self.rij = [particle_i.position[-1][0]-particle_j.position[-1][0],
                    particle_i.position[-1][1]-particle_j.position[-1][1]]
        self.distance = np.sqrt(np.square(self.rij[0])+np.square(self.rij[1]))
        self.rij_norm = [self.rij[0]/self.distance,self.rij[1]/self.distance]
        self.ij = [particle_i.index,particle_j.index]
        
    def update(self,particles,**kwargs):
        self.rij = [particles[self.ij[0]].position[-1][0]-particles[self.ij[1]].position[-1][0],
                    particles[self.ij[0]].position[-1][1]-particles[self.ij[1]].position[-1][1]]
        self.distance = np.sqrt(np.square(self.rij[0])+np.square(self.rij[1]))
        self.rij_norm = [self.rij[0]/self.distance,self.rij[1]/self.distance]
        if 'contagion_distance' in kwargs.keys():
            if self.distance < kwargs['contagion_distance']:
                if particles[self.ij[0]].viral_state ^ particles[self.ij[1]].viral_state:
                    #print([particles[self.ij[0]].viral_state, particles[self.ij[1]].viral_state])
                    get_sick = np.random.rand()<kwargs['contagion_prob']
                    if particles[self.ij[0]].viral_state == False:
                        particles[self.ij[0]].viral_state = get_sick
                    else:
                        particles[self.ij[1]].viral_state = get_sick
                    
            
        
class simulation:
    def __init__(self, temp = 0.0, boundary = 'none',boundary_len = 20.0,viral_particles = False):
        self.particles = []
        self.shapes = []
        self.time_step = 0.001
        self.epoch = 0
        self.plot_out = True
        self.f_c = [0,0]
        self.boundary_interaction = boundary # 3 types of boundaries none, reflect, periodic
        self.boundary_len = boundary_len
        self.viral_particles = viral_particles 
        self.contagion_distance = 3.0
        self.is_death = False
        self.disease_level = 0
        self.interactions = []
        self.contagion_prob = 1/3
    def add_particle(self,position,velocity,charge = 1.0, radius = 1.0, viral_state = False):
        self.particles.append(particle(len(self.particles),position,velocity,charge,radius,self.epoch))
        self.particles[-1].viral_state = viral_state
        self.add_new_interaction()
    
    def add_shape(self,position,lenght,angle):
        self.shapes.append(particle(len(self.shape),lenght,angle,self.epoch))
  
    def add_new_interaction(self):
        if len(self.particles)>1:
            for i in range(len(self.particles)-1):
                self.interactions.append(interaction(self.particles[i],self.particles[-1]))
    def update_interactions(self):
        for i in range(len(self.interactions)):
            if self.viral_particles == True:
                self.interactions[i].update(self.particles,contagion_distance = self.contagion_distance
                                   ,contagion_prob = self.contagion_prob)
            else:
                self.interactions[i].update(self.particles)
    def update_desease(self):
        for part in self.particles:
            pass
        
            
    def integrator(self):
      """
      Add a interaction manager, who calculate the net force over the particle i
      the comunication variable must be f_c
      """
      for i in range(len(self.particles)):
          f_x = self.f_c[0]   
          f_y = self.f_c[1]
          if self.particles[i].DOF[0] == True:
            v_x = f_x*self.time_step + self.particles[i].speed[-1][0]
          else:
            v_x = self.particles[i].velocity[-1][0]
          if self.particles[i].DOF[1]== True:
            v_y = f_y*self.time_step + self.particles[i].speed[-1][1]
          else:
            v_y = self.particles[i].velocity[-1][1]
          p_x = v_x*self.time_step + self.particles[i].position[-1][0]
          p_y = v_y*self.time_step + self.particles[i].position[-1][1]
          """
          Add a shape cross detector detector a corrector 
          """
          self.particles[i].speed.append([v_x,v_y])
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
           # if self.viral_particles:
           #     self.update_desease()
           self.update_interactions()
           self.integrator() 

