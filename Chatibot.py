#C:\Users\TUMI Robotics\Desktop\Devel

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import cv2
import numpy as np
import socket
import pickle
import struct
import time
import multiprocessing
from multiprocessing import Value, Lock
import threading
import pygame
from pygame.locals import *
import signal
from os.path import isfile,join
import os
#import requests

V1G = 0
CONN = 0


def camera1Recv(numDir,wd):
	nombreDirCam1 = "pok" + str(numDir)
	os.mkdir(nombreDirCam1)
	nombreDirCam1 = "\pok" + str(numDir)
	nombreDirVid1 = wd+nombreDirCam1+"\I"
	imgSav=wd+"\poke3.png"
	print("Ruta de guardado de imagen: ",imgSav)
	print("Ruta de guardado de video: ",nombreDirVid1)
	ClientCam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Camera is connecting")
	time.sleep(5)
	ServerCam = ('192.168.137.2',9666)
	ClientCam.connect(ServerCam)

	ImgDat = b""
	PacketSZ = struct.calcsize("Q")
	tiempoAc = 0
	numF = 0
	count = 0

	while True:
		while len(ImgDat) < PacketSZ:
			Pack = ClientCam.recv(4096)
			if not Pack:
				break
			ImgDat+=Pack

		mesSZ_pack = ImgDat[:PacketSZ]
		ImgDat = ImgDat[PacketSZ:]
		mesSZ = struct.unpack("Q",mesSZ_pack)[0]
		#print(mesSZ)

		while len(ImgDat) < PacketSZ:
			Pack = ClientCam.recv(4096)
			if not Pack:
				break
			ImgDat+=Pack

		ind_pack = ImgDat[:PacketSZ]
		ImgDat = ImgDat[PacketSZ:]
		ind = struct.unpack("Q",ind_pack)[0]

		while len(ImgDat) < mesSZ:
			Pack = ClientCam.recv(4096)
			if not Pack:
				break
			ImgDat+=Pack

		Img_pack = ImgDat[:mesSZ]
		ImgDat = ImgDat[mesSZ:]
		Img = pickle.loads(Img_pack)
		ImgDcd = cv2.imdecode(Img,cv2.IMREAD_COLOR)
		if ind == 1:
			cv2.imwrite(imgSav,ImgDcd)
			cv2.imwrite(nombreDirVid1 + str(count) + ".png",ImgDcd)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		if ind == 2:
			cv2.imwrite(imgSav,ImgDcd)
			cv2.imwrite(nombreDirVid1 + str(count) + ".png",ImgDcd)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		count = count + 1
	ClientCam.close()
	cv2.destroyAllWindows()

def camera2Recv(numDir,wd):
    nombreDirCam2 = "pok" + str(numDir)
    os.mkdir(nombreDirCam2)
    nombreDirCam2 = "\pok" + str(numDir)
    nombreDirVid2 = wd+nombreDirCam2+"\I"
    imgSav=wd+"\poke4.png"
    print("Ruta de guardado de imagen: ",imgSav)
    print("Ruta de guardado de video: ",nombreDirVid2)
    ClientCam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Camera is connecting")
    time.sleep(5)
    ServerCam = ('192.168.137.2',7666)
    ClientCam.connect(ServerCam)

    ImgDat = b""
    PacketSZ = struct.calcsize("Q")
    tiempoAc = 0
    numF = 0
    count = 0

    while True:
        while len(ImgDat) < PacketSZ:
            Pack = ClientCam.recv(4096)
            if not Pack:
                break
            ImgDat+=Pack

        mesSZ_pack = ImgDat[:PacketSZ]
        ImgDat = ImgDat[PacketSZ:]
        mesSZ = struct.unpack("Q",mesSZ_pack)[0]

        while len(ImgDat) < PacketSZ:
            Pack = ClientCam.recv(4096)
            if not Pack:
                break
            ImgDat+=Pack

        ind_pack = ImgDat[:PacketSZ]
        ImgDat = ImgDat[PacketSZ:]
        ind = struct.unpack("Q",ind_pack)[0]

        while len(ImgDat) < mesSZ:
            Pack = ClientCam.recv(4096)
            if not Pack:
                break
            ImgDat+=Pack

        Img_pack = ImgDat[:mesSZ]
        ImgDat = ImgDat[mesSZ:]
        Img = pickle.loads(Img_pack)
        ImgDcd = cv2.imdecode(Img,cv2.IMREAD_COLOR)
        if ind == 1:
            cv2.imwrite(imgSav,ImgDcd)
            cv2.imwrite(nombreDirVid2 + str(count) + ".png",ImgDcd)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if ind == 2:
            cv2.imwrite(imgSav,ImgDcd)
            cv2.imwrite(nombreDirVid2 + str(count) + ".png",ImgDcd)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        count = count + 1
    ClientCam.close()
    cv2.destroyAllWindows()


def ReadingInd(ClienteSocket,textSign):
    while True:
        dato = ClienteSocket.recv(4096)
        dato = pickle.loads(dato)
        textSign.emit(dato)

class ComunicationJy(QThread):
    textUp = pyqtSignal(str)

    def run(self):

        ClienteSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.textUp.emit("Estableciendo conexion con el Robot Chatibot")
        hostIP = '192.168.137.2'
        puerto = 8666
        ClienteSocket.connect((hostIP,puerto))
        self.textUp.emit("Se pudo establecer conexion con chatibot")
        time.sleep(1)
        ClienteSocket.sendall(pickle.dumps("$OAX01"))
        print("Inicio de camaras enviado")
        thread2 = threading.Thread(target = ReadingInd, args = (ClienteSocket,self.textUp,))
        thread2.start()

        while True:
            pygame.init()
            clock=pygame.time.Clock()
            joysticks=[]

            boton_A_presionado=0
            boton_B_presionado=0
            boton_X_presionado=0
            boton_Y_presionado=0
            boton_LB_presionado=0
            boton_RB_presionado=0
            boton_back_presionado=0
            boton_start_presionado=0
            flecha_derecha_presionado=0
            flecha_izquierda_presionado=0
            flecha_arriba_presionado=0
            flecha_abajo_presionado=0
            boton_RT_presionado=0
            boton_LT_presionado=0

            for i in range(pygame.joystick.get_count()):
                joysticks.append(pygame.joystick.Joystick(i))
                joysticks[-1].init() #Inicializa el joystic
            self.textUp.emit("Configuración del joystick terminada")
            run = True

            while run:
                clock.tick(20)
                for event in pygame.event.get():
                    if event.type == JOYBUTTONDOWN: #Si se presiona un boton
    					#Se analiza que botón se presionó. Cada boton tiene un número específico.
                        if event.button == 0:
                            boton_A_presionado=1 #Se actualiza la variable correspondiente
                        if event.button == 1:
                            boton_B_presionado=1
                        if event.button == 2:
                            boton_X_presionado=1
                        if event.button == 3:
                            boton_Y_presionado=1
                        if event.button == 4:
                            boton_LB_presionado=1
                        if event.button == 5:
                            boton_RB_presionado=1
                        if event.button == 6:
                            boton_back_presionado=1
                        if event.button == 7:
                            boton_start_presionado=1

                    if event.type == JOYBUTTONUP:#Si se suelta un boton
                		#Se analiza que botón se soltó
                        if event.button == 0:
                            boton_A_presionado=0 #Se actualiza la variable correspondiente
                        if event.button == 1:
                            boton_B_presionado=0
                        if event.button == 2:
                            boton_X_presionado=0
                        if event.button == 3:
                            boton_Y_presionado=0
                        if event.button == 4:
                            boton_LB_presionado=0
                        if event.button == 5:
                            boton_RB_presionado=0
                        if event.button == 6:
                            boton_back_presionado=0
                        if event.button == 7:
                            boton_start_presionado=0


                    if event.type == JOYHATMOTION: #Si se presiona una flecha. Este evento es un array 2x1, guarda el estado de las flechas arriba/abajo y derecha/izquierda
                        if (event.value[0] ==0) and ((flecha_derecha_presionado==1) or (flecha_izquierda_presionado==1)):#Si una flecha estaba presionada y deja de estarlo
                            flecha_derecha_presionado=0 #Se actualiza la variable correspondiente
                            flecha_izquierda_presionado=0
                        if (event.value[1] ==0) and ((flecha_arriba_presionado==1) or (flecha_abajo_presionado==1)):
                            flecha_arriba_presionado=0
                            flecha_abajo_presionado=0
                        if event.value[0] ==1: #Si se presiona una flecha
                            flecha_derecha_presionado=1#Se actualiza la variable correspondiente
                        if event.value[0] ==-1:
                            flecha_izquierda_presionado=1
                        if event.value[1] ==1:
                            flecha_arriba_presionado=1
                        if event.value[1] ==-1:
                            flecha_abajo_presionado=1


                    if event.type == JOYAXISMOTION:#Si se presiona una trigger (RT o LT)
                        if event.axis == 5:
    						#En el caso de los triggers, se analiza que tanto se ha presionado
    						#va de un rango de -0.99 (no presionado) a 0.99 (totalmente presionado)
                            if (event.value <0.99) and (boton_RT_presionado==1): #Si ya estaba presionado, y deja de estarlo
                                boton_RT_presionado=0 #Se actualiza la variable correspondiente
                            if event.value >=0.99: #Si se presiona un trigger
                                boton_RT_presionado=1#Se actualiza la variable correspondiente
    						#misma lógica para el boton LT
                        if event.axis == 4:
                            if (event.value <0.99) and (boton_LT_presionado==1):
                                boton_LT_presionado=0
                            if event.value >=0.99:
                                boton_LT_presionado=1

    			#Después de actualizar el estado de cada boton, se imprimen los que están presionados
                if (boton_A_presionado==1) and  (boton_RT_presionado==0) and  (boton_LT_presionado==0):
                    self.textUp.emit('Avanzar')
                    comando="$OAX3J0A"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                if boton_B_presionado==1:
                    comando="$OAX3J0B"
                    ClienteSocket.sendall(pickle.dumps(comando))
    				#Nucleo.write(comando.encode)
                    self.textUp.emit('Retroceder')

                if (boton_RT_presionado==1) and (boton_A_presionado==0):
                    comando="$OAX3J0r"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Giro Horario')

                if (boton_LT_presionado==1) and (boton_A_presionado==0):
                    comando="$OAX3J0l"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Giro AntiHorario')

                if (boton_LB_presionado==1) and (flecha_derecha_presionado==1) and (flecha_izquierda_presionado==0):
                    comando="$OAX3JR1"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Prender Luces')

                if (boton_LB_presionado==1) and (flecha_derecha_presionado==0) and (flecha_izquierda_presionado==1):
                    comando="$OAX3JR2"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Apagar Luces')

                if (boton_X_presionado==1) and (flecha_arriba_presionado==1) and (flecha_abajo_presionado==0):
                    comando="$OAX3JX1"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Aumentar Velocidad')

                if (boton_X_presionado==1) and (flecha_abajo_presionado==1) and (flecha_arriba_presionado==0):
                    comando="$OAX3JX2"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Disminuir velocidad')

                if (boton_A_presionado==1) and  (boton_RT_presionado==1) and  (boton_LT_presionado==0):
                    comando="$OAX3JRA"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Avanzar derecha')

                if (boton_A_presionado==1) and  (boton_RT_presionado==0) and  (boton_LT_presionado==1):
                    comando="$OAX3JLA"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    #Nucleo.write(comando.encode)
                    self.textUp.emit('Avanzar izquierda')

                if (boton_LB_presionado==1) and (flecha_arriba_presionado==1) and (flecha_abajo_presionado==0):
                    comando="$OAX1S"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    self.textUp.emit('StartMeasure')

                if (boton_Y_presionado==1) and (flecha_abajo_presionado==0) and (flecha_arriba_presionado==0):
                    comando="$OAX3JTM"
                    ClienteSocket.sendall(pickle.dumps(comando))
                    self.textUp.emit('MotoresActivados')

