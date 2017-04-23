#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
#Para rodar:
#    roslaunch projeto2 server_with_map_and_gui_plus_robot.launch
#    roslaunch stdr_launchers rviz.launch
#	rosrun projeto2 projeto2.py
#

import rospy
from nav_msgs.msg import OccupancyGrid
from nav_msgs.srv import GetMap
from sensor_msgs.msg import LaserScan
from stdr_msgs.msg import RobotIndexedMsg, RobotIndexedVectorMsg
from nav_msgs.msgs import MapMetaData


import tf
from tf import TransformListener
from tf import TransformBroadcaster
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix

import numpy as np

import inspercles


import math

# Seu chute inicial de posição para o robo
initial_pose = [2.0, 2.0, math.pi]
inspercles.initial_pose = initial_pose

particulas = []
particle_pub = None
map_metadata = None
mapa =  None



def get_mapa():
    mapa_temp = rospy.wait_for_message("/map", OccupancyGrid) 
    map_metadata = rospy.MapMetaData
    inspercles.w = map_metadata.width
    inspercles.h = map_metadata.height
    inspercles.resolution = map_metadata.resolution
    return mapa_temp


mapa = None
nome_laser = "robot0/laser1"
nome_odom = "robot0/odom"




def recebe_laser_scan(msg):
    """
    Método principal, que vai rodar tudo
    """
    # Incorpore os movimentos (diferenca na odometria) às particulas
    # Atualize o W das particulas com base no laser e na simulacao da posicao real
    # Reamostre as particulas
    # Publique as particulas (usando o particle_pub)
    pass

def recebe_posicao_initial():
	pass

def get_laser_info():
  """
    Retorna um array com as posições dos sensores laser.
    Assume que o 1.o beam está sempre alinhado com o ângulo 0 do robô
    Obtém do 1.o robo que for retornado do topico stdr_server/active_robots
  """
  robots = rospy.wait_for_message("/stdr_server/active_robots", RobotIndexedVectorMsg) 
  robot = robots.robots[0] 
  print("Nome encontrado: ", robot.name)
  body = robot.robot
  laser = body.laserSensors[0]
  min_ang = laser.minAngle
  max_ang = laser.maxAngle
  num_rays = laser.numRays
  angles = np.linspace(min_ang, max_ang, num_rays)
  return angles

def publish_particles(particulas):
    particles_conv = []
    for p in particulas:
        particles_conv.append(p.as_pose())
    # actually send the message so that we can view it in rviz
    particle_pub.publish(PoseArray(header=Header(stamp=rospy.Time.now(),
                                        frame_id=self.map_frame),
                              poses=particles_conv))



# Métodos úteis 
from helper_functions import (convert_pose_inverse_transform,
                              convert_translation_rotation_to_pose,
                              convert_pose_to_xy_and_theta,
                              angle_diff)





if __name__ == '__main__':

  msg = """
  ANTES de executar este script, por favor faça:

    roslaunch projeto2 server_with_map_and_gui_plus_robot.launch

    roslaunch stdr_launchers rviz.launch

  Para usar o teleop vai ser preciso redirecionar o cmd_vel para o robô que está sendo simulado:

    rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=robot0/cmd_vel
  """

  print(msg)


  # O tópico stdr_server/active_robots tem os robôs ativos




  rospy.init_node('fp')

  angles = get_laser_info()
  mapa = get_mapa()

  print("Mapa lido")

  r = rospy.Rate(10)

  # Crie as particulas


  # Publica as partículas para aparecerem no rviz
  particle_pub = rospy.Publisher("particlecloud", PoseArray, queue_size=10)

  # laser_subscriber listens for data from the lidar
  laser = rospy.Subscriber(nome_laser, LaserScan, recebe_laser_scan)
  # O mapa
  mapa = get_mapa()

  particulas = inspercles.nb_initialize_particle_cloud()

  print("main loop")

  while not(rospy.is_shutdown()):
      # in the main loop all we do is continuously broadcast the latest map to odom transform
      print("b.")
      publish_particles(particulas)
      r.sleep()

