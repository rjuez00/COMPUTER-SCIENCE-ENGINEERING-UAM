"""Archivo donde se manejan todas las peticiones
relacionadas con el uso de archivos.

Authors:
    Rodrigo Juez y Kevin de la Coba
"""
import requests
import json
import crypto
from pathlib import Path
import config
import tokens
from petitions import *


def list_files(token, arguments, cmd_line):
    """Función para listar los archivos del
    servidor mediante la API.

    Args:
        token (str): Token para usar la API
        arguments: No se usa
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    url = config.URL+config.FILE_LIST

    # Enviamos petición
    r = requests.post(url, headers=token)

    print(f"Solicitando archivos disponibles para descargar en el "
          f"servidor...{bcolors.OKGREEN}OK{bcolors.ENDC}")

    # Error
    if r.status_code != 200:
        log_error("list_id", r.status_code, r.text)
        return
    response = json.loads(r.text)
    print(f"{response['num_files']} archivos disponibles: ")

    # Imprimimos los archivos
    for archivo in response['files_list']:
        print(archivo)


def delete_file(token, arguments, cmd_line):
    """Función para eliminar un archivo del servidor
    mediante una petición de la API.

    Args:
        token (str): Token para usar la API.
        arguments (str): Id del fichero a eliminar
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    url = config.URL+config.FILE_DELETE

    # Construimos los argumentos
    args = {'file_id': arguments}
    print(f"Solicitando eliminado de archivo "
          f"{arguments} del servidor...{bcolors.OKGREEN}"
          f"OK{bcolors.ENDC}")

    # Enviamos petición
    r = requests.post(url, json=args, headers=token)

    # Error
    if r.status_code != 200:
        log_error('delete_file', r.status_code, r.text)
        return
    response = json.loads(r.text)

    print(response)
    print(f"Archivo con ID#{bcolors.UNDERLINE}"
          f"{response['file_id']}{bcolors.ENDC} "
          f" borrado correctamente")


def upload(token, arguments, cmd_line):
    """Función para subir archivos al servidor
    mediante una petición de la API.

    Args:
        token (str): Token para usar la API.
        arguments (list): Lista de argumentos que contiene
        el ID del archivo y el tamaño de este.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    if cmd_line.get('dest_id') is False:
        print(f"{bcolors.FAIL}HELP: para usar upload "
              f"debes especificar --dest_id {bcolors.ENDC}")
        return

    # Cargamos el contenido del fichero
    try:
        with open(arguments, "rb") as f:
            data = f.read()
    except IOError:
        print(f"{bcolors.FAIL}No existe el archivo "
              f"{arguments} {bcolors.ENDC}")
        return

    print("Solicitando envío de fichero a SecureBox")

    # Obtenemos la clave pública del receptor
    print(f"-> Recuperando la clave pública de ID{cmd_line['dest_id']}")
    received_key = get_public_key(token, cmd_line['dest_id'])
    if received_key is None:
        return

    print(f"-> Encriptando y firmando archivo "
          f"{arguments} para {cmd_line['dest_id']}...")
    data = crypto.encrypt_sign(crypto.get_receiver_RSA_key(received_key),
                               crypto.get_private_RSA_key(PRIVATE_KEY_LOC),
                               data)

    print(f"-> Subiendo fichero a servidor...")
    url = config.URL+config.FILE_UPLOAD

    # Enviamos petición
    r = requests.post(url, headers=token, files={'ufile': (arguments, data)})

    # Error
    if r.status_code != 200:
        log_error("upload", r.status_code, r.text)
        return
    response = json.loads(r.text)
    print(f"Subida realizada correctamente, ID del fichero "
          f"{response['file_id']}")


def download(token, arguments, cmd_line):
    """Función para descargar un fichero del servidor
    mediante una petición de la API.

    Args:
        token (str): Token para usar la API.
        arguments (str): ID del archivo a descargar.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    if cmd_line.get('source_id') is False:
        print(f"{bcolors.FAIL}HELP: para usar "
              f"download debes especificar --source_id {bcolors.ENDC}")
        return

    url = config.URL+config.FILE_DOWNLOAD

    # Construimos los argumentos
    args = {'file_id': arguments}

    print("Descargando fichero de SecureBox")

    # Enviamos petición
    r = requests.post(url, json=args, headers=token)

    # Error
    if r.status_code != 200:
        log_error('download', r.status_code, r.text)
        return
    print(f"-> {len(r.content)} bytes descargados correctamente")

    # Desencriptamos los datos
    data = crypto.decrypt(crypto.get_private_RSA_key(PRIVATE_KEY_LOC),
                          r.content)
    print(f"-> Descifrando fichero...")

    # Obtenemos la clave pública del receptor
    public_key = crypto.get_receiver_RSA_key(
        get_public_key(token, cmd_line['source_id']))
    print(f"-> Recuperando la clave pública de ID{cmd_line['source_id']}")

    data, correcto = crypto.unsign(public_key, data)

    # Comprobamos si la firma es correcta y
    # no ha habido ninguna modificación
    if correcto is True:
        print(f"-> Verificando firma...{bcolors.OKGREEN}OK{bcolors.ENDC}")
    else:
        print(f"-> Verificando firma...{bcolors.FAIL}FALLO{bcolors.ENDC}")
        print("\t-> Se guardará el archivo igualmente")

    filename_encripted = r.headers['Content-Disposition'].split('\"')[1]
    print(f"Guardando el archivo encriptado en "
          f"{filename_encripted} para {cmd_line['source_id']}...")
    f = open(filename_encripted, 'wb')
    f.write(data)
    f.close()


