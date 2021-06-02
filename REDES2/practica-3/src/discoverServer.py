"""Archivo donde se crea una clase con la
intención de que esta comunique al cliente con el
servidor, ejecutando las correspondientes peticiones.

Autores:
    Rodrigo Juez y Kevin de la Coba
"""

import time
import socket
import config

class DiscoverServer:
    """
        Clase para comunicar al cliente con el servidor
        de descubrimiento.
    """
    def __init__(self, HOST='vega.ii.uam.es', PORT = 8000):
        """Constructor de la clase.

        Args:
            HOST (str, optional): Servidor con el que comunicarse. 
                                  Defaults to 'vega.ii.uam.es'.
            PORT (int, optional): Puerto por el que comunicarse 
                                  con el servidor. Defaults to 8000.
        """
        self.HOST = HOST
        self.PORT = PORT

    def socket(self):
        """Función para crear un socket TCP.

        Returns:
            socket: Socket TCP
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        return s
    
    # supported_protocols es una lista en forma (["v0", "v1"])
    def register(self, nickname, password, supported_protocols, port):
        """Función para registrar un usuario.

        Args:
            nickname (str): Nombre del usuario
            password (str): Contraseña del usuario.
            supported_protocols (str): Lista con los protocolos soportados.
            port (str): Puerto por el que especificamos que queremos
            que se nos contacte.

        Returns:
            bool: En caso de exito True, en caso de error False.
        """
        buff_size = 4096
        ip = config.IP #TODO socket.gethostbyname(socket.gethostname())
        data = 'REGISTER ' + nickname + ' ' + ip + ' ' + str(port) + ' ' + str(password) + ' ' + str(('#').join(supported_protocols))
        
        s = self.socket()
        # mejor que solo send porque este no para hasta fallar o enviar todo
        s.sendall(data.encode())

        # Recibimos los datos.
        data = s.recv(buff_size).decode()

        self.quit()

        # Error
        if data[0] == 'N':
            print("ERROR en REGISTRO: ", data)
            return False

        return True
        

    def query(self, name):
        """Función para buscar a un usuario.

        Args:
            name (str): Nombre del usuario al que buscamos.

        Returns:
            tuple: [0] String con el usuario. 
                   [1] Diccionario con los datos del usuario.
        """ 
        buff_size = 4096
        ip = socket.gethostbyname(socket.gethostname())
        data = 'QUERY ' + name
        
        s = self.socket()
        # mejor que solo send porque este no para hasta fallar o enviar todo
        s.sendall(data.encode())

        # Recibimos los datos.
        data = s.recv(buff_size).decode()
        self.quit()

        if data[0] == 'N': # Error
            print("ERROR en QUERY: ", data)
            return None, None
        
        data = data.split(" ")
        
        # Escribiendo los datos en un diccionario
        info_requested = {}
        info_requested['nick'] =  data[2]
        info_requested['ip_address'] = data[3]
        info_requested['port'] = data[4]
        info_requested['protocols'] = data[5]

        formatted_info = info_requested['nick']+", "+info_requested['ip_address']+", "+info_requested["port"]+", "+info_requested['protocols']+".\n"
        info_requested['port'] = int(info_requested['port'])
        return formatted_info, info_requested


    def list_users(self):
        """Función para listar a todos los usuarios
        del servidor.

        Returns:
            tuple: [0] String con todos los usuarios.
                   [1] Lista con diccionarios que contienen usuarios.
        """
        buff_size = 512
        ip = socket.gethostbyname(socket.gethostname())
        msg = 'LIST_USERS'
        
        # Enviamos el mensaje
        s = self.socket()
        s.sendall(msg.encode())

        # Recibimos los datos.
        data = ""

        try:
            s.settimeout(0.5)
            while True:

                chunk = s.recv(buff_size).decode()

                data += chunk
                """if len(chunk) < buff_size:
                    break"""
        except socket.timeout:
            pass

        # Finalizamos la conexión
        self.quit()

        # Error
        if data[0] == 'N':
            print("ERROR en LIST_USERS: ", data)
            return None
        # Guardamos la información
        splitted_users = data.split(" ")[3:]
        splitted_users = (" ").join(splitted_users).split("#")[:-1]

        info_users = []
        for usr in splitted_users:
            info = usr.split(" ")
            try: # Para prevenir de graciosos que ponen # en los nombres
                info_users.append({'nick': info[0], 'ip': info[1], 'port': info[2], 'fecha': info[3] })
            except:
                pass

        # Formateamos la string de los usuarios
        formatted_info = ""
        for usr in info_users:
            formatted_info += "Nickname: "+usr['nick']+", IP: "+usr['ip']+", Puerto: "+usr['port']+", Fecha: "+usr['fecha']+"\n"

        return formatted_info, info_users


    def quit(self):
        """Función para cerrar la conexión
        con el servidor.

        Returns:
            bool: True en caso de éxito, False en caso de error.
        """
        buff_size = 4096
        data = 'QUIT'
        
        s = self.socket()
        # mejor que solo send porque este no para hasta fallar o enviar todo
        s.sendall(data.encode())

        # Recibimos los datos.
        data = s.recv(buff_size).decode()
        if data != "BYE":
            print("ERROR en QUIT: ", data)
            return False
        else:
            return True
