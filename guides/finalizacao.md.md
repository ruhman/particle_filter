
# Guia de instalação ROS no Ubuntu 14.04

Finalização e verificação da instalação do ROS  em sua máquina Virtual ou Linux 14.04

<font color=red>Não se aplica à Raspberry Pi</font>. Todos os comandos devem ser dados em sua máquina de trabalho.

<font color=red>Você precisa usar Ubuntu 14.04</font> para evitar dores de cabeça. Teoricamente dá para rodar o que precisamos no ROS Kinetic Kame, mas muitos dos pacotes que ainda estão só no ROS Indigo Igloo precisarão ser compilados manualmente do Github.

### 1.&nbsp;Atualize os pacotes:

Este comando atualiza a lista de pacotes APT disponíveis nos repositórios.

	sudo apt-get update

### 2.&nbsp;Confirme que está tudo ok e atualizado com sua instalação do ROS:

	sudo apt-get install ros-indigo-desktop-full

### 3.&nbsp;Verifique a instalação ro rviz:

	sudo apt-get install ros-indigo-rviz


### 4.&nbsp;Instale o simulador do Neato:

	sudo apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs

### 5.&nbsp;Instale a OpenCV - para visão computacional:

	$cd /tmp

	$wget https://github.com/Itseez/opencv/archive/2.4.11.zip
	$unzip 2.4.11.zip
	$cd opencv-2.4.11
	$mkdir build
	$cd build

	$cmake .. -DCMAKE_BUILD_TYPE=RELEASE \

		-DBUILD_PYTHON_SUPPORT=ON \
		-DWITH_XINE=ON \
		-DWITH_OPENGL=ON \
		-DWITH_TBB=ON \
		-DBUILD_EXAMPLES=ON \
		-DBUILD_NEW_PYTHON_SUPPORT=ON \
		-DWITH_V4L=ON \
		-DOPENCV_EXTRA_MODULES_PATH=./modules
	$make -j2

	$sudo make install


### 6.&nbsp;Instale o gstreamer - para poder receber a imagem do robô

	sudo add-apt-repository ppa:gstreamer-developers/ppa
	sudo apt-get update
	sudo apt-get install gstreamer1.0*


### 7.&nbsp;Crie um ambiente de trabalho do catkin

catkin é uma ferramenta que compila e faz o ROS encontrar os programas ROS que você desenvolver

Lembre-se que no Unix o símbolo ~  significa seu diretório de usuário

	source /opt/ros/indigo/setup.bash
	mkdir -p ~/catkin_ws/src
	cd ~/catkin_ws/src
	catkin_init_workspace
	cd ..
	catkin_make

Inclua isto ao final do seu arquivo ~/.bashrc - fará com que os ROS reconheça os programas que você fez

	source ~/catkin_ws/devel/setup.bash


### 8.&nbsp;Configure um github para trabalhar:

Comece criando no site do Github um fork do repositório:
	https://github.com/mirwox/robotica16

Em seguida baixe os pacotes necessários para trabalhar:

	cd ~/catkin_ws/src 
	sudo apt-get install git subversion libv4l-devhub python-requests 
	
Instale o programa **teleop** para controlar o neato com as teclas:

    git clone https://github.com/ros-teleop/teleop_twist_keyboard.git
	
	