class TUMI_Xplora(QMainWindow):

    debugTextMain = pyqtSignal(str)
    wd1=os.getcwd()

    def SetWidgetXplora(self):

        #Set the palette of colours for the diferent
        #widgets inside the window
        paleta = QPalette()
        brush = QBrush(QColor(255,255,255,255))
        brush.setStyle(Qt.SolidPattern)
        brush1 = QBrush(QColor(0,0,0,0))
        brush1.setStyle(Qt.SolidPattern)
        brush2 = QBrush(QColor(66,73,90,255))
        brush2.setStyle(Qt.SolidPattern)
        brush3 = QBrush(QColor(55,61,75,255))
        brush3.setStyle(Qt.SolidPattern)
        brush4 = QBrush(QColor(22,24,30,255))
        brush4.setStyle(Qt.SolidPattern)
        brush5 = QBrush(QColor(29,32,40,255))
        brush5.setStyle(Qt.SolidPattern)
        brush6 = QBrush(QColor(210,210,210,255))
        brush6.setStyle(Qt.SolidPattern)
        brush7 = QBrush(QColor(0,0,0,255))
        brush7.setStyle(Qt.SolidPattern)
        brush8 = QBrush(QColor(85,170,255,255))
        brush8.setStyle(Qt.SolidPattern)
        brush9 = QBrush(QColor(255,0,127,255))
        brush9.setStyle(Qt.SolidPattern)
        brush10 = QBrush(QColor(44,49,60,255))
        brush10.setStyle(Qt.SolidPattern)
        brush11 = QBrush(QColor(210,210,210,128))
        brush11.setStyle(Qt.NoBrush)
        brush12 = QBrush(QColor(210,210,210,128))
        brush12.setStyle(Qt.NoBrush)
        brush13 = QBrush(QColor(51,153,255,255))
        brush13.setStyle(Qt.SolidPattern)
        brush14 = QBrush(QColor(210,210,210,128))
        brush14.setStyle(Qt.NoBrush)

        #Set the brush for each pallete of colours, ACTIVE
        paleta.setBrush(QPalette.Active,QPalette.WindowText,brush)
        paleta.setBrush(QPalette.Active,QPalette.BrightText,brush)
        paleta.setBrush(QPalette.Active,QPalette.ButtonText,brush)
        paleta.setBrush(QPalette.Active,QPalette.Button,brush1)
        paleta.setBrush(QPalette.Active,QPalette.Base,brush1)
        paleta.setBrush(QPalette.Active,QPalette.Window,brush1)
        paleta.setBrush(QPalette.Active,QPalette.Light,brush2)
        paleta.setBrush(QPalette.Active,QPalette.Midlight,brush3)
        paleta.setBrush(QPalette.Active,QPalette.Dark,brush4)
        paleta.setBrush(QPalette.Active,QPalette.AlternateBase,brush4)
        paleta.setBrush(QPalette.Active,QPalette.Mid,brush5)
        paleta.setBrush(QPalette.Active,QPalette.Text,brush6)
        paleta.setBrush(QPalette.Active,QPalette.ToolTipText,brush6)
        paleta.setBrush(QPalette.Active,QPalette.Shadow,brush7)
        paleta.setBrush(QPalette.Active,QPalette.Highlight,brush8)
        paleta.setBrush(QPalette.Active,QPalette.Link,brush8)
        paleta.setBrush(QPalette.Active,QPalette.LinkVisited,brush9)
        paleta.setBrush(QPalette.Active,QPalette.ToolTipBase,brush10)

        #Set the brush for each pallete of colours, INACTIVE
        paleta.setBrush(QPalette.Inactive,QPalette.WindowText,brush)
        paleta.setBrush(QPalette.Inactive,QPalette.BrightText,brush)
        paleta.setBrush(QPalette.Inactive,QPalette.ButtonText,brush)
        paleta.setBrush(QPalette.Inactive,QPalette.Button,brush1)
        paleta.setBrush(QPalette.Inactive,QPalette.Base,brush1)
        paleta.setBrush(QPalette.Inactive,QPalette.Window,brush1)
        paleta.setBrush(QPalette.Inactive,QPalette.Light,brush2)
        paleta.setBrush(QPalette.Inactive,QPalette.Midlight,brush3)
        paleta.setBrush(QPalette.Inactive,QPalette.Dark,brush4)
        paleta.setBrush(QPalette.Inactive,QPalette.AlternateBase,brush4)
        paleta.setBrush(QPalette.Inactive,QPalette.Mid,brush5)
        paleta.setBrush(QPalette.Inactive,QPalette.Text,brush6)
        paleta.setBrush(QPalette.Inactive,QPalette.ToolTipText,brush6)
        paleta.setBrush(QPalette.Inactive,QPalette.Shadow,brush7)
        paleta.setBrush(QPalette.Inactive,QPalette.Highlight,brush8)
        paleta.setBrush(QPalette.Inactive,QPalette.Link,brush8)
        paleta.setBrush(QPalette.Inactive,QPalette.LinkVisited,brush9)
        paleta.setBrush(QPalette.Inactive,QPalette.ToolTipBase,brush10)

        #Set the brush for each pallete of colours, DISABLED
        paleta.setBrush(QPalette.Disabled,QPalette.BrightText,brush)
        paleta.setBrush(QPalette.Disabled,QPalette.Button,brush1)
        paleta.setBrush(QPalette.Disabled,QPalette.Base,brush1)
        paleta.setBrush(QPalette.Disabled,QPalette.Window,brush1)
        paleta.setBrush(QPalette.Disabled,QPalette.Light,brush2)
        paleta.setBrush(QPalette.Disabled,QPalette.Midlight,brush3)
        paleta.setBrush(QPalette.Disabled,QPalette.Dark,brush4)
        paleta.setBrush(QPalette.Disabled,QPalette.WindowText,brush4)
        paleta.setBrush(QPalette.Disabled,QPalette.Text,brush4)
        paleta.setBrush(QPalette.Disabled,QPalette.ButtonText,brush4)
        paleta.setBrush(QPalette.Disabled,QPalette.Mid,brush5)
        paleta.setBrush(QPalette.Disabled,QPalette.ToolTipText,brush6)
        paleta.setBrush(QPalette.Disabled,QPalette.Shadow,brush7)
        paleta.setBrush(QPalette.Disabled,QPalette.Link,brush8)
        paleta.setBrush(QPalette.Disabled,QPalette.LinkVisited,brush9)
        paleta.setBrush(QPalette.Disabled,QPalette.AlternateBase,brush10)
        paleta.setBrush(QPalette.Disabled,QPalette.ToolTipBase,brush10)
        paleta.setBrush(QPalette.Disabled,QPalette.Highlight,brush13)

        #Declaracion de las fuentes a utilizar para la creacion de
        #texto en la interfaz grafica
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setBold(True)
        font3.setWeight(75)
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(12)
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setPointSize(40)
        font6 = QFont()
        font6.setFamily(u"Segoe UI")
        font6.setPointSize(14)
        font7 = QFont()
        font7.setFamily(u"Segoe UI")
        font7.setPointSize(15)
        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(8)
        font9 = QFont()
        font9.setFamily(u"Segoe UI")
        font9.setPointSize(6)


        #Parametros iniciales de la ventana principal
        self.setFont(font)
        self.setPalette(paleta)
        self.setStyleSheet(u"QMainWindow {background: transparent;}\n"
"QToolTip {\n"
"       color: #ffffff;\n"
"       background-color: rgba(27,29,35,160);\n"
"       border: 1px solid rgb(40,40,40);\n"
"       border-radius: 2px;\n"
"}")

        #Definicion del widget central
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210,210,210);")

        #Definicion del Layout del widget central
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10,10,10,10)

        #Definicion del frame central, este frame se ubica a lo largo del central widget
        #Todos los componentes iran al interior del frame_main
        self.frame_main=QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"QLineEdit {\n"
