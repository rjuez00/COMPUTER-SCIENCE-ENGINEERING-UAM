"""Archivo donde se definen las funciones usadas en
securebox.py. Dichas funciones se encargan de la
comunicación con la API rest:
https://vega.ii.uam.es:8080/

Authors:
    Rodrigo Juez y Kevin de la Coba
"""
import requests
import json
import crypto
from pathlib import Path
import config
import files
import tokens

PRIVATE_KEY_LOC = "appdata/private.pem"  # Ruta a la clave privada
TOKEN_LOC = "appdata/tokens.dat"  # Token para usar la API
PASSWORD_LOC = "appdata/password.bin"


class bcolors:
    """Clase para definir los colores en los print
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def change_password(token, arguments, cmd_line):
    """Función para cambiar la contraseña de
    secure box. Usa la función de crypto.

    Args:
        token (str): Token.
        arguments (list): Lista que contiene str's,
        en concreto nombre, email, publicKey.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    crypto.change_password(PASSWORD_LOC)


def get_token(alias=None):
    """Función que coge el token de la API.

    Returns:
        tupla: Diccionario que contiene el header y el
        alias del usuario que lo creó con el token para la petición.
    """
    return tokens.get_file_token(TOKEN_LOC)


def log_error(function_name, status_code, return_text):
    """Función para imprimir por pantalla un error.

    Args:
        function_name (str): Función que provocó el error.
        status_code (int): Código de respuesta de la API.
        return_text (str): Texto de respuesta de la API.
    """
    print(f"{bcolors.FAIL}ERROR en {function_name}...\n\
        Codigo de error http: {status_code}{bcolors.ENDC}")

    if status_code != 500:
        error_description = json.loads(return_text)
        print(f"\t{bcolors.WARNING}{bcolors.UNDERLINE}"
              f"{error_description['error_code']}: {bcolors.ENDC}"
              f"{error_description['description']}{bcolors.ENDC}")

        # El error está relacionado con la token
        if error_description['error_code'][:3] == "TOK":
            print(f"\tDirigete a {bcolors.OKBLUE}"
                  f"https://vega.ii.uam.es:8080/tokens/{bcolors.ENDC}"
                  f" para solicitar un nuevo token.\n"
                  f"\tEjecute de nuevo securebox y se le solicitara "
                  f"un nuevo token")
            tokens.delete_token(TOKEN_LOC)

        # El archivo en la petición es incorrecto
        if error_description['error_code'] == "FILE2":
            print(f"\tUsa la opción --list_files para ver la lista de"
                  f" archivos disponibles:\n\n ")
            return files.list_files(get_token(), False, None)

        # El ID del usuario es incorrecto
        if error_description['error_code'] == "USER_ID1":
            print(f"\tusa la opción --search <nombre> para buscar el id"
                  f" correcto del usuario")
    else:
        print(f"{return_text}")


def create_id(token, arguments, cmd_line):
    """Función para crear un ID en el servidor a traves
    de una petición de la API.

    Args:
        token (str): Token para usar la API.
        arguments (list): Lista que contiene str's,
        en concreto nombre, email, publicKey.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    url = config.URL+config.USER_REGISTER

    nombre = str(arguments[0])
    email = str(arguments[1])

    msg = "Hola, parece que no tienes ningún token o no es válido, "\
        + "por favor introduce un nuevo token: "
    if token is None:
        token = {'Authorization': 'Bearer ' + input(msg)}

    stripped_token = token['Authorization'].split(" ")[1]

    if len(arguments) == 2:
        tokens.create_alias(TOKEN_LOC, stripped_token)
    else:
        tokens.create_alias(TOKEN_LOC, stripped_token, arguments[2])

    # Obtenemos la clave pública RSA
    public_key = crypto.generate_RSA_keys(PRIVATE_KEY_LOC)
    print(f"Generando par de claves RSA de {crypto.RSA_SIZE}"
          f"bits...{bcolors.OKGREEN}OK{bcolors.ENDC}")
    print(f"Creando usuario:\n\t{nombre}\n\t{email}")

    # Construimos los argumentos para la petición a la API
    args = {'nombre': nombre,
            'email': email,
            'publicKey': public_key.decode('utf-8')}

    # Petición a la API
    r = requests.post(url, headers=token, json=args)

    # Error en la petición
    if r.status_code != 200:
        log_error("create_id", r.status_code, r.text)
        return

    response = json.loads(r.text)

    print(f"\nIdentidad con ID#{bcolors.UNDERLINE}"
          f"{response['userID']}{bcolors.ENDC} creada correctamente")


def search_id(token, arguments, cmd_line):
    """Función para buscar una ID dentro del servidor
    mediante una petición de la API.

    Args:
        token (str): Token para usar la API.
        arguments (str): Cadena de busqueda.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    url = config.URL+config.USER_SEARCH

    # Construimos los argumentos
    args = {'data_search': str(arguments)}

    # Enviamos petición
    r = requests.post(url, headers=token, json=args)

    # Error
    if r.status_code != 200:
        log_error("search_id", r.status_code, r.text)
        return
    response = json.loads(r.text)

    print(f"Buscando usuario \'{arguments}\' en el servidor..."
          f"{bcolors.OKGREEN}OK{bcolors.ENDC}\n{len(response)}"
          f" usuarios encontrados:")

    # Imprimimos los usuarios
    for index, usuario in zip(range(1, len(response)+1), response):
        print("[{}] {}, {}, ID: {}".format(index,
                                           usuario['nombre'],
                                           usuario['email'],
                                           usuario['userID']))


def delete_id(token, arguments, cmd_line):
    """Función para eliminar un usuario del servidor
    mediante la API.

    Args:
        token (str): Token para usar la API.
        arguments (str): ID del usuario a eliminar.
        cmd_line (dict): Diccionario que contiene todos
        los argumentos utilizados en el comando de securebox.py.
    """
    url = config.URL+config.USER_DELETE

    # Construimos los argumentos
    args = {'userID': arguments}

    # Enviamos petición
    r = requests.post(url, json=args, headers=token)
    print(f"Solicitando borrado de la identidad "
          f"{bcolors.UNDERLINE}{arguments}{bcolors.ENDC}"
          f"... {bcolors.OKGREEN}OK{bcolors.ENDC}")

    # Error
    if r.status_code != 200:
        log_error("delete_id", r.status_code, r.text)
        return
    response = json.loads(r.text)

    print(f"Identidad con ID#{bcolors.UNDERLINE}"
          f"{response['userID']}{bcolors.ENDC}"
          f" borrada correctamente")
