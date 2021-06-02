""" Archivo donde se crea la interfaz y se
manejan el login y la ventana principal. 

Autores:
    Rodrigo Juez y Kevin de la Coba
"""

# import the library
from appJar import gui
from PIL import Image, ImageTk
import numpy as np
import cv2
from src import discoverServer
from src import dial
import config
import threading
import socket
import sys
import time
import os
ARG = None
LOGGED = False

class VideoClient(object):
	nickname = None
	destTCPPort = None
	destTCPIP = None
	pipein = None
	inCall = False
	def __init__(self, window_size):
		"""Constructor del cliente de la P4.

		Args:
			window_size (str): Tamaño de la ventana.
		"""
		
		# Creamos un objeto para comunicarnos con el server
		self.discover = discoverServer.DiscoverServer(HOST = config.HOST, PORT = config.PORT)

		# Hacemos login
		self.app = gui("Login/Register", window_size)
		self.app.setGuiPadding(2, 2)
		if self.login() == False:
			self.app.warningBox("Exiting", "Contraseña Incorrecta", parent=None)
			self.app.stop()
			exit(1)

        # Creamos una variable que contenga el GUI principal
		self.app = gui("Wallace Communications", window_size)
		self.app.setGuiPadding(2, 2)
		self.app.setResizable(canResize=False)

		self.callhandler = dial.Dial(self, self.discover, config.IP, config.puertoTCP, config.puertoUDP)

        # Preparación del interfaz
		self.app.setTitle(f"{self.nickname} - P2P")
		self.app.startSubWindow("Call", transient=True, modal=True)
		self.app.addImage("received", "imgs/transmision_placeholder.gif", 0, 0, 5)
		self.app.setResizable(False)
		self.app.addImage("webcam", "imgs/webcam_placeholder.gif", 1, 0, 1, 2)
		self.app.addButton("PAUSA", self.buttonsCallback, 1, 1)
		self.app.addButton("COLGAR", self.buttonsCallback, 1, 2)
		self.app.addLabelOptionBox("RESOLUTION: ", ["HD", "HIGH", "MEDIUM", "LOW"], 1, 3)
		self.app.setOptionBox("RESOLUTION: ", 1)
		self.app.setStopFunction(lambda: self.buttonsCallback("COLGAR"))
		self.app.addButton("Apply Resolution", self.buttonsCallback, 1, 4)
		self.app.addLabel("llamada_tiempo", "", 2, 1)


		self.app.stopSubWindow()
		self.subwindow_exists = False

		
        # Registramos la función de captura de video
        # Esta misma función también sirve para enviar un vídeo
	

        # Añadir los botones
		infostr, dictlist = self.discover.list_users() 
			
		# Creamos una ventana para que se eliga a un usuario.
		self.subwindow_exists = True
		
		# Añadimos al diccionario un campo de la última conexión
		for user in dictlist:
			user['last_time'] = (time.time() - float(user['fecha']) ) / 60
			if user['last_time'] > 60:
				user['last_time'] /= 60
				user['last_time'] = "hace {:d}".format(int(user['last_time'])) + " horas"
			else:
				user['last_time'] = "hace {:d}".format(int(user['last_time'])) + " minutos"

		#self.app.addOptionBox("ChooseList", [user['nick'] + " - " + user['last_time'] for user in dictlist], 0, 0, 5)
		self.app.addEntry("BUSQUEDATEXT", 0, 0, 6)
		self.app.addButton("Buscar", self.buttonsCallback, 0, 6)
		self.app.setButtonImage("Buscar", os.path.abspath("imgs/search.gif"), align=None)
		self.app.addListBox("ChooseList", [user['nick'] + " - " + user['last_time'] for user in dictlist], 1, 0, 6)
		self.app.setListBoxRows("ChooseList", 7)
		self.app.addButton("ACTUALIZAR", self.buttonsCallback, 1, 6)
		self.app.setButtonImage("ACTUALIZAR", os.path.abspath("imgs/update.gif"), align=None)
		self.app.addHorizontalSeparator(3,0,7, colour="grey")
		self.app.addOptionBox("INPUT", ["WEBCAM", "INPUT FILE"], 4, 0)
		self.app.addButton("LLAMAR", self.buttonsCallback, 4, 6, 1)
		self.app.setButtonImage("LLAMAR", os.path.abspath("imgs/llamar.gif"), align=None)
		self.app.addLabelEntry("Llamar a:",2,0)

		# threading
		#hilo_llamadas = None

		# Fondo de los botones
		self.app.setFg("black")
		self.app.setBg("white")
		self.app.setFont(18)
		self.app.setButtonBg("LLAMAR", "white")
		self.app.setButtonBg("ACTUALIZAR", "white")
		self.app.setButtonBg("Buscar", "white")
		self.app.setButtonBg("PAUSA", "white")
		self.app.setButtonBg("COLGAR", "white")

	def login(self):
		"""Función para iniciar sesión 
		en el servidor.

		Returns:
			bool: True en caso de exito, false en caso de error.
		"""
		
		# Inicializando la ventana de login
		self.app.startSubWindow("Login")
		self.app.setResizable(False)
		self.app.setStopFunction(lambda: self.app.stop())
		# Entradas de la ventana
		self.app.addLabelEntry("Nickname",0,0)
		self.app.addLabelSecretEntry("Contraseña",1,0)
		self.app.addEmptyLabel("SEPARATOR", 2,0)
		self.app.addEmptyLabel("SEPARATOR2", 3,0)

		self.app.addLabel("AVANZADO","Avanzado (por defecto vacío):\t", 4, 0)
		self.app.addLabelNumericEntry("Puerto UDP", 5,0)
		self.app.addLabelNumericEntry("Puerto TCP", 6,0)

		# Botones
		self.app.addButtons(['Login', 'Cancel'], self.login_buttons)

		self.app.setFg("black")
		self.app.setBg("white")
		self.app.setFont(18)
		self.app.setButtonBg("Login", "white")
		self.app.setButtonBg("Cancel", "white")
		self.app.setLabelBg("Nickname", "white")
		self.app.setLabelBg("Contraseña", "white")
		self.app.setLabelBg("AVANZADO", "white")
		self.app.setLabelBg("Puerto UDP", "white")
		self.app.setLabelBg("Puerto TCP", "white")
		self.app.setLabelBg("Puerto TCP", "white")
		self.app.setLabelBg("SEPARATOR", "white")
		self.app.setLabelBg("SEPARATOR2", "white")

		self.app.stopSubWindow()
		self.app.go(startWindow="Login")

		if not LOGGED:
			exit()

	def start(self):
		"""Función que inicia el hilo de las llamadas
		y la GUI.
		"""	
		pipeout, self.pipein = os.pipe()
		self.hilo_llamadas = threading.Thread(target = self.callhandler.call_daemon, args=(pipeout, ))
		self.hilo_llamadas.setDaemon(True)
		self.hilo_llamadas.start()

		self.app.go()


    # Función que gestiona los callbacks de los botones
	def buttonsCallback(self, button):
		"""Función que recoge cuando se pulsa un botón.

		Args:
			button (str): Botón pulsado.
		"""
		if button == "COLGAR":
			# Si hay una llamada pausada, hay que reaunudarla
			# para colgar
			print("COLGANDO")
			if not self.callhandler.pausaLlamada.isSet():
				self.app.infoBox("Pausa", "Reanuda la llamada para colgar", parent="Call")
				return False
		
			# Finalizamos la llamada
			self.callhandler.pausaLlamada.set()
			self.callhandler.finLlamada.set()
			self.callhandler.send_end(self.destTCPIP, self.destTCPPort, self.nickname)
			os.write(self.pipein, b"COLGAR")
			return True

		elif button == "PAUSA":
			# Comprobamos si la llamada ha sido pausada
			if not self.callhandler.pausaLlamada.isSet():
				self.callhandler.pausaLlamada.set()
				self.callhandler.send_resume(self.destTCPIP, self.destTCPPort, self.nickname)
			else:
				# Si no lo ha sido continuamos con esta
				self.callhandler.pausaLlamada.clear()
				self.callhandler.send_hold(self.destTCPIP, self.destTCPPort, self.nickname)

		# Se especifica la resolución de la llamada
		elif button == "Apply Resolution":
			self.callhandler.trans.setImageResolution(self.app.getOptionBox("RESOLUTION: "))

		elif button == "Buscar":
			string = self.app.getEntry("BUSQUEDATEXT")

			# Actualizamos los usuarios
			infostr, dictlist = self.discover.list_users()

			# Obteniendo el delta de la última conexión
			listed_usrs = []
			for user in dictlist:
				if string not in user['nick']:
					continue
				user['last_time'] = (time.time() - float(user['fecha']) ) / 60
				if user['last_time'] > 60:
					user['last_time'] /= 60
					user['last_time'] = "hace {:.2f}".format(user['last_time']) + " horas"
				else:
					user['last_time'] = "hace {:.2f}".format(user['last_time']) + " minutos"
				listed_usrs.append(user)
			self.app.updateListBox("ChooseList", [user['nick'] + " - " + user['last_time'] for user in listed_usrs])

		elif button == "ACTUALIZAR":
			# Actualizamos los usuarios
			infostr, dictlist = self.discover.list_users()

			# Obteniendo el delta de la última conexión
			for user in dictlist:
				user['last_time'] = (time.time() - float(user['fecha']) ) / 60
				if user['last_time'] > 60:
					user['last_time'] /= 60
					user['last_time'] = "hace {:d}".format(int(user['last_time'])) + " horas"
				else:
					user['last_time'] = "hace {:d}".format(int(user['last_time'])) + " minutos"

			self.app.updateListBox("ChooseList", [user['nick'] + " - " + user['last_time'] for user in dictlist])

		elif button == "LLAMAR":
			target = self.app.getEntry("Llamar a:")
			if target == "":
				try:			
					target = self.app.getListBox("ChooseList")[0].split(" ")[0]
				except:
					self.app.infoBox("Warning", "Selecciona a alguien para llamar o introduce un nickname en la entrada para llamar a un usuario")
					return
			video = None
			if self.app.getOptionBox("INPUT") == "WEBCAM":
				video = None
			else:
				video = self.app.openBox(title="Open MP4", dirName="~", fileTypes=[("videos", "*.mp4"), ("videos", "*.mkv")], asFile=False, parent=None, multiple=False, mode='r')
				if video is ():
					return

			strinfo, info_requested = self.discover.query(target)
			if strinfo is None:
				self.app.infoBox("Warning", "El usuario que has introducido no existe, si has seleccionado un usuario de la lista elimina el texto introducido en el campo 'llamar a'")
				return

			if "V0" not in info_requested['protocols']:
				self.app.infoBox("No compatible con protocolos")
				return

			self.destTCPIP = info_requested['ip_address']
			self.destTCPPort = int(info_requested['port'])
			try:
				self.callhandler.send_calling(info_requested['ip_address'], info_requested['port'], self.nickname, video)
			except:
				self.app.infoBox("Warning", f"{info_requested['nick']} no esta disponible")

	def login_buttons(self, button):
		global LOGGED
		if button == "Login":
			nickname = self.app.getEntry("Nickname")
			password = self.app.getEntry("Contraseña")
			puertoTCP = self.app.getEntry("Puerto TCP")
			puertoUDP = self.app.getEntry("Puerto UDP")
			
			if nickname == '' or password == '':
				self.app.infoBox(title="WARNING", message = "Introduce nickname y password")
				return
	
			self.nickname = nickname
			if puertoTCP != None:
				config.puertoTCP = int(puertoTCP)
			else:
				try:
					config.puertoTCP = int(os.environ.get("CONTROL_PORT"))
				except:
					self.app.infoBox(title = "WARNING", message = "La variable de entorno CONTROL_PORT no existe, y el usuario no ha especificado los puertos, se usa el config.py")
			
			if puertoTCP != None:
				config.puertoUDP = int(puertoUDP)
			else:
				try:
					config.puertoUDP = int(os.environ.get("SRC_PORT"))
					
				except:
					self.app.infoBox(title = "WARNING", message = "La variable de entorno SRC_PORT no existe, y el usuario no ha especificado los puertos, se usa el config.py")

			LOGGED = True


			if self.discover.register(nickname, password, ["V0", "V1"], int(config.puertoTCP)) == False:
				self.app.infoBox(title="WARNING", message = "Error al hacer login, compruebe sus datos")
				return False

			self.app.stop()

		else: # Se pulsa CANCEL
			self.app.stop()

if __name__ == '__main__':
	
    vc = VideoClient("500x400")

    # Crear aquí los threads de lectura, de recepción y,
    # en general, todo el código de inicialización que sea necesario
    # ...

    # Lanza el bucle principal del GUI
    # El control ya NO vuelve de esta función, por lo que todas las
    # acciones deberán ser gestionadas desde callbacks y threads
    vc.start()