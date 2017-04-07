# Mini-guia sobre como criar um pacote rospy


*Atenção*: <font color=red> Mude o nome do package porque loop_python já existe </font>

Criando o pacote rospy:

mirwox@ubuntu:~/catkin_ws/src/robotica16$ catkin_create_pkg loop_python rospy std_msgs sensor_msgs geometry_msgs

A linha acima cria um diretório de projeto chamado loop_python que depende dos pacotes std_msgs, sensor_msgs e geometry_msgs

A resposta virá:


	Created file loop_python/CMakeLists.txt
	Created file loop_python/package.xml
	Created folder loop_python/src
	Successfully created files in /home/mirwox/catkin_ws/src/robotica16/loop_python. Please adjust the values in package.xml.

Em seguida crie um diretório para seus scripts Python:

	mirwox@ubuntu:~/catkin_ws/src/robotica16/loop_python$ mkdir scripts

Abra um editor e comece um programa em Python:


	#! /usr/bin/env python
	# -*- coding:utf-8 -*-

	import rospy
	from geometry_msgs.msg import Twist, Vector3

	v = 10  # Velocidade linear
	w = 5  # Velocidade angular

	if __name__ == "__main__":
	    rospy.init_node("roda_exemplo")
	    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)

	    try:
	        while not rospy.is_shutdown():
	            vel = Twist(Vector3(v,0,0), Vector3(0,0,w))
	            pub.publish(vel)
	            rospy.sleep(2.0)
	    except rospy.ROSInterruptException:
	        print("Ocorreu uma exceção com o rospy")



Mude as permissões do seu script para que execute:

	mirwox@ubuntu:~/catkin_ws/src/robotica16/exemplos_rospy/loop_python/scripts$ chmod a+x roda.py

Depois de mudar as permissões, a permissão de execução (letra x) vai ser adicionada à string de permissões 	-rwxrwxr-x

	mirwox@ubuntu:~/catkin_ws/src/robotica16/exemplos_rospy/loop_python/scripts$ ls -l roda.py
	-rwxrwxr-x 1 mirwox mirwox 505 Mar 16 23:25 roda.py

Para compilar o pacote volte ao diretório catkin_ws no shell:

	mirwox@ubuntu:~/catkin_ws$


	mirwox@ubuntu:~/catkin_ws$ catkin_make

Para executar:

mirwox@ubuntu:~/catkin_ws/devel$ rosrun loop_python roda.py


Lembre-se de que se começar a escrever o nome dos pacotes e apertar TAB o terminal irá autocompletar para você