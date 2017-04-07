#Como desenvolver sem robô - Alvar

Siga os passos a seguir para testar seus programas sem ter um robô, se você está usando marcadores Alvar

## 1. Instalar ros-indigo-ar-track-alvar
    sudo apt-get install ros-indigo-ar-track-alvar


## 2. Abrir a webcam

    roslaunch tag_tracking usb_cam

(a webcam deve acender)

## 3. Abrir rastreamento da webcam
    roslaunch tag_tracking ar_track_usb_cam

 Para que esta etapa funcione, você precisa ter um **arquivo de calibração de câmera**.

Veja [aqui mais detalhes](calibrar_camera.md) sobre como calibrar

**Atenção**: no caso do robô o referencial da câmera se chama camera_frame, mas quando usamos via webcam este referencial se chama head_camera. Isso influencia no rviz e nas chamadas no código a lookupTransform para converter entre sistemas de coordenadas.

## 4. Para ver se detectou
    rostopic echo ar_pose_marker

## 5. Para usar o robô virtual
    roslaunch neato_simulator neato_playground.launch


## Para imprimir marcadores
Lembre-se de que para gerar o arquivo de marcador para imprimir, use o comando

    rosrun ar_track_alvar createMarker
