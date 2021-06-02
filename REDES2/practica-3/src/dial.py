"""Gestiona peticiones recibidas e inicia conexiones UDP

Autores:
    Rodrigo Juez y Kevin de la Coba
"""

import socket
import config
from src import discoverServer
from src import callResponses
import src.transmision as ts
import threading
import os
import select
BUFFER_RECV = 1024

class Dial:
    """Clase para tener una conexión de control 
    entre 2 usuarios.
    """

    transmision = None
    finLlamada = threading.Event()
    pausaLlamada = threading.Event() #negated true = no pausada
    video = None
    pipein1 = None
    pipein2 = None

    def __init__(self, client, server, source_ip, source_TCPport, source_UDPport):
        """Constructor de la clase

        Args:
            client (AppJar): Cliente. Se usa para pequeñas modificaciones en la GUI.
            server (DiscoverServer): Objeto para hacer, si es necesario, peticiones
            al servidor de descubrimiento.
            source_ip (str): Nuestra IP.
            source_TCPport (int): Nuestro puerto TCP.
            source_UDPport (int): Nuestro puerto UDP.
        """
        self.client = client
        self.server = server

        self.source_ip = source_ip
        self.source_TCPport = source_TCPport
        self.source_UDPport = source_UDPport

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((config.IP, source_TCPport))
        self.sock.listen(10)

    def send_data_sock(self, ip, puerto, data):
        """Función para enviar datos a través de un socket.

        Args:
            ip (str): Dirección IP a quien enviar los datos.
            puerto (str): Puerto por donde enviar datos.
            data: Datos a enviar.

        Returns:
            bool: True en caso de exito.
        """
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.send_sock.connect((ip, int(puerto)))
        try:
            self.send_sock.send(data.encode('utf-8'))
        except:
            return False
        self.send_sock.close()
        return True


    def send_calling(self, ip, puerto, name, video=None): 
        """Función para pedir una llamada con un usuario.

        Args:
            ip (str): IP a quien enviar el mensaje.
            puerto (int): Puerto TCP por el que enviar el mensaje.
            name (str): Nuestro nickname.
            video (str, optional): Localización del video a enviar
            en caso de que se especifique. Defaults to None.

        Returns:
            bool: True en caso de exito.
        """
        buff_size = 4096
        # Construyendo mensaje
        data = 'CALLING ' + name + ' ' + str(self.source_UDPport)
        self.send_data_sock(ip, puerto, data)

        self.video = video
        return True


    def send_hold(self, ip, puerto, name):
        """Función para poner en espera una llamada.
        Envía un mensaje TCP.

        Args:
            ip (str): IP a quien enviar el mensaje.
            puerto (int): Puerto TCP por el que enviar el mensaje.
            name (str): Nuestro nickname.
        """
        # Construyendo respuesta
        data = 'CALL_HOLD ' + name
        return self.send_data_sock(ip, puerto, data)


    def send_resume(self, ip, puerto, name):
        """Función para continuar una llamada.
        Envía un mensaje TCP.

        Args:
            ip (str): IP a quien enviar el mensaje.
            puerto (int): Puerto TCP por el que enviar el mensaje.
            name (str): Nuestro nickname.
        """
        # Construyendo respuesta
        data = 'CALL_RESUME ' + name
        return self.send_data_sock(ip, puerto, data)


    def send_end(self, ip, puerto, name):
        """Función para acabar una llamada.
        Envía un mensaje TCP.

        Args:
            ip (str): IP a quien enviar el mensaje.
            puerto (int): Puerto TCP por el que enviar el mensaje.
            name (str): Nuestro nickname.
        """
        # Construyendo respuesta
        data = 'CALL_END ' + name
        return self.send_data_sock(ip, puerto, data)

    def send_quality(self, ip, puerto, quality):
        """Función para enviar la calidad.
        
        quality = 1. Nos va muy mal, el emisor tiene que bajar mucho la calidad.
        quality = 2. Nos va mal, el emisor tiene que bajar un poco la calidad.
        quality = 3. Nos va bien, el emisor tiene que subir la calidad (si se puede).
        

        Args:
            ip (str): IP a quien enviar el mensaje.
            puerto (int): Puerto TCP por el que enviar el mensaje.
            quality (int): Nivel de calidad.
        """
        data = 'CALL_META ' + str(quality)
        return self.send_data_sock(ip, puerto, data)

    def call_daemon(self, pipeout):
        """Función ejecutada por un daemos para recibir
        peticiones.

        Args:
            pipeout (int): Pipe para acabar con la llamada.
        """
        while True:
            #cerrar socket desde padre y luego hacer join
            rfds, _, _ = select.select([self.sock, pipeout], [], [])
            if pipeout in rfds and self.client.inCall == True:
                colgarstr = os.read(pipeout, 7)
                os.write(self.pipein1, b"COLGAR")
                os.write(self.pipein2, b"COLGAR")
                
                self.trans.cap.release()
                self.reception_thread.join()

                # Esperamos a que los threads acaben su ejecución.
                self.transmision_thread.join()

                os.close(self.pipein1)
                os.close(self.pipein2)
                self.client.inCall = False
                self.client.app.hideSubWindow("Call")
                #self.client.app.show()

            else:
                conn, addr = self.sock.accept()

            petition = conn.recv(BUFFER_RECV)
            if petition:
                petition = petition.decode('utf-8')
                self.handle_petition(petition)


    def handle_petition(self, petition):
        """Función que maneja las peticiones recibidas.

        Args:
            petition (str): Petición recibida.
        """
        petition = petition.split(" ")
        if petition[0] == "CALLING":
            # CALLING nick srcUDPport
            self.handlerCALLING(petition[1], petition[2])
        elif petition[0] == "CALL_HOLD":
            self.handlerHOLD(petition[1]) #nick
        elif petition[0] == "CALL_RESUME":
            self.handlerRESUME(petition[1]) #nick
        elif petition[0] == "CALL_END":
            self.handlerEND(petition[1]) #nick
        elif petition[0] == "CALL_ACCEPTED":
            # ACCEPTED nick dstUDPport
            self.handlerACCEPTED(petition[1], petition[2])
        elif petition[0] == "CALL_DENIED":
            self.handlerDENIED(petition[1]) #NICK
        elif petition[0] == "CALL_BUSY":
            self.handlerBUSY() #no args
        elif petition[0] == "CALL_META":
            self.handlerMETA(petition[1])


    def handlerCALLING(self, nick, port_destUDP):
        """Función para manejar una llamada que recibimos.

        Args:
            nick (str): Nick name de quien nos llama.
            port_destUDP (int): Puerto del quien nos llama.
        """
        # Obtenemos información del nick que nos llama
        string, query = self.server.query(nick)
        if query == None:
            return None
            
        # Si estamos en llamada mandamos un mensaje de "busy call"
        if self.client.inCall == True:
            callResponses.busy_call(query['ip_address'], query['port'])
            return
        
        # Si no estamos en llamada preguntamos al usuario si quiere coger la llamada.
        if self.client.app.yesNoBox("Llamada Entrante", f"{nick} te esta llamando\n¿Coger el teléfono?") == True:
            if self.client.app.yesNoBox("Webcam", "¿Desea usar la webcam?") == True:
                self.video = None
            else:
                self.video = self.client.app.openBox(title="Open MP4", dirName="~", fileTypes=[("videos", "*.mp4"), ("videos", "*.mkv")], asFile=False, parent=None, multiple=False, mode='r')
                if self.video is ():
                    return

            # Enviamos un mensaje de que aceptamos la llamada
            callResponses.accept_call(self.client.nickname, self.source_UDPport, query['ip_address'], query['port'])
            self.client.inCall = True
            self.pausaLlamada.set()
            self.finLlamada.clear()

            # TODO establecer conexion a port_destUDP
            self.trans = ts.Transmision(self.client, self.source_ip, self.source_UDPport, query['ip_address'], int(port_destUDP), query['port'], self.video)
            self.client.destTCPIP = query['ip_address']
            self.client.destTCPPort = int(query['port'])

            max_protocol_supported = max([int(protocol[1]) for protocol in query['protocols'].split("#")])
            if max_protocol_supported == 1:
                connection_version = 1
            else:
                connection_version = 0

            # Desplegamos la transmisión
            self.despliegueTransmision(connection_version)
        else:
            # En caso de que no se quiera coger la llamada, mandamos un "deny call"
            self.finLlamada.clear()
            callResponses.deny_call(self.client.nickname, query['ip_address'], query['port'])            


    def handlerHOLD(self, nick):
        """Función para pausar una llamada.

        Args:
            nick (str): Nickname del usuario en la llamada.
        """
        self.pausaLlamada.clear()

    def handlerRESUME(self, nick):
        """Función para continuar con una llamada pausada.

        Args:
            nick (str): Nickname del usuario en la llamada.
        """
        self.pausaLlamada.set()

    def handlerEND(self, nick):
        """Función para terminar una llamada.

        Args:
            nick (str): Nickname del usuario con 
            quien finalizar una llamada.
        """
        os.write(self.pipein1, b"COLGAR")
        os.write(self.pipein2, b"COLGAR")
        os.close(self.pipein1)
        os.close(self.pipein2)
        self.client.inCall = False
        self.pausaLlamada.set()
        self.finLlamada.set()
        self.trans.cap.release()

        self.reception_thread.join()
        self.transmision_thread.join()
        self.client.app.hideSubWindow("Call")
        #self.client.app.show()

    
    def handlerACCEPTED(self, nick, port_destUDP):
        """Función para aceptar una llamada.

        Args:
            nick (str): Nickname de quien llama.
            port_destUDP (int): Puerto de quien llama.
        """
        #self.client.app.hideSubWindow("CallingBox")
        self.client.inCall = True
        self.finLlamada.clear()
        self.pausaLlamada.set()
        #self.client.app.hide()

        string, query = self.server.query(nick)

        # Obteniendo el protocolo más alto de la otra parte
        max_protocol_supported = max([int(protocol[1]) for protocol in query['protocols'].split("#")])
        if max_protocol_supported == 1:
            connection_version = 1
        else:
            connection_version = 0

        #generar clase transmision
        self.trans = ts.Transmision(self.client, self.source_ip, self.source_UDPport, query['ip_address'], int(port_destUDP), query['port'], self.video)
        self.despliegueTransmision(connection_version)

    def handlerDENIED(self, nick):
        """Función para mostrar por la GUI que
        el receptor nos ha denegado la llamada.

        Args:
            nick (str): Nickname del receptor.
        """
        #self.client.app.hideSubWindow("CallingBox")
        self.client.app.infoBox("Respuesta Llamada", f"{nick} ha denegado tu llamada")
    
    def handlerBUSY(self):
        """Función para mostrar por la GUI que
        el receptor esta ocupado.
        """
        self.client.app.infoBox("Respuesta Llamada", "La persona a la que llamas esta ocupada")
        #self.client.app.hideSubWindow("CallingBox")

    def handlerMETA(self, quality):
        """Función para manejar una petición de
        cambio de calidad en la llamada.

        Args:
            quality (int): Nivel de calidad que se ha pedido.
        """
        quality = int(quality)
        if quality == 3: # Subir calidad
            if self.trans.res_actual < 3:
                self.trans.res_actual += 1
                self.trans.setImageResolution(self.trans.res_list[self.trans.res_actual])
        elif quality == 2: # Bajar calidad
            if self.trans.res_actual > 0:
                self.trans.res_actual -= 1
                self.trans.setImageResolution(self.trans.res_list[self.trans.res_actual])
        elif quality == 1: # Bajar mucho la calidad, dos niveles
            if self.trans.res_actual > 1:
                self.trans.res_actual -= 2
                self.trans.setImageResolution(self.trans.res_list[self.trans.res_actual])
            elif self.trans.res_actual > 0: # En caso de que no se puedan bajar 2 niveles, bajamos 1
                self.trans.res_actual -= 1
                self.trans.setImageResolution(self.trans.res_list[self.trans.res_actual])
        self.client.app.setOptionBox("RESOLUTION: ", 3-self.trans.res_actual, value=True, callFunction=True, override=False)

    def despliegueTransmision(self, version_llamada):
        """Función para desplegar la transmision de datos.
        Hay 2 threads:
            - El primero envia datos al receptor.
            - El segundo los recibe y los muestra.

        Args:
            version_llamada (int): Si es 1 permitimos mensajes
            para manejar la calidad de la llamada, si es 0 no.
        """
        connection_version = 0
        pipeout1, self.pipein1 = os.pipe()
        pipeout2, self.pipein2 = os.pipe()

        # 2 threads, 1 que envié y otro que reciba y muestre
        self.finLlamada.clear()
        self.pausaLlamada.set()
        self.transmision_thread = threading.Thread( target = self.trans.enviar_imagenes, args=(self.finLlamada, self.pausaLlamada, pipeout1, version_llamada))
        self.reception_thread = threading.Thread(   target = self.trans.recibir_imagenes, args=(self.finLlamada, self.pausaLlamada, pipeout2, version_llamada))
        self.transmision_thread.setDaemon(True)
        self.reception_thread.setDaemon(True)
        self.transmision_thread.start()
        self.reception_thread.start()
        self.client.app.showSubWindow("Call")
        #self.client.app.hide()