"       background-color: rgb(27, 29, 35);\n"
"       border-radius: 5px;\n"
"       border: 2px solid rgb(27, 29, 35);\n"
"       padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"       border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"       border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"       border: none;\n"
"       background: rgb(52, 59, 72);\n"
"       height: 14px;\n"
"       margin: 0px 21px 0 21px;\n"
"       border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"       background: rgb(85, 170, 255);\n"
"       min-width: 25px;\n"
"       border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"       border: none;\n"
"       background: rgb(55, 63, 77);\n"
"       width: 20px;\n"
"       border-top-right-radius: 7px;\n"
"       border-bottom-right-radius: 7px;\n"
"       subcontrol-position: right;\n"
"       subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"       border: none;\n"
"       background: rgb(55, 63, 77);\n"
"       width: 20px;\n"
"       border-top-left-radius: 7px;\n"
"       border-bottom-left-radius: 7px;\n"
"       subcontrol-position: left;\n"
"       subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"       background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"       background: none;\n"
"}\n"
"QScrollBar:vertical {\n"
"       border: none;\n"
"       background: rgb(52, 59, 72);\n"
"       width: 14px;\n"
"       margin: 21px 0 21px 0;\n"
"       border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:vertical {  \n"
"       background: rgb(85, 170, 255);\n"
"       min-height: 25px;\n"
"       border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"       border: none;\n"
"       background: rgb(55, 63, 77);\n"
"       height: 20px;\n"
"       border-bottom-left-radius: 7px;\n"
"       border-bottom-right-radius: 7px;\n"
"       subcontrol-position: bottom;\n"
"       subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"       border: none;\n"
"       background: rgb(55, 63, 77);\n"
"       height: 20px;\n"
"       border-top-left-radius: 7px;\n"
"       border-top-right-radius: 7px;\n"
"       subcontrol-position: top;\n"
"       subcontrol-origin: margin;\n"
" }\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"       background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"       background: none;\n"
"}\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"       border: 3px solid rgb(52, 59, 72);\n"
"       width: 15px;\n"
"       height: 15px;\n"
"       border-radius: 10px;\n"
"       background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"       border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"       background: 3px solid rgb(52, 59, 72);\n"
"       border: 3px solid rgb(52, 59, 72);      \n"
"       background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"       border: 3px solid rgb(52, 59, 72);\n"
"       width: 15px;\n"
"       height: 15px;\n"
"       border-radius: 10px;\n"
"       background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"       border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"       background: 3px solid rgb(94, 106, 130);\n"
"       border: 3px solid rgb(52, 59, 72);      \n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"       background-color: rgb(27, 29, 35);\n"
"       border-radius: 5px;\n"
"       border: 2px solid rgb(27, 29, 35);\n"
"       padding: 5px;\n"
"       padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"       border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"       subcontrol-origin: padding;\n"
"       subcontrol-position: top right;\n"
"       width: 25px; \n"
"       border-left-width: 3px;\n"
"       border-left-color: rgba(39, 44, 54, 150);\n"
"       border-left-style: solid;\n"
"       border-top-right-radius: 3px;\n"
"       border-bottom-right-radius: 3px;        \n"
"       background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"       background-position: center;\n"
"       background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"       color: rgb(85, 170, 255);       \n"
"       background-color: rgb(27, 29, 35);\n"
"       padding: 10px;\n"
"       selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"       border-radius: 9px;\n"
"       height: 18px;\n"
"       margin: 0px;\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"       background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"       background-color: rgb(85, 170, 255);\n"
"       border: none;\n"
"       height: 18px;\n"
"       width: 18px;\n"
"       margin: 0px;\n"
"       border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"       background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"       background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"       border-radius: 9px;\n"
"       width: 18px;\n"
"       margin: 0px;\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"       background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"       background-color: rgb(85, 170, 255);\n"
"       border: none;\n"
"       height: 18px;\n"
"       width: 18px;\n"
"       margin: 0px;\n"
"       border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"       background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"       background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")

        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)

        #Definicion del Layout para el main_frame
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        #Definicion del Frame_Top para contener 2 frames principales
        #Frame_top
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(1000000, 65))
        self.frame_top.setStyleSheet(u"background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)

        #Definicion del layout para el frame 2
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        #Definicion del frame Hijo final para el boton de menu
        #Definicion del frame Hijo para el boton menu
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMinimumSize(QSize(70,0))
        self.frame_toggle.setMaximumSize(QSize(70, 1000000))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Raised)

        #Layout del frame Menu
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setAlignment(Qt.AlignCenter)

        #Elemento hijo para el frame Menu
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
"       background-image: url(C:/Users/TB-4H/OneDrive/Desktop/Devel/icons/24x24/cil-menu.png);\n"
"       background-position: center;\n"
"       background-repeat: no-reperat;\n"
"       border: none;\n"
"       background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")

        #Se añade el boton de manu al Layout 3 perteneciente al frame togle
        #Se añade el frame toggle al layout horizontal
        self.verticalLayout_3.addWidget(self.btn_toggle_menu)
        self.horizontalLayout_3.addWidget(self.frame_toggle)

        #Definicion del frame en donde estan los botones y la ruta del proyecto
        #Definicion del frame_top_right
        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)

        #Definicion del Layout del frame_top_right
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        #Definicion del frame en donde estaran los botones
        #Def frame_top_btns
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMinimumSize(QSize(0,42))
        self.frame_top_btns.setMaximumSize(QSize(1000000, 42))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)

        #Definicion del Layout para el frame_top_btns
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)

        #Definicion del frame para el nombre de la interfaz
        #Definicion de frame_Name
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy1)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)

        #Definicion del Layout para el nombre e icono de la interfaz
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)

        #Definicion del frame_icon
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-image: url(C:/Users/TB-4H/OneDrive/Desktop/Devel/icons/16x16/cil-terminal.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        #Se añade el frame icon al layout
        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        #Se crea el label del titulo
        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        self.label_title_bar_top.setFont(font1)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;")

        #Se añade el label del titulo al layout_10
        self.horizontalLayout_10.addWidget(self.label_title_bar_top)

        #Se añade el titulo e icono al frame padre
        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        #Se crea el frame para los botores
        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy1.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy1)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)

        #Se crea el layout para los botores
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        #Boton minimizar
        self.btn_minimize = QPushButton(self.frame_btns_right)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy2)
        self.btn_minimize.setMinimumSize(QSize(40, 0))
        self.btn_minimize.setMaximumSize(QSize(40, 16777215))
        self.btn_minimize.setStyleSheet(u"QPushButton { \n"
"       border: none;\n"
"       background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_minimize.setIcon(icon)
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.horizontalLayout_5.addWidget(self.btn_minimize)

        #Boton Maximizar
        self.btn_maximize_restore = QPushButton(self.frame_btns_right)
        self.btn_maximize_restore.setObjectName(u"btn_maximize_restore")
        sizePolicy2.setHeightForWidth(self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy2)
        self.btn_maximize_restore.setMinimumSize(QSize(40, 0))
        self.btn_maximize_restore.setMaximumSize(QSize(40, 16777215))
        self.btn_maximize_restore.setStyleSheet(u"QPushButton { \n"
"       border: none;\n"
"       background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1)
        self.btn_maximize_restore.setEnabled(False)
        self.horizontalLayout_5.addWidget(self.btn_maximize_restore)

        #Boton cerrar
        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy2.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy2)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setStyleSheet(u"QPushButton {    \n"
"       border: none;\n"
"       background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)
        self.btn_close.clicked.connect(lambda: self.close())
        self.horizontalLayout_5.addWidget(self.btn_close)

        #Se añade todo lo avanzado al frame parent
        self.horizontalLayout_4.addWidget(self.frame_btns_right,0, Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top_btns)

        #Se define el frame_info
        self.frame_top_info = QFrame(self.frame_top_right)
        self.frame_top_info.setObjectName(u"frame_top_info")
        self.frame_top_info.setMaximumSize(QSize(1000000, 65))
        self.frame_top_info.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_top_info.setFrameShape(QFrame.NoFrame)
        self.frame_top_info.setFrameShadow(QFrame.Raised)

        #Layout del frame top info
        self.horizontalLayout_8 = QHBoxLayout(self.frame_top_info)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 0, 10, 0)

        #Label del top info
        self.label_top_info_1 = QLabel(self.frame_top_info)
        self.label_top_info_1.setObjectName(u"label_top_info_1")
        self.label_top_info_1.setMaximumSize(QSize(1000000, 15))
        self.label_top_info_1.setFont(font2)
        self.label_top_info_1.setStyleSheet(u"color: rgb(98, 103, 111); ")
        self.horizontalLayout_8.addWidget(self.label_top_info_1)

        #Label para el usuario
        self.label_top_info_2 = QLabel(self.frame_top_info)
        self.label_top_info_2.setObjectName(u"label_top_info_2")
        self.label_top_info_2.setMinimumSize(QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QSize(250, 20))
        self.label_top_info_2.setFont(font3)
        self.label_top_info_2.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_top_info_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        #Se añade todo y se finaliza con la implementaciòn del frame_top
        self.horizontalLayout_8.addWidget(self.label_top_info_2)
        self.verticalLayout_2.addWidget(self.frame_top_info)
        self.horizontalLayout_3.addWidget(self.frame_top_right)
        self.verticalLayout.addWidget(self.frame_top)

        #Definicion del frame_Center
        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)

        #Layout para el frame_center
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        #Se define el frame izquierdo
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy3)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)

        #Definicion del Layout izquierdo
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)

        #Definicion del frame Menus
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)

        #Definicion del Layout
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        #Se agrega los menus al parent directo
        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignTop)

        #Creacion del menu auxiliar inferior
        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy3.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy3)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)

        #Definicion del Layout para el menu auxiliar
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)

        #Definicion del label del menu extra
        self.label_user_icon = QLabel(self.frame_extra_menus)
        self.label_user_icon.setObjectName(u"label_user_icon")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_user_icon.sizePolicy().hasHeightForWidth())
        self.label_user_icon.setSizePolicy(sizePolicy4)
        self.label_user_icon.setMinimumSize(QSize(60, 60))
        self.label_user_icon.setMaximumSize(QSize(60, 60))
        self.label_user_icon.setFont(font4)
        self.label_user_icon.setStyleSheet(u"QLabel {\n"
"       border-radius: 30px;\n"
"       background-color: rgb(44, 49, 60);\n"
"       border: 5px solid rgb(39, 44, 54);\n"
"       background-position: center;\n"
"       background-repeat: no-repeat;\n"
"}")

        #Se añade lo avanzado hasta aqui a los frame parent
        self.label_user_icon.setAlignment(Qt.AlignCenter)
        self.layout_menu_bottom.addWidget(self.label_user_icon, 0, Qt.AlignHCenter)
        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)
        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        #Se crea el frame content right
        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)

        #Se crea el layout del content RIght
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        #Se crea el frame content
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)

        #Se crea el layout del frame content
        self.verticalLayout_9 = QVBoxLayout(self.frame_content)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)

        #Se crea el objeto para manejar pestañas
        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")

        #Se crean las pestañas
        #AQUI SE CREA TODO LO QUE SE VAYA A UTILIZAR, AHORITA SOLO USA LABELS
        #Y LOS AÑADE AL PARENT
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        #self.page_home.resize(400,500)

        self.vertical_home = QVBoxLayout(self.page_home)
        self.vertical_home.setSpacing(5)
        self.vertical_home.setObjectName(u"vertical_home")

        self.frame_camaras = QFrame(self.page_home)
        self.frame_camaras.setObjectName(u"frame_camaras")
        self.frame_camaras.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_camaras.setFrameShape(QFrame.NoFrame)
        self.frame_camaras.setFrameShadow(QFrame.Raised)

        self.layout_camaras = QHBoxLayout(self.frame_camaras)
        self.layout_camaras.setObjectName(u"layout_camaras")
        self.layout_camaras.setSpacing(0)

        self.frame_cam1 = QFrame(self.frame_camaras)
        self.frame_cam1.setObjectName(u"frame_cam1")
        self.frame_cam1.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 0px;\n"
"}")
        self.frame_cam1.setFrameShape(QFrame.NoFrame)
        self.frame_cam1.setFrameShadow(QFrame.Raised)

        self.layout_cam1 = QVBoxLayout(self.frame_cam1)
        self.layout_cam1.setObjectName(u"layout_cam1")
        self.layout_cam1.setSpacing(1)
        self.layout_cam1.setContentsMargins(0,0,0,0)

        self.labelCam1_Idf = QLabel(self.frame_cam1)
        self.labelCam1_Idf.setFont(font3)
        self.labelCam1_Idf.setText(u"FRONT CAMERA")
        self.labelCam1_Idf.setStyleSheet(u"background-color: transparent")
        self.labelCam1_Idf.setAlignment(Qt.AlignCenter)

        self.label_camera1 = QLabel(self.frame_cam1)
        self.label_camera1.setStyleSheet(u"background-color: transparent")
        self.label_camera1.setAlignment(Qt.AlignCenter)

        self.layout_cam1.addWidget(self.labelCam1_Idf,0,Qt.AlignCenter|Qt.AlignTop)
        self.layout_cam1.addWidget(self.label_camera1,0,Qt.AlignCenter)

        self.frame_cam2 = QFrame(self.frame_camaras)
        self.frame_cam2.setObjectName(u"frame_cam1")
        self.frame_cam2.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 0px;\n"
"}")
        self.frame_cam2.setFrameShape(QFrame.NoFrame)
        self.frame_cam2.setFrameShadow(QFrame.Raised)

        self.layout_cam2 = QVBoxLayout(self.frame_cam2)
        self.layout_cam2.setObjectName(u"layout_cam2")
        self.layout_cam2.setSpacing(1)
        self.layout_cam2.setContentsMargins(0,0,0,0)

        self.labelCam2_Idf = QLabel(self.frame_cam2)
        self.labelCam2_Idf.setFont(font3)
        self.labelCam2_Idf.setText(u"BACK CAMERA")
        self.labelCam2_Idf.setStyleSheet(u"background-color: transparent")
        self.labelCam2_Idf.setAlignment(Qt.AlignCenter)

        self.label_camera2 = QLabel(self.frame_cam2)
        self.label_camera2.setStyleSheet(u"background-color: transparent")
        self.label_camera2.setAlignment(Qt.AlignCenter)

        self.layout_cam2.addWidget(self.labelCam2_Idf,0,Qt.AlignCenter|Qt.AlignTop)
        self.layout_cam2.addWidget(self.label_camera2,0,Qt.AlignCenter)

        self.layout_camaras.addWidget(self.frame_cam1,0,Qt.AlignCenter)
        self.layout_camaras.addWidget(self.frame_cam2,0,Qt.AlignCenter)
        self.vertical_home.addWidget(self.frame_camaras,0,Qt.AlignCenter)

        self.frameBackPart = QFrame(self.page_home)
        self.frameBackPart.setObjectName(u"frameBackPart")
        self.frameBackPart.setStyleSheet(u"background-color: transparent")
        self.frameBackPart.setFrameShape(QFrame.NoFrame)
        self.frameBackPart.setFrameShadow(QFrame.Raised)

        self.layout_BackPart = QHBoxLayout(self.frameBackPart)
        self.layout_BackPart.setObjectName(u"layout_BackPart")
        self.layout_BackPart.setSpacing(20)
        self.layout_BackPart.setAlignment(Qt.AlignCenter)
        self.layout_BackPart.setContentsMargins(0,0,0,0)

        self.frame_Robot = QFrame(self.frameBackPart)
        self.frame_Robot.setObjectName(u"frame_Robot")
        self.frame_Robot.setStyleSheet(u"QFrame {\n"
"       background-color: transparent;\n"
"       border-radius: 5px;\n"
"}")
        self.frame_Robot.setFrameShape(QFrame.NoFrame)
        self.frame_Robot.setFrameShadow(QFrame.Raised)

        self.layout_Robot = QVBoxLayout(self.frame_Robot)
        self.layout_Robot.setObjectName(u"layout_Robot")
        self.layout_Robot.setSpacing(0)
        self.layout_Robot.setContentsMargins(0,0,0,0)

        self.label_Robot = QLabel(self.frame_Robot)
        self.label_Robot.setStyleSheet(u"background-color: transparent")
        self.label_Robot.setAlignment(Qt.AlignCenter)

        self.imgRobot = cv2.imread("C:/Users/TB-4H/OneDrive/Desktop/Devel/TumiRobot.png")
        #self.imgRobotQ = self.convert_cv_qt3(self.imgRobot)
        self.label_Robot.setStyleSheet(u"QLabel {\n"
"       background-color: transparent;\n"
"       border-radius: 5px;\n"
"       background-image: url(C:/Users/TB-4H/OneDrive/Desktop/Devel/TumiRobot1.png);\n"
"}")

        self.layout_Robot.addWidget(self.label_Robot,0,Qt.AlignCenter)

        self.layout_BackPart.addWidget(self.frame_Robot,0,Qt.AlignCenter)

        self.frame_Control = QFrame(self.frameBackPart)
        self.frame_Control.setObjectName(u"frame_Control")
        self.frame_Control.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_Control.setFrameShape(QFrame.NoFrame)
        self.frame_Control.setFrameShadow(QFrame.Raised)

        self.layout_Control = QHBoxLayout(self.frame_Control)
        self.layout_Control.setObjectName(u"layout_Control")
        self.layout_Control.setSpacing(0)
        self.layout_Control.setContentsMargins(0,0,0,0)

        self.frame_StarCom = QFrame(self.frame_Control)
        self.frame_StarCom.setObjectName(u"frame_StarCom")
        self.frame_StarCom.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 10px;\n"
