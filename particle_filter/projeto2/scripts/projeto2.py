# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Para rodar:
    roslaunch projeto2 server_with_map_and_gui_plus_robot.launch
    roslaunch stdr_launchers rviz.launch
	rosrun projeto2 projeto2.py
"""

import rospy
from nav_msgs.msg import OccupancyGrid
from nav_msgs.srv import GetMap
from sensor_msgs.msg import LaserScan

import tf
from tf import TransformListener
from tf import TransformBroadcaster
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix


import math

# Seu chute inicial de posição para o robo
initial_pose = [2.0, 2.0, math.pi]
particulas = []

def obter_mapa():
  rospy.wait_for_service('static_map')
  try:
     get_map = rospy.ServiceProxy('static_map', GetMap)
     mapa = get_map().map
     return mapa
  except rospy.ServiceException, e:
     print "Service call failed: %s"%e


mapa = None
nome_laser = "robot0/laser1"
nome_odom = "robot0/odom"




def recebe_laser_scan(msg):
	"""
		Método principal, que vai rodar tudo
	"""

	# Incorpore os movimentos (diferenca na odometria) às particulas

	# Atualize o W das particulas com base no laser

	# Reamostre as particulas

	# Publique as particulas (usando o particle_pub)

def recebe_posicao_initial():
	pass




# Métodos úteis 
from helper_functions import (convert_pose_inverse_transform,
                              convert_translation_rotation_to_pose,
                              convert_pose_to_xy_and_theta,
                              angle_diff)





if __name__ == '__main__':

	rospy.init_node('fp')
	mapa = obter_mapa()

    r = rospy.Rate(10)

    # Crie as particulas


    # Publica as partículas para aparecerem no rviz
    particle_pub = rospy.Publisher("particlecloud", PoseArray, queue_size=10)

    # laser_subscriber listens for data from the lidar
    laser = rospy.Subscriber(nome_laser, LaserScan, recebe_laser_scan)


    while not(rospy.is_shutdown()):
        # in the main loop all we do is continuously broadcast the latest map to odom transform
        r.sleep()

