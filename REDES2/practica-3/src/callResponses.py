"""Archivo donde se implementan las respuestas con un
usuario.

Autores:
    Rodrigo Juez y Kevin de la Coba
"""
import socket

def accept_call(name, source_udp, dest_ip, dest_port):
    """Función para aceptar una llamada. Envía un mensaje
    TCP al usuario que nos llama.

    Args:
        name (str): Nombre del usuario que nos llama.
        source_udp (int): Puerto UDP del usuario que llama.
        dest_ip (str): Dirección IP del usuario que llama.
        dest_port (int): (TCP) Puerto de destino al que responder.
    """
    # Construyendo respuesta
    data = 'CALL_ACCEPTED ' + name + ' ' + str(source_udp)

    # Enviamos la respuesta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dest_ip, dest_port))
    s.sendall(data.encode())


def deny_call(name, dest_ip, dest_port):
    """Función para denegar una llamada. Envía un mensaje
    TCP al usuario que nos llama.

    Args:
        name (str): Nombre del usuario que nos llama.
        source_udp (int): Puerto UDP del usuario que llama.
        dest_ip (str): Dirección IP del usuario que llama.
        dest_port (int): (TCP) Puerto de destino al que responder.
    """
    # Construyendo respuesta
    data = 'CALL_DENIED '+name

    # Enviamos la respuesta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dest_ip, dest_port))
    s.sendall(data.encode())


def busy_call(dest_ip, dest_port):
    """Función para indicar que estamos ocupados y no
    podemos responder una llamada. Se envía un mensaje
    TCP.

    Args:
        name (str): Nombre del usuario que nos llama.
        source_udp (int): Puerto UDP del usuario que llama.
        dest_ip (str): Dirección IP del usuario que llama.
        dest_port (int): (TCP) Puerto de destino al que responder.
    """
    # Construyendo respuesta
    data = 'CALL_BUSY'

    # Enviamos la respuesta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dest_ip, dest_port))
    s.sendall(data.encode())