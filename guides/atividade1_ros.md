
# Contato inicial com o ROS

### Setup do Git 

Crie um repositório git chamado robotica16 em seu usuário no Github 

Execute o script chamado checkandfork.py, que está no diretório */home/borg* do Linux fornecido.

Se você usar seu próprio Linux, baixe or repositório robotica16 em algum lugar que esteja no build path do ROS.


### Verifique seu robô

Itens a verificar:

- O cartão micro SD da Raspberry Pi está adequadamente inserido
- A Raspberry Pi está ligada e o display mostra um endereço IP
- O robô está ligado (você pode verificar se há algo em sua tela LCD)
- A Raspberry responde ao ping. Para fazer este teste digite: 

### A conexão com o Neatos

Abra um terminal e digite:

	$ cd
	$ roslaunch neato_node bringup.launch host:=IP_DO_ROBO

**Responda no seu relatório, em detalhes**

1. Que tópicos o robô publica?
2. Como você pode fazer para investigar?
3. Quais são as classes (ou tipo de dados) das mensagens?

** Observações

### rostopic

Para saber os tópicos, digite
	rostopic list

Para saber o tipo de um tópico, digite
	rostopic info NOME_DO_TOPICO

Para monitorar um tópico, use

	rostopic echo NOME_DO_TOPICO

### rosmg



Controle remoto do robô:

	$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py


**Visualize o grafo de nós e explique como o controle remoto funciona. Use o rqt_graph para isso**


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
