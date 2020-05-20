# -*- coding: utf-8 -*-
"""
Created on Sun May  3 22:42:41 2020

@author: alejandro
"""

"""

"""
import numpy as np
from numba import jit
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
    self.neighbors = []
    self.force = [0.0,0.0]
    self.set_destiny = False
    self.destiny_position = [0.0,0.0]
    self.destiny_intensity = 1.0
    self.destiny_ofset = 2.0
    
class shape:        
  def __init__(self,index = 0,position = [0.0,0.0],lenght = 1.0,angle = 0,intro_epoch = 0):
      self.index = index
      self.position = position
      self.angle = angle
      self.lenght = lenght
      self.normal_vector = np.array([np.sin(angle),-np.cos(angle)])
      self.intro_epoch = intro_epoch
    
class interaction:
    def __init__(self,particle_i,particle_j,index):
        self.rij = [particle_i.position[-1][0]-particle_j.position[-1][0],
                    particle_i.position[-1][1]-particle_j.position[-1][1]]
        self.distance = np.sqrt(np.square(self.rij[0])+np.square(self.rij[1]))
        self.rij_norm = [self.rij[0]/self.distance,self.rij[1]/self.distance]
        self.ij = [particle_i.index,particle_j.index]
        self.index = index
        self.active_interaction = True
    def update(self,particles,**kwargs):
        self.rij = [particles[self.ij[0]].position[-1][0]-particles[self.ij[1]].position[-1][0],
                    particles[self.ij[0]].position[-1][1]-particles[self.ij[1]].position[-1][1]]
        self.distance = np.sqrt(np.square(self.rij[0])+np.square(self.rij[1]))
        if self.distance<1e-6:
            self.distance = 1e-5
        self.rij_norm = [self.rij[0]/self.distance,self.rij[1]/self.distance]
        self.active_interaction = particles[self.ij[0]].is_death or particles[self.ij[0]].is_death
        self.active_interaction = not(self.active_interaction)
        if 'contagion_distance' in kwargs.keys() and self.active_interaction:
            if self.distance < kwargs['contagion_distance']:
                particles[self.ij[0]].neighbors.append(self.index)
                particles[self.ij[1]].neighbors.append(self.index)
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
        self.random_walk = True
        self.random_amp = 0.1
        self.viscose_damping = 1.0
        self.append = False
        self.death_probability = 0.01
    def add_particle(self,position,velocity,charge = 1.0, radius = 1.0, viral_state = False):
        self.particles.append(particle(len(self.particles),position,velocity,charge,radius,self.epoch))
        self.particles[-1].viral_state = viral_state
        self.add_new_interaction()
    
    def add_shape(self,position,lenght,angle):
        self.shapes.append(particle(len(self.shape),lenght,angle,self.epoch))
  
    def add_new_interaction(self):
        if len(self.particles)>1:
            for i in range(len(self.particles)-1):
                self.interactions.append(interaction(self.particles[i],
                                                     self.particles[-1],len(self.interactions)))
                
    def update_interactions(self):
        for i in range(len(self.interactions)):
            if self.viral_particles == True:
                self.interactions[i].update(self.particles,contagion_distance = self.contagion_distance,contagion_prob = self.contagion_prob)
            else:
                self.interactions[i].update(self.particles)
    def update_particles(self):
        for part in self.particles:
            """
            sickness status - !down with the sickness!
            """
           
            if part.viral_state == True:
                if part.disease_level == 0:
                    part.disease_level = 1
                elif part.disease_level == 1 or part.disease_level == 2:
                    part.disease_level = part.disease_level+np.random.randint(-1,2)
                elif part.disease_level == 3:
                    part.is_death = np.random.rand()<self.death_probability 
                    part.disease_level = part.disease_level+np.random.randint(-1,0)
                    if part.is_death:
                        part.disease_level = 4
                    else:
                        part.disease_level = part.disease_level+np.random.randint(-1,0)
            part.force[0] = 0.0
            part.force[1] = 0.0
            """
            repulsive_central_force   ---> social distance == contagion_distance
            """
            if part.charge != 0.0:
                if len(part.neighbors)>0:
                    for index in part.neighbors:   
                        if part.index == self.interactions[index].ij[1]:
                            #print(part.index==self.interactions[index].ij[1])
                            part.force[0] = part.force[0]-part.charge*self.interactions[index].rij_norm[0]#/np.square(self.interactions[index].distance)
                            part.force[1] = part.force[1]-part.charge*self.interactions[index].rij_norm[1]#/np.square(self.interactions[index].distance)
                        else:
                            #print(part.index==self.interactions[index].ij[1])
                            part.force[0] = part.force[0]+part.charge*self.interactions[index].rij_norm[0]#/np.square(self.interactions[index].distance)
                            part.force[1] = part.force[1]+part.charge*self.interactions[index].rij_norm[1]#/np.square(self.interactions[index].distance)             
            
            if part.is_death == False:
                """
                central_force to one place of the space actractive !!!
                """
                if part.set_destiny == True:
                    distance =  np.sqrt(np.square(part.destiny_position[0]-part.position[-1][0])+
                                        np.square(part.destiny_position[1]-part.position[-1][1]))
                    if distance > part.destiny_ofset:
                        part.force[0] = part.force[0] + part.destiny_intensity*(part.destiny_position[0]-part.position[-1][0])/distance
                        part.force[1] = part.force[1] + part.destiny_intensity*(part.destiny_position[1]-part.position[-1][1])/distance
                """
                random force
                """
                if self.random_walk == True:
                    angle = np.random.rand()*2*np.pi
                    part.force[0] = part.force[0] + self.random_amp*np.cos(angle)
                    part.force[1] = part.force[1] + self.random_amp*np.sin(angle)
                """
                viscose force
                    
                """
                speed_magnitude = np.sqrt(np.square(part.speed[-1][0])+np.square(part.speed[-1][1]))
                part.force[0] = part.force[0] - self.viscose_damping*part.speed[-1][0]*np.power(speed_magnitude,3/2)
                part.force[1] = part.force[1] - self.viscose_damping*part.speed[-1][1]*np.power(speed_magnitude,3/2)
        ##print(part.force)

                    
                    
    def integrator(self):
      """
      Add a interaction manager, who calculate the net force over the particle i
      the comunication variable must be f_c
      """
      for i in range(len(self.particles)):
          if self.particles[i].is_death == False:
              f_x = self.particles[i].force[0]  
              f_y = self.particles[i].force[1]
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
              if self.append == True:
                  self.particles[i].speed.append([v_x,v_y])
                  self.particles[i].position.append([p_x,p_y])
              else:
                  
                  self.particles[i].speed = [[v_x,v_y]]
                  self.particles[i].position = [[p_x,p_y]]            
                  self.particles[i].neighbors = []
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
           try:
               self.update_interactions()
           except:
               print('interaction_error') 
           try:
               self.update_particles()
           except:
               print('update_error')
           try:
               self.integrator() 
           except:
               print('integrate_error')