def get_public_key(token, userID):
    """Función para obtener la clave pública de un
    user ID.

    Args:
        token (str): Token para usar la API.
        userID (str): Id del usuario del que obtenemos
        la clave.

    Returns:
        Clave pública RSA del usuario.
    """
    url = config.URL+config.USER_GETPUBLICKEY

    args = {'userID': userID}

    r = requests.post(url, headers=token, json=args)
    if r.status_code != 200:
        log_error('get_plubic_key', r.status_code, r.text)
        return
    response = json.loads(r.text)
    return response['publicKey']


def encrypt(token, arguments, cmd_line):
    """Función para encriptar un fichero

    Args:
        token (str): Token para usar la API.
        arguments (str): Ruta al fichero a encriptar.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    if cmd_line.get('dest_id') is False:
        print(f"{bcolors.FAIL}HELP: para usar "
              f"encrypt debes especificar --dest_id {bcolors.ENDC}")
        return

    print('Solicitando la clave pública')
    received_key = get_public_key(token, cmd_line['dest_id'])

    print(f"Encriptando archivo {arguments} para {cmd_line['dest_id']}...")
    try:
        with open(arguments, "rb") as f:
            data = f.read()
    except IOError:
        print(f"{bcolors.FAIL}No existe el archivo "
              f"{arguments} {bcolors.ENDC}")
        return

    file_encrypted_bytes = crypto.encrypt(
        crypto.get_receiver_RSA_key(received_key), data)

    filename_encripted = 'encrypted_' + cmd_line['dest_id'] + '_' + arguments
    print(f"Guardando el archivo encriptado en "
          f"{filename_encripted} para {cmd_line['dest_id']}...")
    f = open(filename_encripted, 'wb')
    f.write(file_encrypted_bytes)
    f.close()


def sign(token, arguments, cmd_line):
    """Función para firmar un fichero.

    Args:
        token (str): Token para usar la API (no es necesario).
        arguments (str): Ruta al fichero
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    # Cargando los datos del fichero
    try:
        with open(arguments, "rb") as f:
            data = f.read()
    except IOError:
        print(f"{bcolors.FAIL}No existe el archivo "
              f"{arguments} {bcolors.ENDC}")
        return

    # Firmando el fichero
    file_signed_bytes = crypto.sign(
        crypto.get_private_RSA_key(PRIVATE_KEY_LOC), data)

    filename_signed = 'signed_'+arguments

    print(f"Firmando archivo {arguments}...")

    # Guardando archivo firmado
    f = open(filename_signed, 'wb')
    f.write(file_signed_bytes)
    f.close()


def enc_sign(token, arguments, cmd_line):
    """Función para encriptar y firmar un ficher.

    Args:
        token (str): Token para usar la API.
        arguments (str): Ruta al fichero.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    if cmd_line.get('dest_id') is False:
        print(f"{bcolors.FAIL}HELP: para usar enc_sign debes "
              f"especificar --dest_id {bcolors.ENDC}")
        return

    # Cargando el contenido del fichero
    try:
        with open(arguments, "rb") as f:
            data = f.read()
    except IOError:
        print(f"{bcolors.FAIL}No existe el archivo "
              f"{arguments} {bcolors.ENDC}")
        return

    print("Encriptando archivo")

    print(f"-> Recuperando la clave pública de ID{cmd_line['dest_id']}")
    received_key = get_public_key(token, cmd_line['dest_id'])

    # Encriptamos el contenido
    print(f"-> Encriptando y firmando archivo "
          f"{arguments} para {cmd_line['dest_id']}...")
    data = crypto.encrypt_sign(crypto.get_receiver_RSA_key(received_key),
                               crypto.get_private_RSA_key(PRIVATE_KEY_LOC),
                               data)

    filename_encripted = 'encrypted_signed_'\
        + cmd_line['dest_id'] + '_' + arguments

    print(f"Guardando el archivo encriptado y "
          f"firmado en {filename_encripted} para {cmd_line['dest_id']}...")
    f = open(filename_encripted, 'wb')
    f.write(data)
    f.close()
