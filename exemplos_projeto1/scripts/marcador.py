#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = ["Rachel P. B. Moraes", "Fabio Miranda"]

import rospy
import numpy
from numpy import linalg
import transformations
from tf import TransformerROS
import tf2_ros
import math
from geometry_msgs.msg import Twist, Vector3, Pose, Vector3Stamped
from ar_track_alvar_msgs.msg import AlvarMarker, AlvarMarkers
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from std_msgs.msg import Header

x = 0
y = 0
z = 0 
id = 0
tfl = 0

buffer = tf2_ros.Buffer()


x_desejado = 0.12
#y_desejado = 0.10
z_desejado = 1.80

def recebe(msg):
	global x # O global impede a recriacao de uma variavel local, para podermos usar o x global ja'  declarado
	global y
	global z
	global id
	for marker in msg.markers:
		x = round(marker.pose.pose.position.x, 2) # para arredondar casas decimais e impressao ficar ok
		y = round(marker.pose.pose.position.y, 2)
		z = round(marker.pose.pose.position.z, 2)
		#print(x)
		id = marker.id
		#print(marker.pose.pose)
		if id == 100:
			print(buffer.can_transform("base_link", "ar_marker_100", rospy.Time(0)))
			header = Header(frame_id= "ar_marker_100")
			# Procura a transformacao em sistema de coordenadas entre a base do robo e o marcador numero 100
			# Note que para seu projeto 1 voce nao vai precisar de nada que tem abaixo, a 
			# Nao ser que queira levar angulos em conta
			trans = buffer.lookup_transform("base_link", "ar_marker_100", rospy.Time(0))
			# Separa as translacoes das rotacoes
			t = transformations.translation_matrix([trans.transform.translation.x, trans.transform.translation.y, trans.transform.translation.z])
			# Encontra as rotacoes
			r = transformations.quaternion_matrix([trans.transform.rotation.x, trans.transform.rotation.y, trans.transform.rotation.z, trans.transform.rotation.w])
			m = numpy.dot(r,t)
			v2 = numpy.dot(m,[0,0,1,0])
			v2_n = v2[0:-1]
			n2 = v2_n/linalg.norm(v2_n)
			cosa = numpy.dot(n2,[1,0,0])
			angulo_marcador_robo = math.degrees(math.acos(cosa))
			print("Angulo entre marcador e robo", angulo_marcador_robo)


if __name__=="__main__":
	global tfl 
	global buffer

	rospy.init_node("marcador") # Como nosso programa declara  seu nome para o sistema ROS

	recebedor = rospy.Subscriber("/ar_pose_marker", AlvarMarkers, recebe) # Para recebermos notificacoes de que marcadores foram vistos
	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1) # Para podermos controlar o robo

	tfl = tf2_ros.TransformListener(buffer) # Para fazer conversao de sistemas de coordenadas - usado para calcular angulo


	try:
		# Loop principal - todo programa ROS deve ter um
		while not rospy.is_shutdown():
			if id == 100:
				if
				print ("z: ",z)
				print ("z desejado: ",z_desejado)
				if z_desejado < z-0.5:
				 	print("Vá para frente")
				 	vel = Twist(Vector3(0.5, 0, 0), Vector3(0, 0, 0))
				 	velocidade_saida.publish(vel)
				 	rospy.sleep(0.05)

				elif z-0.5 <= z_desejado or z_desejado >= z+0.5:
		 	 		print("Z CERTO")
		 	 		vel = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
		 	 		velocidade_saida.publish(vel)
				 	rospy.sleep(0.05)

				 else:
				 	print("Vá para trás")
				 	vel = Twist(Vector3(-0.5, 0, 0), Vector3(0, 0, 0))
			 		velocidade_saida.publish(vel)
				 	rospy.sleep(0.05)

			else:
				print("Não encontrei o marcador 100")
				vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
				velocidade_saida.publish(vel)
			rospy.sleep(0.05)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")