"}")
        self.frame_StarCom.setFrameShape(QFrame.NoFrame)
        self.frame_StarCom.setFrameShadow(QFrame.Raised)

        self.layout_StarCom = QHBoxLayout(self.frame_StarCom)
        self.layout_StarCom.setObjectName(u"layout_StarCom")
        self.layout_StarCom.setSpacing(10)
        self.layout_StarCom.setAlignment(Qt.AlignCenter)
        self.layout_StarCom.setContentsMargins(10,10,10,10)

        self.frame_Start = QFrame(self.frame_StarCom)
        self.frame_Start.setObjectName(u"frame_Start")
        self.frame_Start.setStyleSheet(u"background-color: rgb(98,103,111);")
        self.frame_Start.setFrameShape(QFrame.NoFrame)
        self.frame_Start.setFrameShadow(QFrame.Raised)

        self.layout_Start = QVBoxLayout(self.frame_Start)
        self.layout_Start.setObjectName(u"layout_Start")
        self.layout_Start.setSpacing(1)
        self.layout_Start.setContentsMargins(0, 0, 0, 0)

        self.Star_btn = QPushButton(self.frame_Start)
        self.Star_btn.setObjectName(u"Star_btn")
        self.Star_btn.setStyleSheet(u"QPushButton {     \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 18px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        icon_Start = QIcon()
        icon_Start.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-power-standby.png")
        self.Star_btn.setIcon(icon_Start)
        #self.Star_btn.clicked.connect(self.Star_con)

        self.layout_Start.addWidget(self.Star_btn,0,Qt.AlignCenter)

        self.frame_Com = QFrame(self.frame_StarCom)
        self.frame_Com.setObjectName(u"frame_Com")
        self.frame_Com.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_Com.setFrameShape(QFrame.NoFrame)
        self.frame_Com.setFrameShadow(QFrame.Raised)

        self.layout_com = QVBoxLayout(self.frame_Com)
        self.layout_com.setObjectName(u"layout_com")
        self.layout_com.setAlignment(Qt.AlignCenter)
        self.layout_com.setSpacing(0)
        self.layout_com.setContentsMargins(0, 0, 0, 0)

        self.frame_Exp = QFrame(self.frame_Com)
        self.frame_Exp.setObjectName(u"frame_Exp")
        self.frame_Exp.setStyleSheet(u"QFrame {\n"
"       background-color: transparent;\n"
"       border-radius: 0px;\n"
"}")
        self.frame_Exp.setFrameShape(QFrame.NoFrame)
        self.frame_Exp.setFrameShadow(QFrame.Raised)

        self.layout_Exp = QHBoxLayout(self.frame_Exp)
        self.layout_Exp.setObjectName(u"layout_Exp")
        self.layout_Exp.setSpacing(20)
        self.layout_Exp.setAlignment(Qt.AlignCenter)
        self.layout_Exp.setContentsMargins(0, 0, 0, 0)

        self.ExpCom1 = QLineEdit(self.frame_Exp)
        self.ExpCom1.setStyleSheet(u"QLineEdit {\n"
"       background-color: rgb(255,255,255);\n"
"       border-style: solid;\n"
"       border-width: 6px;\n"
"       border-radius: 8px;\n"
"       border-color: rgb(27,29,35);\n"
"       color: rgb(0,0,0);\n"
"}")
        self.ExpCom1.setMaxLength(16)
        self.ExpCom1.setFont(font8)
        self.ExpCom1.clear()

        self.Send_btn = QPushButton(self.frame_Exp)
        self.Send_btn.setObjectName(u"Send_btn")
        self.Send_btn.setStyleSheet(u"QPushButton {     \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 14px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        icon_Send = QIcon()
        icon_Send.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-arrow-circle-right.png")
        self.Send_btn.setIcon(icon_Send)
        #self.Star_btn.clicked.connect(self.Star_con)

        self.layout_Exp.addWidget(self.ExpCom1,0,Qt.AlignCenter)
        self.layout_Exp.addWidget(self.Send_btn,0,Qt.AlignCenter)

        self.frame_deb = QFrame(self.frame_Com)
        self.frame_deb.setObjectName(u"frame_deb")
        self.frame_deb.setStyleSheet(u"background-color: transparent;")
        self.frame_deb.setFrameShape(QFrame.NoFrame)
        self.frame_deb.setFrameShadow(QFrame.Raised)

        self.layout_deb = QVBoxLayout(self.frame_deb)
        self.layout_deb.setObjectName(u"layout_deb")
        self.layout_deb.setSpacing(1)
        self.layout_deb.setAlignment(Qt.AlignCenter)
        self.layout_deb.setContentsMargins(0, 0, 0, 0)
#$OAX01
        self.ExpCom = QPlainTextEdit(self.frame_Exp)
        self.ExpCom.setStyleSheet(u"QPlainTextEdit {\n"
"       background-color: rgb(255,255,255);\n"
"       border-style: solid;\n"
"       border-width: 6px;\n"
"       border-radius: 8px;\n"
"       border-color: rgb(27,29,35);\n"
"       color: rgb(0,0,0);\n"
"}")
        self.ExpCom.setFont(font8)
        self.ExpCom.clear()

        self.layout_deb.addWidget(self.ExpCom,0,Qt.AlignCenter)

        self.layout_com.addWidget(self.frame_Exp)
        self.layout_com.addWidget(self.frame_deb)

        self.layout_StarCom.addWidget(self.frame_Start,0,Qt.AlignCenter)
        self.layout_StarCom.addWidget(self.frame_Com,0,Qt.AlignCenter)

        self.frame_VidInd = QFrame(self.frame_Control)
        self.frame_VidInd.setObjectName(u"frame_VidInd")
        self.frame_VidInd.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 10px;\n"
"}")
        self.frame_VidInd.setFrameShape(QFrame.NoFrame)
        self.frame_VidInd.setFrameShadow(QFrame.Raised)

        self.layout_VidInd = QVBoxLayout(self.frame_VidInd)
        self.layout_VidInd.setObjectName(u"layout_VidInd")
        self.layout_VidInd.setSpacing(5)

        self.frame_Vid = QFrame(self.frame_VidInd)
        self.frame_Vid.setObjectName(u"frame_Vid")
        self.frame_Vid.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_Vid.setFrameShape(QFrame.NoFrame)
        self.frame_Vid.setFrameShadow(QFrame.Raised)

        self.layout_Vid = QHBoxLayout(self.frame_Vid)
        self.layout_Vid.setObjectName(u"layout_Vid")
        self.layout_Vid.setAlignment(Qt.AlignCenter)
        self.layout_Vid.setSpacing(10)
        self.layout_Vid.setContentsMargins(0,0,0,0)

        self.frame_VidIzq = QFrame(self.frame_Vid)
        self.frame_VidIzq.setObjectName(u"frame_VidIzq")
        self.frame_VidIzq.setStyleSheet(u"background-color: rgb(98,103,111);")
        self.frame_VidIzq.setFrameShape(QFrame.NoFrame)
        self.frame_VidIzq.setFrameShadow(QFrame.Raised)

        self.layout_VidIzq = QHBoxLayout(self.frame_VidIzq)
        self.layout_VidIzq.setObjectName(u"layout_VidIzq")
        self.layout_VidIzq.setSpacing(25)
        self.layout_VidIzq.setAlignment(Qt.AlignCenter)
        self.layout_VidIzq.setContentsMargins(0, 0, 0, 0)

        self.Rec_btn = QPushButton(self.frame_VidIzq)
        self.Rec_btn.setObjectName(u"Rec_btn")
        self.Rec_btn.setStyleSheet(u"QPushButton {      \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconRecIzq = QIcon()
        iconRecIzq.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-media-record.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Rec_btn.setIcon(iconRecIzq)

        self.Set_btn = QPushButton(self.frame_VidIzq)
        self.Set_btn.setObjectName(u"Set_btn")
        self.Set_btn.setStyleSheet(u"QPushButton {      \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconSecIzq = QIcon()
        iconSecIzq.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-camera.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Set_btn.setIcon(iconSecIzq)

        self.Gen_btn = QPushButton(self.frame_VidIzq)
        self.Gen_btn.setObjectName(u"Gen_btn")
        self.Gen_btn.setStyleSheet(u"QPushButton {      \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(53,59,72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconGenIzq = QIcon()
        iconGenIzq.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Gen_btn.setIcon(iconGenIzq)

        self.layout_VidIzq.addWidget(self.Rec_btn,0,Qt.AlignCenter)
        self.layout_VidIzq.addWidget(self.Set_btn,0,Qt.AlignCenter)
        self.layout_VidIzq.addWidget(self.Gen_btn,0,Qt.AlignCenter)

        self.frame_VidCen = QFrame(self.frame_Vid)
        self.frame_VidCen.setObjectName(u"frame_VidCen")
        self.frame_VidCen.setStyleSheet(u"background-color: rgb(98,103,111);")
        self.frame_VidCen.setFrameShape(QFrame.NoFrame)
        self.frame_VidCen.setFrameShadow(QFrame.Raised)

        self.layout_VidCen = QHBoxLayout(self.frame_VidCen)
        self.layout_VidCen.setObjectName(u"layout_VidCen")
        self.layout_VidCen.setSpacing(10)
        self.layout_VidCen.setAlignment(Qt.AlignCenter)
        self.layout_VidCen.setContentsMargins(0, 0, 0, 0)

        self.Rec_btnCen = QPushButton(self.frame_VidCen)
        self.Rec_btnCen.setObjectName(u"Rec_btnCen")
        self.Rec_btnCen.setStyleSheet(u"QPushButton {   \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconRecCen = QIcon()
        iconRecCen.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-media-record.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Rec_btnCen.setIcon(iconRecCen)

        self.Gen_btnCen = QPushButton(self.frame_VidCen)
        self.Gen_btnCen.setObjectName(u"Send_btn")
        self.Gen_btnCen.setStyleSheet(u"QPushButton {   \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconGenCen = QIcon()
        iconGenCen.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Gen_btnCen.setIcon(iconGenCen)

        self.layout_VidCen.addWidget(self.Rec_btnCen,0,Qt.AlignCenter)
        self.layout_VidCen.addWidget(self.Gen_btnCen,0,Qt.AlignCenter)

        self.frame_VidDer = QFrame(self.frame_Vid)
        self.frame_VidDer.setObjectName(u"frame_VidDer")
        self.frame_VidDer.setStyleSheet(u"background-color: rgb(98,103,111);")
        self.frame_VidDer.setFrameShape(QFrame.NoFrame)
        self.frame_VidDer.setFrameShadow(QFrame.Raised)

        self.layout_VidDer = QHBoxLayout(self.frame_VidDer)
        self.layout_VidDer.setObjectName(u"layout_VidDer")
        self.layout_VidDer.setSpacing(25)
        self.layout_VidDer.setAlignment(Qt.AlignCenter)
        self.layout_VidDer.setContentsMargins(0, 0, 0, 0)

        self.Rec_btnDer = QPushButton(self.frame_VidDer)
        self.Rec_btnDer.setObjectName(u"Rec_btnDer")
        self.Rec_btnDer.setStyleSheet(u"QPushButton {   \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconRecDer = QIcon()
        iconRecDer.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-media-record.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Rec_btnDer.setIcon(iconRecDer)

        self.Set_btnDer = QPushButton(self.frame_VidDer)
        self.Set_btnDer.setObjectName(u"Set_btnDer")
        self.Set_btnDer.setStyleSheet(u"QPushButton {   \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconSetDer = QIcon()
        iconSetDer.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-camera.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Set_btnDer.setIcon(iconSetDer)

        self.Gen_btnDer = QPushButton(self.frame_VidDer)
        self.Gen_btnDer.setObjectName(u"Gen_btnDer")
        self.Gen_btnDer.setStyleSheet(u"QPushButton {   \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        iconGenDer = QIcon()
        iconGenDer.addFile(u"C:/Users/TUMI Robotics/Desktop/Chatibotv1/icons/24x24/cil-settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Gen_btnDer.setIcon(iconGenDer)

        self.layout_VidDer.addWidget(self.Rec_btnDer,0,Qt.AlignCenter)
        self.layout_VidDer.addWidget(self.Set_btnDer,0,Qt.AlignCenter)
        self.layout_VidDer.addWidget(self.Gen_btnDer,0,Qt.AlignCenter)

        self.layout_Vid.addWidget(self.frame_VidIzq,0,Qt.AlignCenter)
        self.layout_Vid.addWidget(self.frame_VidCen,0,Qt.AlignCenter)
        self.layout_Vid.addWidget(self.frame_VidDer,0,Qt.AlignCenter)

        self.frame_Ind = QFrame(self.frame_VidInd)
        self.frame_Ind.setObjectName(u"frame_Ind")
        self.frame_Ind.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 12px;\n"
"}")
        self.frame_Ind.setFrameShape(QFrame.NoFrame)
        self.frame_Ind.setFrameShadow(QFrame.Raised)

        self.layout_Ind = QHBoxLayout(self.frame_Ind)
        self.layout_Ind.setObjectName(u"layout_Ind")
        self.layout_Ind.setSpacing(4)
        self.layout_Ind.setAlignment(Qt.AlignCenter)
        self.layout_Ind.setContentsMargins(0, 0, 0, 0)

        self.frame_Vel = QFrame(self.frame_Ind)
        self.frame_Vel.setObjectName(u"frame_Vel")
        self.frame_Vel.setStyleSheet(u"QFrame {\n"
"       background-color: transparent;\n"
"       border-radius: 8px;\n"
"}")
        self.frame_Vel.setFrameShape(QFrame.NoFrame)
        self.frame_Vel.setFrameShadow(QFrame.Raised)

        self.layout_Vel = QVBoxLayout(self.frame_Vel)
        self.layout_Vel.setObjectName(u"layout_Vel")
        self.layout_Vel.setSpacing(10)
        self.layout_Vel.setAlignment(Qt.AlignCenter)
        self.layout_Vel.setContentsMargins(0, 0, 0, 0)

        self.frame1 = QFrame(self.frame_Vel)
        self.frame1.setObjectName(u"frame1")
        self.frame1.setStyleSheet(u"background-color: transparent;")
        self.frame1.setFrameShape(QFrame.NoFrame)
        self.frame1.setFrameShadow(QFrame.Raised)

        self.layout_f1 = QHBoxLayout(self.frame1)
        self.layout_f1.setObjectName(u"layout_f1")
        self.layout_f1.setSpacing(0)
        self.layout_f1.setContentsMargins(5,0,5,0)

        self.Bat_Lab = QLabel(self.frame1)
        self.Bat_Lab.setStyleSheet(u"background-color: transparent")
        self.Bat_Lab.setFont(font3)
        self.Bat_Lab.setAlignment(Qt.AlignLeft)
        self.Bat_Lab.setText(u"BATTERY")

        self.BatInd_Lab = QLabel(self.frame1)
        self.BatInd_Lab.setStyleSheet(u"background-color: transparent")
        self.BatInd_Lab.setFont(font3)
        self.BatInd_Lab.setAlignment(Qt.AlignLeft)
        self.BatInd_Lab.setText(u":   0.0")

        self.layout_f1.addWidget(self.Bat_Lab,0,Qt.AlignLeft)
        self.layout_f1.addWidget(self.BatInd_Lab,0,Qt.AlignLeft)

        self.frame2 = QFrame(self.frame_Vel)
        self.frame2.setObjectName(u"frame2")
        self.frame2.setStyleSheet(u"background-color: transparent;")
        self.frame2.setFrameShape(QFrame.NoFrame)
        self.frame2.setFrameShadow(QFrame.Raised)

        self.Bat_Pro = QProgressBar(self.frame2)
        self.Bat_Pro.setObjectName(u"Bat_Pro")
        self.Bat_Pro.setMaximum(100)
        self.Bat_Pro.setValue(0)
        self.Bat_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 5px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")

        self.frame3 = QFrame(self.frame_Vel)
        self.frame3.setObjectName(u"frame3")
        self.frame3.setStyleSheet(u"background-color: transparent;")
        self.frame3.setFrameShape(QFrame.NoFrame)
        self.frame3.setFrameShadow(QFrame.Raised)

        self.layout_f3 = QHBoxLayout(self.frame3)
        self.layout_f3.setObjectName(u"layout_f3")
        self.layout_f3.setSpacing(0)
        self.layout_f3.setContentsMargins(5,0,5,0)

        self.Spe_Lab = QLabel(self.frame3)
        self.Spe_Lab.setStyleSheet(u"background-color: transparent")
        self.Spe_Lab.setFont(font3)
        self.Spe_Lab.setAlignment(Qt.AlignLeft)
        self.Spe_Lab.setText(u"SPEED")

        self.SpeInd_Lab = QLabel(self.frame3)
        self.SpeInd_Lab.setStyleSheet(u"background-color: transparent")
        self.SpeInd_Lab.setFont(font3)
        self.SpeInd_Lab.setAlignment(Qt.AlignLeft)
        self.SpeInd_Lab.setText(u":   HIGH")

        self.layout_f3.addWidget(self.Spe_Lab,0,Qt.AlignLeft)
        self.layout_f3.addWidget(self.SpeInd_Lab,0,Qt.AlignLeft)

        self.frame4 = QFrame(self.frame_Vel)
        self.frame4.setObjectName(u"frame4")
        self.frame4.setStyleSheet(u"background-color: transparent;")
        self.frame4.setFrameShape(QFrame.NoFrame)
        self.frame4.setFrameShadow(QFrame.Raised)

        self.Spe_Pro = QProgressBar(self.frame4)
        self.Spe_Pro.setObjectName(u"Spe_Pro")
        self.Spe_Pro.setMaximum(100)
        self.Spe_Pro.setValue(0)
        self.Spe_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 5px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")

        self.frame5 = QFrame(self.frame_Vel)
        self.frame5.setObjectName(u"frame5")
        self.frame5.setStyleSheet(u"background-color: transparent;")
        self.frame5.setFrameShape(QFrame.NoFrame)
        self.frame5.setFrameShadow(QFrame.Raised)

        self.layout_f5 = QHBoxLayout(self.frame5)
        self.layout_f5.setObjectName(u"layout_f5")
        self.layout_f5.setSpacing(0)
        self.layout_f5.setContentsMargins(5,0,5,0)

        self.Lig_Lab = QLabel(self.frame5)
        self.Lig_Lab.setStyleSheet(u"background-color: transparent")
        self.Lig_Lab.setFont(font3)
        self.Lig_Lab.setAlignment(Qt.AlignLeft)
        self.Lig_Lab.setText(u"LIGHT")

        self.LigInd_Lab = QLabel(self.frame5)
        self.LigInd_Lab.setStyleSheet(u"background-color: transparent")
        self.LigInd_Lab.setFont(font3)
        self.LigInd_Lab.setAlignment(Qt.AlignLeft)
        self.LigInd_Lab.setText(u":   ON")

        self.layout_f5.addWidget(self.Lig_Lab,0,Qt.AlignLeft)
        self.layout_f5.addWidget(self.LigInd_Lab,0,Qt.AlignLeft)

        self.frame6 = QFrame(self.frame_Vel)
        self.frame6.setObjectName(u"frame6")
        self.frame6.setStyleSheet(u"background-color: transparent;")
        self.frame6.setFrameShape(QFrame.NoFrame)
        self.frame6.setFrameShadow(QFrame.Raised)

        self.Lig_Pro = QProgressBar(self.frame6)
        self.Lig_Pro.setObjectName(u"Lig_Pro")
        self.Lig_Pro.setMaximum(100)
        self.Lig_Pro.setValue(0)
        self.Lig_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 5px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")

        self.layout_Vel.addWidget(self.frame1,0,Qt.AlignCenter)
        self.layout_Vel.addWidget(self.frame2,0,Qt.AlignCenter)
        self.layout_Vel.addWidget(self.frame3,0,Qt.AlignCenter)
        self.layout_Vel.addWidget(self.frame4,0,Qt.AlignCenter)
        self.layout_Vel.addWidget(self.frame5,0,Qt.AlignCenter)
        self.layout_Vel.addWidget(self.frame6,0,Qt.AlignCenter)

        self.frame_Est = QFrame(self.frame_Ind)
        self.frame_Est.setObjectName(u"frame_Est")
        self.frame_Est.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 4px;\n"
"}")
        self.frame_Est.setFrameShape(QFrame.NoFrame)
        self.frame_Est.setFrameShadow(QFrame.Raised)

        self.layout_Est = QVBoxLayout(self.frame_Est)
        self.layout_Est.setObjectName(u"layout_Est")
        self.layout_Est.setSpacing(12.5)
        self.layout_Est.setAlignment(Qt.AlignCenter)
        self.layout_Est.setContentsMargins(0, 0, 0, 0)

        self.frame12 = QFrame(self.frame_Est)
        self.frame12.setObjectName(u"frame12")
        self.frame12.setStyleSheet(u"background-color: transparent;")
        self.frame12.setFrameShape(QFrame.NoFrame)
        self.frame12.setFrameShadow(QFrame.Raised)

        self.layout_f12 = QHBoxLayout(self.frame12)
        self.layout_f12.setObjectName(u"layout_f12")
        self.layout_f12.setSpacing(0)
        self.layout_f12.setAlignment(Qt.AlignVCenter)
        self.layout_f12.setContentsMargins(5,0,5,0)

        self.Tit_Ind = QLabel(self.frame12)
        self.Tit_Ind.setStyleSheet(u"background-color: transparent")
        self.Tit_Ind.setFont(font3)
        self.Tit_Ind.setAlignment(Qt.AlignLeft)
        self.Tit_Ind.setText(u"JOYSTICK")

        self.Joy_Pro = QProgressBar(self.frame12)
        self.Joy_Pro.setObjectName(u"Rpi_Pro")
        self.Joy_Pro.setMaximum(100)
        self.Joy_Pro.setValue(0)
        self.Joy_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 8px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")
        self.Joy_Pro.setTextVisible(False)

        self.layout_f12.addWidget(self.Tit_Ind,0,Qt.AlignLeft)

        self.frame22 = QFrame(self.frame_Est)
        self.frame22.setObjectName(u"frame22")
        self.frame22.setStyleSheet(u"background-color: transparent;")
        self.frame22.setFrameShape(QFrame.NoFrame)
        self.frame22.setFrameShadow(QFrame.Raised)

        self.layout_f22 = QHBoxLayout(self.frame22)
        self.layout_f22.setObjectName(u"layout_f22")
        self.layout_f22.setSpacing(0)
        self.layout_f22.setAlignment(Qt.AlignVCenter)
        self.layout_f22.setContentsMargins(5,0,5,0)

        self.Rsp_Ind = QLabel(self.frame22)
        self.Rsp_Ind.setStyleSheet(u"background-color: transparent")
        self.Rsp_Ind.setFont(font3)
        self.Rsp_Ind.setAlignment(Qt.AlignLeft)
        self.Rsp_Ind.setText(u"RASPBERRY PI")

        self.Rpi_Pro = QProgressBar(self.frame22)
        self.Rpi_Pro.setObjectName(u"Rpi_Pro")
        self.Rpi_Pro.setMaximum(100)
        self.Rpi_Pro.setValue(0)
        self.Rpi_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 8px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")
        self.Rpi_Pro.setTextVisible(False)

        self.layout_f22.addWidget(self.Rsp_Ind,0,Qt.AlignLeft)

        self.frame32 = QFrame(self.frame_Est)
        self.frame32.setObjectName(u"frame32")
        self.frame32.setStyleSheet(u"background-color: transparent;")
        self.frame32.setFrameShape(QFrame.NoFrame)
        self.frame32.setFrameShadow(QFrame.Raised)

        self.layout_f32 = QHBoxLayout(self.frame32)
        self.layout_f32.setObjectName(u"layout_f32")
        self.layout_f32.setSpacing(0)
        self.layout_f32.setAlignment(Qt.AlignVCenter)
        self.layout_f32.setContentsMargins(5,0,5,0)

        self.Nuc_Ind = QLabel(self.frame12)
        self.Nuc_Ind.setStyleSheet(u"background-color: transparent")
        self.Nuc_Ind.setFont(font3)
        self.Nuc_Ind.setAlignment(Qt.AlignLeft)
        self.Nuc_Ind.setText(u"LiDAR")

        self.Nuc_Pro = QProgressBar(self.frame32)
        self.Nuc_Pro.setObjectName(u"Nuc_Pro")
        self.Nuc_Pro.setMaximum(100)
        self.Nuc_Pro.setValue(0)
        self.Nuc_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 8px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")
        self.Nuc_Pro.setTextVisible(False)

        self.layout_f32.addWidget(self.Nuc_Ind,0,Qt.AlignLeft)

        self.frame42 = QFrame(self.frame_Est)
        self.frame42.setObjectName(u"frame42")
        self.frame42.setStyleSheet(u"background-color: transparent;")
        self.frame42.setFrameShape(QFrame.NoFrame)
        self.frame42.setFrameShadow(QFrame.Raised)

        self.layout_f42 = QHBoxLayout(self.frame42)
        self.layout_f42.setObjectName(u"layout_f42")
        self.layout_f42.setSpacing(0)
        self.layout_f42.setAlignment(Qt.AlignVCenter)
        self.layout_f42.setContentsMargins(5,0,5,0)

        self.CamS_Ind = QLabel(self.frame42)
        self.CamS_Ind.setStyleSheet(u"background-color: transparent")
        self.CamS_Ind.setFont(font3)
        self.CamS_Ind.setAlignment(Qt.AlignLeft)
        self.CamS_Ind.setText(u"CAMERAS")

        self.CamS_Pro = QProgressBar(self.frame42)
        self.CamS_Pro.setObjectName(u"CamS_Pro")
        self.CamS_Pro.setMaximum(100)
        self.CamS_Pro.setValue(0)
        self.CamS_Pro.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(27, 29, 35);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-radius: 8px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 5px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(244, 70, 17, 255), stop:1 rgba(255, 128, 0, 255));\n"
"}")
        self.CamS_Pro.setTextVisible(False)

        self.layout_f42.addWidget(self.CamS_Ind,0,Qt.AlignLeft)

        self.frame52 = QFrame(self.frame_Est)
        self.frame52.setObjectName(u"frame52")
        self.frame52.setStyleSheet(u"background-color: transparent;")
        self.frame52.setFrameShape(QFrame.NoFrame)
        self.frame52.setFrameShadow(QFrame.Raised)

        self.layout_f52 = QHBoxLayout(self.frame52)
        self.layout_f52.setObjectName(u"layout_f52")
        self.layout_f52.setSpacing(0)
        self.layout_f52.setAlignment(Qt.AlignVCenter)
        self.layout_f52.setContentsMargins(5,0,5,0)

        self.Lid_Ind = QLabel(self.frame52)
        self.Lid_Ind.setStyleSheet(u"background-color: transparent")
        self.Lid_Ind.setFont(font3)
        self.Lid_Ind.setAlignment(Qt.AlignLeft)
        self.Lid_Ind.setText(u"LiDAR")

        self.Lid_Cou = QLabel(self.frame52)
        self.Lid_Cou.setStyleSheet(u"QLabel {\n"
"       background-color: rgb(0,0,0);\n"
"       border-style: solid;\n"
"       border-width: 2px;\n"
"       border-color: rgb(255,255,255);\n"
"       border-radius: 10px;\n"
"}")
        self.Lid_Cou.setFont(font3)
        self.Lid_Cou.setAlignment(Qt.AlignCenter)
        self.Lid_Cou.setText(u"Counter")

        self.layout_f52.addWidget(self.Lid_Ind,0,Qt.AlignLeft)
        self.layout_f52.addWidget(self.Lid_Cou,0,Qt.AlignRight)

        self.layout_Est.addWidget(self.frame12,0,Qt.AlignCenter)
        self.layout_Est.addWidget(self.frame22,0,Qt.AlignCenter)
        self.layout_Est.addWidget(self.frame32,0,Qt.AlignCenter)
        self.layout_Est.addWidget(self.frame42,0,Qt.AlignCenter)
        self.layout_Est.addWidget(self.frame52,0,Qt.AlignCenter)

        self.layout_Ind.addWidget(self.frame_Vel,0,Qt.AlignCenter)
        self.layout_Ind.addWidget(self.frame_Est,0,Qt.AlignCenter)

        self.layout_VidInd.addWidget(self.frame_Vid,0,Qt.AlignCenter)
        self.layout_VidInd.addWidget(self.frame_Ind,0,Qt.AlignCenter)

        self.frame_Report = QFrame(self.frame_Control)
        self.frame_Report.setObjectName(u"frame_Report")
        self.frame_Report.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 10px;\n"
"}")
        self.frame_Report.setFrameShape(QFrame.NoFrame)
        self.frame_Report.setFrameShadow(QFrame.Raised)

        self.layout_Report = QVBoxLayout(self.frame_Report)
        self.layout_Report.setObjectName(u"layout_Report")
        self.layout_Report.setSpacing(5)

        self.frame_Ent = QFrame(self.frame_Report)
        self.frame_Ent.setObjectName(u"frame_Ent")
        self.frame_Ent.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_Ent.setFrameShape(QFrame.NoFrame)
        self.frame_Ent.setFrameShadow(QFrame.Raised)

        self.layout_Ent = QVBoxLayout(self.frame_Ent)
        self.layout_Ent.setObjectName(u"layout_Ent")
        self.layout_Ent.setSpacing(1)
        self.layout_Ent.setAlignment(Qt.AlignCenter)
        self.layout_Ent.setContentsMargins(0, 0, 0, 0)

        self.EntRep = QPlainTextEdit(self.frame_Ent)
        self.EntRep.setStyleSheet(u"QPlainTextEdit {\n"
"       background-color: rgb(255,255,255);\n"
"       border-style: solid;\n"
"       border-width: 6px;\n"
"       border-radius: 8px;\n"
"       border-color: rgb(27,29,35);\n"
"       color: rgb(0,0,0);\n"
"}")
        self.EntRep.setFont(font8)
        self.EntRep.clear()

        self.layout_Ent.addWidget(self.EntRep,0, Qt.AlignCenter)

        self.frame_Rbtn = QFrame(self.frame_Report)
        self.frame_Rbtn.setObjectName(u"frame_Rbtn")
        self.frame_Rbtn.setStyleSheet(u"QFrame {\n"
"       background-color: rgb(98,103,111);\n"
"       border-radius: 15px;\n"
"}")
        self.frame_Rbtn.setFrameShape(QFrame.NoFrame)
        self.frame_Rbtn.setFrameShadow(QFrame.Raised)

        self.layout_Rbtn = QHBoxLayout(self.frame_Rbtn)
        self.layout_Rbtn.setObjectName(u"layout_Rbtn")
        self.layout_Rbtn.setAlignment(Qt.AlignCenter)
        self.layout_Rbtn.setSpacing(1)
        self.layout_Rbtn.setContentsMargins(0, 0, 0, 0)

        self.frame_btn_der = QFrame(self.frame_Rbtn)
        self.frame_btn_der.setObjectName(u"frame_btn_der")
        self.frame_btn_der.setStyleSheet(u"background-color: transparent;")
        self.frame_btn_der.setFrameShape(QFrame.NoFrame)
        self.frame_btn_der.setFrameShadow(QFrame.Raised)

        self.layout_btn_der = QHBoxLayout(self.frame_btn_der)
        self.layout_btn_der.setObjectName(u"layout_btn_der")
        self.layout_btn_der.setSpacing(1)
        self.layout_btn_der.setAlignment(Qt.AlignCenter)
        self.layout_btn_der.setContentsMargins(0, 0, 0, 0)

        self.Sav_btn = QPushButton(self.frame_btn_der)
        self.Sav_btn.setObjectName(u"Sav_btn")
        self.Sav_btn.setFont(font3)
        self.Sav_btn.setStyleSheet(u"QPushButton {      \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        self.Sav_btn.setText("Add")

        self.layout_btn_der.addWidget(self.Sav_btn,Qt.AlignCenter)

        self.frame_btn_izq = QFrame(self.frame_Rbtn)
        self.frame_btn_izq.setObjectName(u"frame_btn_izq")
        self.frame_btn_izq.setStyleSheet(u"background-color: transparent;")
        self.frame_btn_izq.setFrameShape(QFrame.NoFrame)
        self.frame_btn_izq.setFrameShadow(QFrame.Raised)

        self.layout_btn_izq = QHBoxLayout(self.frame_btn_izq)
        self.layout_btn_izq.setObjectName(u"layout_btn_izq")
        self.layout_btn_izq.setSpacing(1)
        self.layout_btn_izq.setAlignment(Qt.AlignCenter)
        self.layout_btn_izq.setContentsMargins(0, 0, 0, 0)

        self.Can_btn = QPushButton(self.frame_btn_izq)
        self.Can_btn.setObjectName(u"Can_btn")
        self.Can_btn.setFont(font3)
        self.Can_btn.setStyleSheet(u"QPushButton {      \n"
"       border-style: solid;\n"
"       background-color: rgb(27,29,35);\n"
"       border-radius: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {  \n"
"       background-color: rgb(85, 170, 255);\n"
"}")
        self.Can_btn.setText("Clear")

        self.layout_btn_izq.addWidget(self.Can_btn, Qt.AlignCenter)

        self.layout_Rbtn.addWidget(self.frame_btn_der,0,Qt.AlignCenter)
        self.layout_Rbtn.addWidget(self.frame_btn_izq,0,Qt.AlignCenter)

        self.layout_Report.addWidget(self.frame_Ent,0,Qt.AlignCenter)
        self.layout_Report.addWidget(self.frame_Rbtn,0,Qt.AlignCenter)

        self.layout_Control.addWidget(self.frame_StarCom,Qt.AlignCenter)
        self.layout_Control.addWidget(self.frame_VidInd,Qt.AlignCenter)
        self.layout_Control.addWidget(self.frame_Report,Qt.AlignCenter)

        self.layout_BackPart.addWidget(self.frame_Control,0,Qt.AlignCenter|Qt.AlignBottom)

        self.frame_Logo = QFrame(self.frameBackPart)
        self.frame_Logo.setObjectName(u"frame_Logo")
        self.frame_Logo.setStyleSheet(u"QFrame {\n"
"       background-color: transparent;\n"
"       border-radius: 5px;\n"
"}")
        self.frame_Logo.setFrameShape(QFrame.NoFrame)
        self.frame_Logo.setFrameShadow(QFrame.Raised)

        self.layout_Logo = QVBoxLayout(self.frame_Logo)
        self.layout_Logo.setObjectName(u"layout_Logo")
        self.layout_Logo.setSpacing(0)
        self.layout_Logo.setContentsMargins(0,0,0,0)

        self.label_Logo = QLabel(self.frame_Logo)
        self.label_Logo.setStyleSheet(u"background-color: transparent")
        self.label_Logo.setAlignment(Qt.AlignCenter)

        self.imgLogo = cv2.imread("C:/Users/TB-4H/OneDrive/Desktop/Devel/LogoTumi1.png")
        #self.imgRobotQ = self.convert_cv_qt3(self.imgRobot)
        self.label_Logo.setStyleSheet(u"QLabel {\n"
"       background-color: transparent;\n"
"       border-radius: 5px;\n"
"       background-image: url(C:/Users/TB-4H/OneDrive/Desktop/Devel/LogoTumi1.png);\n"
"}")

        self.layout_Logo.addWidget(self.label_Logo,0,Qt.AlignCenter)

        self.layout_BackPart.addWidget(self.frame_Logo,0,Qt.AlignCenter)

        self.vertical_home.addWidget(self.frameBackPart,0,Qt.AlignCenter)

        self.ScrollArea = QScrollArea()
        self.ScrollArea.setWidget(self.page_home)
        self.ScrollArea.setWidgetResizable(True)
        self.stackedWidget.addWidget(self.ScrollArea)
        self.verticalLayout_9.addWidget(self.stackedWidget)
        self.verticalLayout_4.addWidget(self.frame_content)

        #Se define el frame_grip con los creditos
        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)

        #Se define el Layout horizontal para el Frame_Grip
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)

        #Se define el frame para el label bottom
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)

        #Se define el Layout para el frame
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)

        #Se crea el label para creditos y se añade al layout parent
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font2)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.horizontalLayout_7.addWidget(self.label_credits)

        #Se crea el label para la version y se añade al layout parent
        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        self.label_version.setFont(font2)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.horizontalLayout_7.addWidget(self.label_version,1,Qt.AlignRight)
        self.horizontalLayout_6.addWidget(self.frame_label_bottom)

        #Se crea el ultimo frame chiquito de la parte inferior derecha
        self.frame_size_grip = QFrame(self.frame_grip)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
"       background-image: url(:/16x16/icons/16x16/cil-size-grip.png);\n"
"       background-position: center;\n"
"       background-repeat: no-reperat;\n"
"}")
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        #Se añade todo al layout parent
        self.horizontalLayout_6.addWidget(self.frame_size_grip)
        self.verticalLayout_4.addWidget(self.frame_grip)
        self.horizontalLayout_2.addWidget(self.frame_content_right)
        self.verticalLayout.addWidget(self.frame_center)
        self.horizontalLayout.addWidget(self.frame_main)

        #Se finaliza la implementaciòn colocando el central widget en la pantalla
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)
        self.stackedWidget.setCurrentIndex(0)

        #Finalizacion de la descripcion de los Widgets de la interfaz
        QWidget.setTabOrder(self.btn_minimize, self.btn_maximize_restore)
        QWidget.setTabOrder(self.btn_maximize_restore, self.btn_close)
        QWidget.setTabOrder(self.btn_close, self.btn_toggle_menu)
        self.retranslateUI()
        self.resizeWidgets()

        #Declaracion de metodos asociados a botones, procesos y emision de senales
        self.Star_btn.clicked.connect(self.StartEndConexion)
        self.debugTextMain.connect(self.ActualizarLabel)

    def StartEndConexion(self):
        global CONN
        wd=os.getcwd()
        print("La direccion es: ",wd)
        if CONN == 0:
            CONN = 1
            numDir = 1
            countList = 0

            contenido = os.listdir(wd)
            while countList < len(contenido):
                nombreDir = "pok" + str(numDir)
                if(contenido[countList] == nombreDir):
                    numDir = numDir + 1
                    countList = 0
                else:
                    countList = countList + 1
            numDir_1=numDir+1

            self.debugTextMain.emit("Se creara el servicio de conexion con el joystick")
            self.thread1 = ComunicationJy()
            self.thread1.textUp.connect(self.ActualizarLabel)
            self.thread1.start()
            self.debugTextMain.emit("Servicio de conexion creado correctamente")
            self.debugTextMain.emit("Se inician las camaras para conexion")
            self.LecturaCam1 = multiprocessing.Process(target= camera1Recv,args = (numDir,wd,))
            self.LecturaCam2 = multiprocessing.Process(target= camera2Recv,args = (numDir_1,wd,))
            self.LecturaCam1.start()
            self.LecturaCam2.start()
            self.debugTextMain.emit("Camaras iniciadas correctamente")
            self.updateImg.start(0.025)
            self.updateImg2.start(0.025)
            self.debugTextMain.emit("Conexion realizada correctamente")
            self.debugTextMain.emit("Todos los servicios se encuentran corriendo")
        else:
            CONN = 0
            time.sleep(2)
            self.debugTextMain.emit("Se finalizaran todos los servicios")
            self.updateImg.stop()
            self.updateImg2.stop()
            self.debugTextMain.emit("Servicio de cámaras eliminandoes")
            self.LecturaCam1.kill()
            self.LecturaCam2.kill()
            #self.LecturaCam1.wait()
            #self.LecturaCam2.wait()
            self.debugTextMain.emit("Las camaras se han eliminado")
            self.thread1.terminate()
            self.thread1.wait()
            self.debugTextMain.emit("La conexión con el robot se ha cerrado")

    def retranslateUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"TUMI Robotics App", None))
        self.btn_toggle_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("MainWindow", u"TUMI ROBOTICS", None))
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.btn_minimize.setText("")
        self.btn_maximize_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        self.btn_maximize_restore.setText("")
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        self.btn_close.setText("")
        self.label_top_info_1.setText(QCoreApplication.translate("MainWindow", u"Ruta del proyecto", None))
        self.label_top_info_2.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.label_user_icon.setText(QCoreApplication.translate("MainWindow", u"T", None))
        self.label_credits.setText(QCoreApplication.translate("MainWindow", u"Registered by: Luis Turpo, Alexander Segovia", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))

    def resizeWidgets(self):

        screen = QDesktopWidget().screenGeometry()
        SizeFlag = 0

        if screen.width() > 1060 :
            SizeFlag = 1

        if screen.width() > 1300 :
            SizeFlag = 2

        if screen.width() > 1650 :
            SizeFlag = 3

        if screen.width() > 2000 :
            SizeFlag = 4


        if SizeFlag == 0:
            self.resize(1050,700)
            self.setMinimumSize(1050,700)

        if SizeFlag == 1:
            self.resize(1350,900)
            self.setMinimumSize(1350,900)

        if SizeFlag == 2:
            self.resize(1800,1200)
            self.setMinimumSize(1800,1200)
            self.frame_camaras.setMinimumSize(QSize(1650,630))
            self.frame_camaras.setMaximumSize(QSize(1650,630))
            self.frame_cam1.setMinimumSize(QSize(800,600))
            self.frame_cam1.setMaximumSize(QSize(800,600))
            self.frame_cam2.setMinimumSize(QSize(800,600))
            self.frame_cam2.setMaximumSize(QSize(800,600))
            self.labelCam1_Idf.setMinimumSize(QSize(300,20))
            self.labelCam1_Idf.setMaximumSize(QSize(300,20))
            self.label_camera1.setMaximumSize(QSize(750,550))
            self.label_camera1.setMinimumSize(QSize(750,550))
            self.labelCam2_Idf.setMinimumSize(QSize(300,20))
            self.labelCam2_Idf.setMaximumSize(QSize(300,20))
            self.label_camera2.setMaximumSize(QSize(750,550))
            self.label_camera2.setMinimumSize(QSize(750,550))
            self.frameBackPart.setMinimumSize(QSize(1600,260))
            self.frameBackPart.setMaximumSize(QSize(1600,260))
            self.frame_Logo.setMaximumSize(QSize(190,210))
            self.frame_Logo.setMinimumSize(QSize(190,210))
            self.frame_Robot.setMaximumSize(QSize(190,210))
            self.frame_Robot.setMinimumSize(QSize(190,210))
            self.frame_Control.setMinimumSize(QSize(1200,230))
            self.frame_Control.setMaximumSize(QSize(1200,230))
            self.frame_StarCom.setMinimumSize(QSize(350,230))
            self.frame_StarCom.setMaximumSize(QSize(350,230))
            self.frame_VidInd.setMinimumSize(QSize(470,230))
            self.frame_VidInd.setMaximumSize(QSize(470,230))
            self.frame_Report.setMinimumSize(QSize(350,230))
            self.frame_Report.setMaximumSize(QSize(350,230))
            self.frame_Start.setMinimumSize(QSize(65,65))
            self.frame_Start.setMaximumSize(QSize(65,65))
            self.Star_btn.setMinimumSize(QSize(46, 46))
            self.Star_btn.setMaximumSize(QSize(46, 46))
            self.frame_Com.setMinimumSize(QSize(260,180))
            self.frame_Com.setMaximumSize(QSize(260,180))
            self.frame_Exp.setMinimumSize(QSize(250,40))
            self.frame_Exp.setMaximumSize(QSize(250,40))
            self.ExpCom1.setMaximumSize(180,30)
            self.ExpCom1.setMinimumSize(180,30)
            self.Send_btn.setMinimumSize(QSize(35,35))
            self.Send_btn.setMaximumSize(QSize(35,35))
            self.frame_deb.setMinimumSize(QSize(230,120))
            self.frame_deb.setMaximumSize(QSize(230,120))
            self.ExpCom.setMaximumSize(230,100)
            self.ExpCom.setMinimumSize(230,100)


        if SizeFlag == 3:
            self.resize(1800,1200)
            self.setMinimumSize(1800,1200)
            self.frame_camaras.setMinimumSize(QSize(1650,630))
            self.frame_camaras.setMaximumSize(QSize(1650,630))
            self.frame_cam1.setMinimumSize(QSize(800,600))
            self.frame_cam1.setMaximumSize(QSize(800,600))
            self.frame_cam2.setMinimumSize(QSize(800,600))
            self.frame_cam2.setMaximumSize(QSize(800,600))
            self.labelCam1_Idf.setMinimumSize(QSize(300,20))
            self.labelCam1_Idf.setMaximumSize(QSize(300,20))
            self.label_camera1.setMaximumSize(QSize(750,550))
            self.label_camera1.setMinimumSize(QSize(750,550))
            self.labelCam2_Idf.setMinimumSize(QSize(300,20))
            self.labelCam2_Idf.setMaximumSize(QSize(300,20))
            self.label_camera2.setMaximumSize(QSize(750,550))
            self.label_camera2.setMinimumSize(QSize(750,550))
            self.frameBackPart.setMinimumSize(QSize(1600,260))
            self.frameBackPart.setMaximumSize(QSize(1600,260))
            self.frame_Logo.setMaximumSize(QSize(190,210))
            self.frame_Logo.setMinimumSize(QSize(190,210))
            self.frame_Robot.setMaximumSize(QSize(190,210))
            self.frame_Robot.setMinimumSize(QSize(190,210))
            self.frame_Control.setMinimumSize(QSize(1200,230))
            self.frame_Control.setMaximumSize(QSize(1200,230))
            self.frame_StarCom.setMinimumSize(QSize(350,220))
            self.frame_StarCom.setMaximumSize(QSize(350,220))
            self.frame_VidInd.setMinimumSize(QSize(470,220))
            self.frame_VidInd.setMaximumSize(QSize(470,220))
            self.frame_Report.setMinimumSize(QSize(350,220))
            self.frame_Report.setMaximumSize(QSize(350,220))
            self.frame_Start.setMinimumSize(QSize(65,65))
            self.frame_Start.setMaximumSize(QSize(65,65))
            self.Star_btn.setMinimumSize(QSize(46, 46))
            self.Star_btn.setMaximumSize(QSize(46, 46))
            self.frame_Com.setMinimumSize(QSize(260,180))
            self.frame_Com.setMaximumSize(QSize(260,180))
            self.frame_Exp.setMinimumSize(QSize(250,40))
            self.frame_Exp.setMaximumSize(QSize(250,40))
            self.ExpCom1.setMaximumSize(180,30)
            self.ExpCom1.setMinimumSize(180,30)
            self.Send_btn.setMinimumSize(QSize(35,35))
            self.Send_btn.setMaximumSize(QSize(35,35))
            self.frame_deb.setMinimumSize(QSize(230,120))
            self.frame_deb.setMaximumSize(QSize(230,120))
            self.ExpCom.setMaximumSize(230,100)
            self.ExpCom.setMinimumSize(230,100)
            self.frame_Ent.setMinimumSize(QSize(260,130))
            self.frame_Ent.setMaximumSize(QSize(260,130))
            self.EntRep.setMaximumSize(250,120)
            self.EntRep.setMinimumSize(250,120)
            self.frame_Rbtn.setMinimumSize(QSize(260,30))
            self.frame_Rbtn.setMaximumSize(QSize(260,30))
            self.frame_btn_der.setMinimumSize(QSize(120,25))
            self.frame_btn_der.setMaximumSize(QSize(120,25))
            self.frame_btn_izq.setMinimumSize(QSize(120,25))
            self.frame_btn_izq.setMaximumSize(QSize(120,25))
            self.Sav_btn.setMinimumSize(QSize(100,20))
            self.Sav_btn.setMaximumSize(QSize(100,20))
            self.Can_btn.setMinimumSize(QSize(100,20))
            self.Can_btn.setMaximumSize(QSize(100,20))
            self.frame_Vid.setMinimumSize(QSize(380,40))
            self.frame_Vid.setMaximumSize(QSize(380,40))
            self.frame_Ind.setMinimumSize(QSize(350,150))
            self.frame_Ind.setMaximumSize(QSize(350,150))
            self.frame_VidIzq.setMinimumSize(QSize(130,40))
            self.frame_VidIzq.setMaximumSize(QSize(130,40))
            self.frame_VidCen.setMinimumSize(QSize(90,40))
            self.frame_VidCen.setMaximumSize(QSize(90,40))
            self.frame_VidDer.setMinimumSize(QSize(130,40))
            self.frame_VidDer.setMaximumSize(QSize(130,40))
            self.Rec_btn.setMinimumSize(QSize(30,30))
            self.Rec_btn.setMaximumSize(QSize(30,30))
            self.Set_btn.setMinimumSize(QSize(30,30))
            self.Set_btn.setMaximumSize(QSize(30,30))
            self.Gen_btn.setMinimumSize(QSize(30,30))
            self.Gen_btn.setMaximumSize(QSize(30,30))
            self.Rec_btnCen.setMinimumSize(QSize(30,30))
            self.Rec_btnCen.setMaximumSize(QSize(30,30))
            self.Gen_btnCen.setMinimumSize(QSize(30,30))
            self.Gen_btnCen.setMaximumSize(QSize(30,30))
            self.Rec_btnDer.setMinimumSize(QSize(30,30))
            self.Rec_btnDer.setMaximumSize(QSize(30,30))
            self.Set_btnDer.setMinimumSize(QSize(30,30))
            self.Set_btnDer.setMaximumSize(QSize(30,30))
            self.Gen_btnDer.setMinimumSize(QSize(30,30))
            self.Gen_btnDer.setMaximumSize(QSize(30,30))
            self.frame_Vel.setMinimumSize(QSize(170,120))
            self.frame_Vel.setMaximumSize(QSize(170,120))
            self.frame1.setMaximumSize(QSize(150,16))
            self.frame1.setMinimumSize(QSize(150,16))
            self.frame2.setMaximumSize(QSize(150,16))
            self.frame2.setMinimumSize(QSize(150,16))
            self.frame3.setMaximumSize(QSize(150,16))
            self.frame3.setMinimumSize(QSize(150,16))
            self.frame4.setMaximumSize(QSize(150,16))
            self.frame4.setMinimumSize(QSize(150,16))
            self.frame5.setMaximumSize(QSize(150,16))
            self.frame5.setMinimumSize(QSize(150,16))
            self.frame6.setMaximumSize(QSize(150,16))
            self.frame6.setMinimumSize(QSize(150,16))
            self.frame_Est.setMinimumSize(QSize(170,120))
            self.frame_Est.setMaximumSize(QSize(170,120))
            self.frame12.setMinimumSize(QSize(150,18))
            self.frame12.setMaximumSize(QSize(150,18))
            self.frame22.setMinimumSize(QSize(150,18))
            self.frame22.setMaximumSize(QSize(150,18))
            self.frame32.setMinimumSize(QSize(150,18))
            self.frame32.setMaximumSize(QSize(150,18))
            self.frame42.setMinimumSize(QSize(150,18))
            self.frame42.setMaximumSize(QSize(150,18))
            self.frame52.setMinimumSize(QSize(150,18))
            self.frame52.setMaximumSize(QSize(150,18))
            self.Bat_Lab.setMinimumSize(QSize(60,12))
            self.Bat_Lab.setMaximumSize(QSize(60,12))
            self.BatInd_Lab.setMinimumSize(QSize(60,12))
            self.BatInd_Lab.setMaximumSize(QSize(60,12))
            self.Bat_Pro.setGeometry(QRect(37.5,2,100,11))
            self.Spe_Lab.setMinimumSize(QSize(60,12))
            self.Spe_Lab.setMaximumSize(QSize(60,12))
            self.SpeInd_Lab.setMinimumSize(QSize(60,12))
            self.SpeInd_Lab.setMaximumSize(QSize(60,12))
            self.Spe_Pro.setGeometry(QRect(37.5,2,100,11))
            self.Lig_Lab.setMinimumSize(QSize(60,12))
            self.Lig_Lab.setMaximumSize(QSize(60,12))
            self.LigInd_Lab.setMinimumSize(QSize(60,12))
            self.LigInd_Lab.setMaximumSize(QSize(60,12))
            self.Lig_Pro.setGeometry(QRect(37.5,2,100,11))
            self.Joy_Pro.setGeometry(QRect(100,2,15,15))
            self.Rpi_Pro.setGeometry(QRect(100,2,15,15))
            self.Nuc_Pro.setGeometry(QRect(100,2,15,15))
            self.CamS_Pro.setGeometry(QRect(100,2,15,15))
            self.Lid_Cou.setMaximumSize(QSize(50,18))
            self.Lid_Cou.setMinimumSize(QSize(50,18))
            self.label_Robot.setMaximumSize(200,178)
            self.label_Robot.setMinimumSize(200,178)
            self.label_Logo.setMaximumSize(200,180)
            self.label_Logo.setMinimumSize(200,180)

        if SizeFlag == 4:
            self.resize(2010,1340)
            self.setMinimumSize(2010,1340)
            self.frame_camaras.setMinimumSize(QSize(2020,870))
            self.frame_camaras.setMaximumSize(QSize(2020,870))
            self.frame_cam1.setMinimumSize(QSize(990,830))
            self.frame_cam1.setMaximumSize(QSize(990,830))
            self.frame_cam2.setMinimumSize(QSize(990,830))
            self.frame_cam2.setMaximumSize(QSize(990,830))
            self.labelCam1_Idf.setMinimumSize(QSize(300,20))
            self.labelCam1_Idf.setMaximumSize(QSize(300,20))
            self.label_camera1.setMaximumSize(QSize(970,800))
            self.label_camera1.setMinimumSize(QSize(970,800))
            self.labelCam2_Idf.setMinimumSize(QSize(300,20))
            self.labelCam2_Idf.setMaximumSize(QSize(300,20))
            self.label_camera2.setMaximumSize(QSize(970,800))
            self.label_camera2.setMinimumSize(QSize(970,800))
            self.frameBackPart.setMinimumSize(QSize(2000,320))
            self.frameBackPart.setMaximumSize(QSize(2000,320))
            self.frame_Logo.setMaximumSize(QSize(220,210))
            self.frame_Logo.setMinimumSize(QSize(220,210))
            self.frame_Robot.setMaximumSize(QSize(220,210))
            self.frame_Robot.setMinimumSize(QSize(220,210))
            self.frame_Control.setMinimumSize(QSize(1500,320))
            self.frame_Control.setMaximumSize(QSize(1500,320))
            self.frame_StarCom.setMinimumSize(QSize(450,310))
            self.frame_StarCom.setMaximumSize(QSize(450,310))
            self.frame_VidInd.setMinimumSize(QSize(580,310))
            self.frame_VidInd.setMaximumSize(QSize(580,310))
            self.frame_Report.setMinimumSize(QSize(450,310))
            self.frame_Report.setMaximumSize(QSize(450,310))
            self.frame_Start.setMinimumSize(QSize(65,65))
            self.frame_Start.setMaximumSize(QSize(65,65))
            self.Star_btn.setMinimumSize(QSize(46, 46))
            self.Star_btn.setMaximumSize(QSize(46, 46))
            self.frame_Com.setMinimumSize(QSize(350,290))
            self.frame_Com.setMaximumSize(QSize(350,290))
            self.frame_Exp.setMinimumSize(QSize(340,50))
            self.frame_Exp.setMaximumSize(QSize(340,50))
            self.ExpCom1.setMaximumSize(240,30)
            self.ExpCom1.setMinimumSize(240,30)
            self.Send_btn.setMinimumSize(QSize(35,35))
            self.Send_btn.setMaximumSize(QSize(35,35))
            self.frame_deb.setMinimumSize(QSize(340,210))
            self.frame_deb.setMaximumSize(QSize(340,210))
            self.ExpCom.setMaximumSize(320,190)
            self.ExpCom.setMinimumSize(320,190)
            self.frame_Ent.setMinimumSize(QSize(340,210))
            self.frame_Ent.setMaximumSize(QSize(340,210))
            self.EntRep.setMaximumSize(320,190)
            self.EntRep.setMinimumSize(320,190)
            self.frame_Rbtn.setMinimumSize(QSize(340,50))
            self.frame_Rbtn.setMaximumSize(QSize(340,50))
            self.frame_btn_der.setMinimumSize(QSize(150,45))
            self.frame_btn_der.setMaximumSize(QSize(150,45))
            self.frame_btn_izq.setMinimumSize(QSize(150,45))
            self.frame_btn_izq.setMaximumSize(QSize(150,45))
            self.Sav_btn.setMinimumSize(QSize(120,30))
            self.Sav_btn.setMaximumSize(QSize(120,30))
            self.Can_btn.setMinimumSize(QSize(120,30))
            self.Can_btn.setMaximumSize(QSize(120,30))
            self.frame_Vid.setMinimumSize(QSize(520,40))
            self.frame_Vid.setMaximumSize(QSize(520,40))
            self.frame_Ind.setMinimumSize(QSize(540,240))
            self.frame_Ind.setMaximumSize(QSize(540,240))
            self.frame_VidIzq.setMinimumSize(QSize(190,40))
            self.frame_VidIzq.setMaximumSize(QSize(190,40))
            self.frame_VidCen.setMinimumSize(QSize(90,40))
            self.frame_VidCen.setMaximumSize(QSize(90,40))
            self.frame_VidDer.setMinimumSize(QSize(190,40))
            self.frame_VidDer.setMaximumSize(QSize(190,40))
            self.Rec_btn.setMinimumSize(QSize(35,35))
            self.Rec_btn.setMaximumSize(QSize(35,35))
            self.Set_btn.setMinimumSize(QSize(35,35))
            self.Set_btn.setMaximumSize(QSize(35,35))
            self.Gen_btn.setMinimumSize(QSize(35,35))
            self.Gen_btn.setMaximumSize(QSize(35,35))
            self.Rec_btnCen.setMinimumSize(QSize(35,35))
            self.Rec_btnCen.setMaximumSize(QSize(35,35))
            self.Gen_btnCen.setMinimumSize(QSize(35,35))
            self.Gen_btnCen.setMaximumSize(QSize(35,35))
            self.Rec_btnDer.setMinimumSize(QSize(35,35))
            self.Rec_btnDer.setMaximumSize(QSize(35,35))
            self.Set_btnDer.setMinimumSize(QSize(35,35))
            self.Set_btnDer.setMaximumSize(QSize(35,35))
            self.Gen_btnDer.setMinimumSize(QSize(35,35))
            self.Gen_btnDer.setMaximumSize(QSize(35,35))
            self.frame_Vel.setMinimumSize(QSize(250,200))
            self.frame_Vel.setMaximumSize(QSize(250,200))
            self.frame1.setMaximumSize(QSize(225,30))
            self.frame1.setMinimumSize(QSize(225,30))
            self.frame2.setMaximumSize(QSize(225,30))
            self.frame2.setMinimumSize(QSize(225,30))
            self.frame3.setMaximumSize(QSize(225,30))
            self.frame3.setMinimumSize(QSize(225,30))
            self.frame4.setMaximumSize(QSize(225,30))
            self.frame4.setMinimumSize(QSize(225,30))
            self.frame5.setMaximumSize(QSize(225,30))
            self.frame5.setMinimumSize(QSize(225,30))
            self.frame6.setMaximumSize(QSize(225,30))
            self.frame6.setMinimumSize(QSize(225,30))
            self.frame_Est.setMinimumSize(QSize(250,220))
            self.frame_Est.setMaximumSize(QSize(250,220))
            self.frame12.setMinimumSize(QSize(225,28))
            self.frame12.setMaximumSize(QSize(225,28))
            self.frame22.setMinimumSize(QSize(225,28))
            self.frame22.setMaximumSize(QSize(225,28))
            self.frame32.setMinimumSize(QSize(225,28))
            self.frame32.setMaximumSize(QSize(225,28))
            self.frame42.setMinimumSize(QSize(225,28))
            self.frame42.setMaximumSize(QSize(225,28))
            self.frame52.setMinimumSize(QSize(225,28))
            self.frame52.setMaximumSize(QSize(225,28))
            self.Bat_Lab.setMinimumSize(QSize(100,18))
            self.Bat_Lab.setMaximumSize(QSize(100,18))
            self.BatInd_Lab.setMinimumSize(QSize(100,18))
            self.BatInd_Lab.setMaximumSize(QSize(100,18))
            self.Bat_Pro.setGeometry(QRect(37.5,2,150,20))
            self.Spe_Lab.setMinimumSize(QSize(100,18))
            self.Spe_Lab.setMaximumSize(QSize(100,18))
            self.SpeInd_Lab.setMinimumSize(QSize(100,18))
            self.SpeInd_Lab.setMaximumSize(QSize(100,18))
            self.Spe_Pro.setGeometry(QRect(37.5,2,150,20))
            self.Lig_Lab.setMinimumSize(QSize(100,18))
            self.Lig_Lab.setMaximumSize(QSize(100,18))
            self.LigInd_Lab.setMinimumSize(QSize(100,18))
            self.LigInd_Lab.setMaximumSize(QSize(100,18))
            self.Lig_Pro.setGeometry(QRect(37.5,2,150,20))
            self.Joy_Pro.setGeometry(QRect(180,4,20,20))
            self.Rpi_Pro.setGeometry(QRect(180,4,20,20))
            self.Nuc_Pro.setGeometry(QRect(180,4,20,20))
            self.CamS_Pro.setGeometry(QRect(180,4,20,20))
            self.Lid_Cou.setMaximumSize(QSize(70,25))
            self.Lid_Cou.setMinimumSize(QSize(70,25))
            self.label_Robot.setMaximumSize(200,178)
            self.label_Robot.setMinimumSize(200,178)
            self.label_Logo.setMaximumSize(200,180)
            self.label_Logo.setMinimumSize(200,180)


        self.setMaximumSize(screen.width(),screen.height())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()
        self.updateImg = QTimer()
        self.updateImg.timeout.connect(self.updImg)
        self.updateImg2 = QTimer()
        self.updateImg2.timeout.connect(self.updImg2)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb_image.shape
        bytes_per_line = ch*w
        convert_to_Qt_format = QImage(rgb_image.data,w,h,bytes_per_line,QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(970, 640,Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def convert_cv_qt2(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb_image.shape
        bytes_per_line = ch*w
        convert_to_Qt_format = QImage(rgb_image.data,w,h,bytes_per_line,QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(970, 640,Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def convert_cv_qt3(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb_image.shape
        bytes_per_line = ch*w
        convert_to_Qt_format = QImage(rgb_image.data,w,h,bytes_per_line,QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(200, 200, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def updImg(self):
        try:
            directorio=self.wd1+"\poke3.png"
            self.imgCV = cv2.imread(directorio)
            #cv2.imshow("frame",self.imgCV)
            self.imgQT = self.convert_cv_qt(self.imgCV)
            self.label_camera1.setPixmap(self.imgQT)
        except:
            print("Error en la actualizacion de imagen")
            pass

    def updImg2(self):
        try:
            directorio=self.wd1+"\poke4.png"
            self.imgCV2 = cv2.imread(directorio)
            #self.imgCV2 = cv2.flip(self.imgCV2,0)
            #self.imgCV2 = cv2.flip(self.imgCV2,1)
            self.imgQT2 = self.convert_cv_qt2(self.imgCV2)
            self.label_camera2.setPixmap(self.imgQT2)
        except:
            pass

    def ActualizarLabel(self,textAction):
        print(textAction)
        if(textAction[5] == 'j'):
            self.Lid_Cou.setText(textAction[16:])
            #print("Comando de indicadores recibido")
            try:
            	battery = float(textAction[7:10])
            except:
            	print('Battery mistake')
            speed = int(textAction[11:13])
            lights = int(textAction[14:15])
            print(battery)
            print(lights)

            self.Spe_Pro.setValue(speed)
            
            if lights == 1:
            	self.Lig_Pro.setValue(100)

            if lights == 0:
            	self.Lig_Pro.setValue(0)

            Bat_100 = 250.0
            Bat_0 = 220.0

            if (battery < Bat_100) and (battery > Bat_0):
                self.BatInd_Lab.setText(str((battery/10)))
                porcentaje = battery - Bat_0
                porcentaje = porcentaje/(Bat_100-Bat_0)
                porcentaje = porcentaje*95
                porcentaje = porcentaje + 5
                self.Bat_Pro.setValue(int(porcentaje)) 
        else:
            self.ExpCom.appendPlainText(textAction)

        if(textAction == "StartMeasure"):
            self.Nuc_Pro.setValue(100)

        if(textAction == "MeasureStopped"):
            self.Nuc_Pro.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    TUMI = TUMI_Xplora()
    TUMI.SetWidgetXplora()
    TUMI.show()
    sys.exit(app.exec_())
