import socket
import time
import multiprocessing
import threading
import cv2
import pickle
import struct
import serial

serialPuerto=0

def IndSendDat(nucleo):
	global serialPuerto
	dato="$OAX1J"
	while(True):
		time.sleep(0.01)
		if serialPuerto==0:
			nucleo.write(dato.encode())

def IndRecvDat(nucleo,cliente):
	while(True):
		dato=nucleo.readline()
		print("dato recibido: ",dato)
		cliente.send(pickle.dumps(dato.decode()))

def enviarFram(frame,clienteCam,ind):
	imEncoded,buf=cv2.imencode('.jpg',frame)
	ImgSend=pickle.dumps(buf)
	message=struct.pack("Q",len(ImgSend))+struct.pack("Q",ind)+ImgSend
	clienteCam.send(message)

def camara1Send():
	print("PROCESO CAMARA")
	CamServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	CamLoc=('192.168.137.10',9666)
	CamServer.bind(CamLoc)
	CamServer.listen(1)
	clienteCam,clienteCamLoc=CamServer.accept()
	try:
		Cap=cv2.VideoCapture('/dev/video0')
	except:
		print("No existe conexion con la camara, revisar conexion fisica")
		exit()
	Cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
	Cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
	CamIni=1
	while(True):
		if CamIni==1:
			Cam,frame=Cap.read()
			CamIni=2
		SendPro=threading.Thread(target=enviarFram,args=(frame,clienteCam,1,))
		SendPro.start()
		Cam,frame=Cap.read()
		SendPro.join()

	
	

def InicioRobot():
	global serialPuerto
	print("Inicio del programa Magnus")
	print("Se creara el socket principal")
	Server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ServerLoc=('192.168.137.10',8666)
	try:
		Server.bind(ServerLoc)
		print("El socket se ha creado correctamente")
	except:
		print("No se pudo crear el socket, revisar la IP del robot")
		exit()
	try:
		nucleo=serial.Serial('/dev/ttyACM0',115200)
		if(nucleo.is_open == True):
			print("Nucleo conectada y puerto abierto")
		else:
			print("Nucleo conectada y puerto cerrado")
	except:
		print("No existe conexion con la nucleo")
		exit()
	
	print("Esperando conexion")
	Server.listen(1)
	cliente, clienteLoc = Server.accept()
	print("Conexion establecida con el usuario: ", clienteLoc)
	print("Se iniciaran los servicios de comunicacion con la nucleo")
	IndRecv=threading.Thread(target=IndRecvDat, args=(nucleo,cliente,))
	IndRecv.start()
	IndSend=threading.Thread(target=IndSendDat, args=(nucleo,) )
	IndSend.start()
	print("Procesos de comunicacion iniciados, enviando indicadores a la estacion base")
	print("Esperando comandos de la estacion base")
	
	while(True):
		Comando=cliente.recv(4096)
		comando=pickle.loads(Comando)
		print("Comando recibido: ", comando)
		if comando==b'':
			print("Conexion fallida, reiniciar todo")
			exit()
		if comando=="$OAX01":
			print("Se iniciara la camara trasera")
			camara1Pro=multiprocessing.Process(target=camara1Send)
			camara1Pro.start()
			print("Camara iniciada")
		if comando=="$OAX3J0A":
			print("Comando de Avanzar")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando Avanzar ejecutado")
		if comando=="$OAX3J0B":
			print("Comando de retroceder")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando retroceder ejecutado")
		if comando=="$OAX3J0r":
			print("Comando giro horario ")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando giro horario ejecutado")
		if comando=="$OAX3J0l":
			print("Comando de giro antihorario ")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando giro antihorario ejecutado")
		if comando=="$OAX3JR1":
			print("Comando de prender luces")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando prender luces ejecutado")
		if comando=="$OAX3JR2":
			print("Comando de apagar luces")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando apagar luces ejecutado")
		if comando=="$OAX3JX1":
			print("Comando de aumentar velocidad")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando aumentar velocidad ejecutado")
		if comando=="$OAX3JX2":
			print("Comando de disminuir velocidad")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando disminuir velocidad ejecutado")
		if comando=="$OAX3JRA":
			print("Comando de avanzar derecha")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando avanzar derecha ejecutado")
		if comando=="$OAX3JLA":
			print("Comando de avanzar izquierda")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando avanzar izquierda ejecutado")
		if comando=="$OAX1S":
			print("Comando de empezar sensor")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando empezar sensor ejecutado")
		if comando=="$OAX1P":
			print("Comando de encender motores")
			serialPuerto=1
			time.sleep(0.01)
			nucleo.write(comando.encode())
			time.sleep(0.01)
			serialPuerto=0
			print("Comando encender motor ejecutado")
	print("Bucle terminado, conexion perdida. Volver a iniciar")
		

if __name__=="__main__":
	print("El robot Magnus iniciará")
	try:
		InicioRobot()
	except:
		print("No se pudo iniciar el programa de Magnus, error de codigo")