Os passos restantes podem ser feitos manualmente, ou você pode usar [este script Python que faz isso por você](https://raw.githubusercontent.com/mirwox/robotica16/master/config/checkandfork.py)

** Atenção**
Para o software básico do Neatos continua valendo o repositório *robotica16*, apesar de estarmos em 2017

Clone o projeto em seu computador local. Substitua *SEU_USERNAME_AQUI* por seu login no Github

	git clone https://github.com/SEU_USERNAME_AQUI/robotica16
	
Mude para o diretório
	cd robotica16
	
Configure o projeto do professor como *upstream* em relação ao seu.  
 Quando você faz um remote upstream tudo o que eu fizer se altera no seu diretório, mas você pode ter suas próprias alterações

	git remote add upstream https://github.com/mirwox/robotica16
	cd ..
	git clone https://github.com/ros-teleop/teleop_twist_keyboard.git
	cd ..
	catkin_make



Também é importante já ter lido o [Capítulo 1](https://cse.sc.edu/~jokane/agitr/agitr-letter-intro.pdf) e o [Capítulo 2](https://cse.sc.edu/~jokane/agitr/agitr-letter-intro.pdf) do *A Gentle Introduction to ROS*.


### 9.Conectando-se ao seu robô Neatos


Itens a verificar:

- O cartão micro SD da Raspberry Pi está adequadamente inserido
- A Raspberry Pi está ligada e o display mostra um endereço IP
- O robô está ligado (você pode verificar se há algo em sua tela LCD)
- A Raspberry responde ao ping. Para fazer este teste digite: 

Para ter o comando `ping` digite:

	$ ping IP_DO_ROBO

Lembre-se de que o `IP_DO_ROBO` é o endereço do seu robô que aparece na tela de LCD.

Também é importante que você tenha o conteúdo mais recente do [Github da disciplina](https://github.com/mirwox/robotica16) em seu diretório `˜/catkin_ws/`

Mude para seu diretório `˜/catkin_ws/`:

	$ cd ˜/catkin_ws/
	
Em seguida dê o comando:

	$ catkin_make
	
** Lembre-se de que não se deve digitar o *$*. Ele está aí para você saber que são comandos de terminal




### 10. A conexão com o Neatos

Abra um terminal e digite:

	$ cd
	$ roslaunch neato_node bringup.launch host:=IP_DO_ROBO
	
**Responda no seu relatório, em detalhes**

1. Que tópicos o robô publica?
2. Como você pode fazer para investigar?
3. Quais são as classes (ou tipo de dados) das mensagens?

Visualização da câmera do robô (em testes, se funcionar avise ao Fábio)

	$	rosrun image_view image_view image:=/camera/image_raw

Controle remoto do robô:

	$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py
	
	
**Instruções para debugar o vídeo:**

Pode-se verificar se o stream MJPG da câmera está ok acessando o seguinte endereço no Google Chrome ou Firefox. Substitua IP_DO_ROBO pelo endereço que estiver aparecendo em seu LCD.

	http://IP_DO_ROBO:11111/?action=stream
	
Se o *Video Mode* da câmera estiver configurado para uma das opções em H264, o seguinte comando permitirá testá-lo (digite no Linux em seu laptop)


	gst-launch-1.0 -v tcpclientsrc host=IP_DO_ROBO port=5001  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false





**Visualize o grafo de nós e explique como o controle remoto funciona. Use o rqt_graph para isso**





Abra o rviz:

	$ roscore	
	
<font color=red> Executar o roscore **não é necessário** se o *roslaunch neato_node*... estiver executando</font>

	
	
	$ rosrun rviz rviz

Na interface do RViz:

1. Adicione uma visão para o *scan laser* - /stable_scan
2. adicione uma visão para  odometria - /odom
3. adicione uma visão do próprio Neato - escolha *Robot Model* no menu *insert*
3. Mude o target_frame do LaserScan para a odometria
4. Explore as transformações (*rosrun tf view_frames*)
5. Procure entender o grafo de mensagens

Dicas:

a.Se ele reclamar da transformação do Robot Model, abra um novo terminal e dê o comando:

 &nbsp;
 
	rosrun tf static_transform_publisher 0 0 0 0 0 0 base_footprint odom 2

b.Experimente controlar o robô via teclado e também publicando a transformação:


&nbsp;

	rostopic pub -r 10 /cmd_vel geometry_msgs/Twist  '{linear:  {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'


c.Para explorar as transformações use o seguinte comando:

	rosrun tf view_frames
	
Este comando salvará um arquivo chamado *frames.pdf* no diretório em que foi salvo

d.Para entender o grafo de tópicos use: 
	
	rqt_graph
	



