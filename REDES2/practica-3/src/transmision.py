"""Archivo para manejar la transmisión de
datos.

Autores:
    Rodrigo Juez y Kevin de la Coba
"""

import time
import socket
import cv2
from PIL import Image, ImageTk
import numpy
from config import *
import threading
import select
import os

class Transmision():
    """
    Clase que maneja la transmisión de
    los datos (envío y recepción).
    """
    compresion = 40
    delay = 0.2
    constante_fija = 0.2
    retardo_anterior = 0.0
    variaciones_anterior = 0.0
    #K = 0.0 # Hay que definir un K

    def __init__(self, gui, sourceIP, sourcePort, destIP, destPort, destPortTCP, sourceVideo = None):
        """Constructor de la clase para la transmisión.

        Args:
            gui (Appjar Object): Instancia de la GUI de la aplicación.
            sourceIP (str): Nuestra IP.
            sourcePort (int): Nuestro puerto reservado para la transmisión.
            destIP (str): IP del receptor.
            destPort (int): Puerto del receptor.
            sourceVideo (str, optional): En caso de que se quiera usar un video
            destPortTCP (int): Puerto TCP del receptor.
            ya guardado y no la webcam. Defaults to None.
        """
        self.gui = gui
        self.sourceIP = sourceIP
        self.sourcePort = sourcePort
        self.destIP = destIP
        self.destPort = destPort
        self.destportTCP = destPortTCP

        # Iniciando socket para la recepción de datos
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_sock.bind((self.sourceIP, self.sourcePort))

        # Iniciando socket para el envío de datos.
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_sock.connect((self.destIP, self.destPort))

        self.current_res = None
        self.res_actual = None
        self.res_list = ['LOW', 'MEDIUM', 'HIGH', 'HD']
        if sourceVideo == None:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(sourceVideo)

        self.setImageResolution("HIGH")
        self.fps = 25
        self.frames_sent = 0
        self.last_call = 0
        self.start_call_time = time.time()

    # Establece la resolución de la imagen capturada
    def setImageResolution(self, resolution):
        """Función para establecer la resolución
        de las imágenes que se envían.

        Args:
            resolution (str): LOW, MEDIUM, HIGH y HD.
        """
        # Se establece la resolución de captura de la webcam
        # Puede añadirse algún valor superior si la cámara lo permite
        # pero no modificar estos
        # Dependiendo de la resolución se modifican los fps
        if resolution == "LOW":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
            self.current_res = (160, 120)
            self.res_actual = 0
            self.fps = 15
            self.compresion = 50

        elif resolution == "MEDIUM":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.current_res = (320, 240)
            self.res_actual = 1
            self.fps = 19
            self.compresion = 50

        elif resolution == "HIGH":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.current_res = (640, 480)
            self.res_actual = 2
            self.fps = 22
            self.compresion = 50

        elif resolution == "HD":
            self.compresion = 40
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.current_res = (960, 720)
            self.res_actual = 3
            self.fps = 25
            self.compresion = 60

    #mete a la gui el frame y devuelve los bytes a enviar
    #TODO meter fps aqui
    def webcam_read(self):
        """Función que obtiene una imagen de la webcam.
        Se generan 2 frames, uno para mostrarlo en la GUI
        y otro para enviarlo.

        Returns:
            bytes: Bytes de la imágen a enviar.
        """
        # Capturamos un frame de la cámara o del vídeo
        ret, frame = self.cap.read()
        try:
            # Lo mostramos en el GUI
            framegui = cv2.resize(frame, (160,120), interpolation=cv2.INTER_AREA)
            cv2_im = cv2.cvtColor(framegui, cv2.COLOR_BGR2RGB)
            img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))
            #img_tk = img_tk.resize((256,144))
            self.gui.app.setImageData("webcam", img_tk, fmt='PhotoImage')
        except:
            return None
        frame_send = cv2.resize(frame, self.current_res)
        #compresion de la imagen para enviar por el socket
        param = [cv2.IMWRITE_JPEG_QUALITY, self.compresion]
        result, encimg = cv2.imencode(' .jpg', frame_send, param)
        if result == False:
            return None
        encimg = encimg.tobytes()

        return encimg

    def send_package(self, payload):
        """Función para enviar datos de la llamada (video).

        Args:
            payload (bytearray): Imagen a enviar.
        """
        # Construimos el mensaje.
        package = f"{self.frames_sent}#{time.time()}#{self.current_res[0]}x{self.current_res[1]}#{self.fps}#"
        package = bytearray(package.encode('utf-8')) + payload
        self.frames_sent += 1

        # Enviamos el mensaje.
        self.send_sock.sendall(package)

    def unpack_package(self, package):
        """Desempaqueta un paquete. De bytes a string.
        Devuelve una lista con los elementos del paquete:
        frames_sent, time, resolución - width, 
        resuolución - height, fps y el payload.

        Args:
            package (bytes): Paquete.

        Returns:
            tuple: Tiempo en el que se ha enviado la imágen y
            los bytes del paquete.
        """
        package_decoded = package.split(b'#', 4)
        return package_decoded[1], package_decoded[4]

    def enviar_imagenes(self, finLlamada, pausaLlamada, pipeout, version_llamada):
        """Función que envía imágenes al receptor. Mientras
        comprueba si hay que finalizar la llamada o pausarla.

        Args:
            finLlamada (Thread.Event): Thread event para marcar el fin de la llamada.
            pausaLlamada (Thread.Event): Thread event para pausar el fin de la llamada.
            pipeout (int): Pipe para acabar la llamada-
            version_llamada (int): Para saber la versión de la llamada.
        """
        print(f"LA VERSION ENVIAR DE LA LLAMADA ES {version_llamada}")
        # Creamos un marco
        while not finLlamada.isSet():
            frame_bytes = self.webcam_read()
            if frame_bytes == None:
                return
            try:
                self.send_package(frame_bytes)
            except:
                break

            time.sleep(1/self.fps)
            pausaLlamada.wait()

            # Tiempo llamada
            self.gui.app.setLabel("llamada_tiempo", "duracion: {:.0f} s".format(time.time() - self.start_call_time))

    def recibir_imagenes(self, finLlamada, pausaLlamada, pipeout, version_llamada):
        """Función para recibir imagenes del emisor.

        Args:
            finLlamada (Thread.Event): Thread event para marcar el fin de la llamada.
            pausaLlamada (Thread.Event): Thread event para pausar el fin de la llamada.
            pipeout (int): Pipe para acabar la llamada-
            version_llamada (int): Para saber la versión de la llamada.
        """
        print(f"LA VERSION RECIBIR DE LA LLAMADA ES {version_llamada}")
        buff_size = 10485760
        while not finLlamada.isSet():
            
            time.sleep(1/self.fps)
            # Si se recibe colgar salimos
            rfds, _, _ = select.select([self.recv_sock, pipeout], [], [])
            if pipeout in rfds:
                break

            # Recibimos el paquete
            data = self.recv_sock.recv(buff_size)

            if data == None:
                exit()
            # Controlamos el flujo
            self.flow_control(data, finLlamada, version_llamada)

            pausaLlamada.wait()

            # Tiempo llamada
            self.gui.app.setLabel("llamada_tiempo", "duracion: {:.0f} s".format(time.time() - self.start_call_time))

    def flow_control(self, data, finLlamada, version_llamada):
        """Función para manejar el control
        de flujo de la llamada.

        Args:
            data (bytearray): Datos.
        """
        global retardo_anterior
        
        ts, photo = self.unpack_package(data)
        ts = float(ts.decode('utf-8'))

        # Calculamos el retardo actual.
        self.retardo_anterior = (1-self.constante_fija)*self.retardo_anterior + self.constante_fija*(time.time()-ts)

        # Establecemos unos niveles para el valor del retardo.
        self.last_call += 1
        if version_llamada == 1 and self.last_call%20 == 0:
            if self.retardo_anterior > 0.2:
                self.delay = 1
                self.gui.callhandler.send_quality(self.destIP, self.destportTCP, 1)
            elif self.retardo_anterior > 0.1:
                self.delay = 0.4
                self.gui.callhandler.send_quality(self.destIP, self.destportTCP, 2)
            else:
                self.delay = 0.1
                self.gui.callhandler.send_quality(self.destIP, self.destportTCP, 3)
            self.last_call = 0

        if finLlamada.isSet():
            return
        # Calculamos la diferencia en el tiempo
        dif = (ts + self.delay) - time.time()
        if dif > 0.00001: #este es el tiempo que tarda en crease un thread
            t = threading.Timer(dif, self.show_frame, args=[photo, finLlamada])
            t.start()

    def show_frame(self, photo, finLlamada):
        """Función para mostrar una Imagen.

        Args:
            photo (bytearray): Imagen a mostrar.
            finLlamada (Thread.Event): Thread event para marcar el fin de la llamada.
        """
        photo = cv2.imdecode(numpy.frombuffer(photo, numpy.uint8), 1)

        photo = cv2.resize(photo, (960,720), interpolation=cv2.INTER_AREA)

        photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)

        if finLlamada.isSet():
            return
        photo = ImageTk.PhotoImage(Image.fromarray(photo))
        self.gui.app.setImageData("received", photo, fmt='PhotoImage')
