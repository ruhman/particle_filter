# coding: utf-8
from random import randint, choice
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
import random
from pf import Particle
from nav_msgs.msg import OccupancyGrid
from occupancy_field import OccupancyField
from helper_functions import angle_normalize, angle_diff

def nb_draw_map(mapa_numpy, particles = None, initial_position=False, pose=False, robot=False):
    """
        particles - um conjunto de partículas definidas como objetos do tipo partícula

        initial_position - cor para desenhar a posição inicial do robo

        pose - pose do robo

        robot - booleano que determina se o robô é desenhado como um círculo ou não
    """
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set(xlim=[0, width], ylim=[0, height]) # Or use "ax.axis([x0,x1,y0,y1])"

    fig.canvas.draw()

### Gera N particulas aleatorias distribuidas uniformemente dentro
### de uma area minx, miny, maxx, maxy
def gerar_particle_cloud(pose, minx=10,maxx=60,miny=10,maxy=60, var_theta = math.pi/3, n=40):
    particle_cloud = []
    s = pose
    var_x = maxx - minx
    var_y = maxy-miny
    for i in range(n):
        x = random.uniform(s[0] - var_x, s[0] + var_x)
        y = random.uniform(s[1] - var_x, s[1] + var_y)
        theta = random.uniform(s[2] - var_theta, s[2] + var_theta)
        p = Particle(x, y, theta, w=1.0) # A prob. w vai ser normalizada depois
        particle_cloud.append(p)
    return particle_cloud

### Desenha as n particulas
def nb_draw_particle_cloud(particles, ax):
    """
        Desenha o particle cloud
        particles - uma lista de objetos Particle
        ax - eixo
    """
    for p in particles:
        nb_draw_arrow(p.x, p.y, p.theta, ax, particle_size, color='b')

### Lista de movimentos
movimentos = [[-10, -10, 0], [-10, 10, 0], [-10,0,0], [-10, 0, 0],
              [0,0,math.pi/12.0], [0, 0, math.pi/12.0], [0, 0, math.pi/12],[0,0,-math.pi/4],
              [-5, 0, 0],[-5,0,0], [-5,0,0], [-10,0,0],[-10,0,0], [-10,0,0],[-10,0,0],[-10,0,0],[-15,0,0],
              [0,0,-math.pi/4],[0, 10, 0], [0,10,0], [0, 10, 0], [0,10,0], [0,0,math.pi/8], [0,10,0], [0,10,0],
              [0,10,0], [0,10,0], [0,10,0],[0,10,0],
              [0,0,-math.radians(90)],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0]]

### Aplica deslocamento  delta com desvio padrao
def deslocamento (movimentos, delta, std):
    movimentos=[]
    for mov in movimentos:
        movN = []
        movN[0] += delta[0] + np.random.randint(0, std[0])
        movN[1] += delta[1] + np.random.randint(0, std[1])
        movN[2] += delta[2] + np.random.randint(0, std[2])
        movimentos.append(movN)
    return movimentos

### Desenha particulas apos deslocamento
delta = [10, 5, math.pi/4]
std = [3, 2, 1.5]
nb_draw_particle_cloud(deslocamento(movimentos, delta, std), ax)
