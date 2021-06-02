"""Archivo donde se define el
uso y manejo del token.

Authors:
    Rodrigo Juez y Kevin de la Coba
"""
import json
import os


def create_alias(token_loc, token, alias=None):
    """Función para crear un alias.

    Args:
        token_loc (str): Ruta al token.
        token (str): Token.
        alias (str, optional): Alias. Por defecto None.

    Returns:
        str: Alias
    """
    if not os.path.exists(token_loc):
        with open(token_loc, 'w'):
            pass

    if alias is None:
        alias = ""
    tokens = {}
    tokens[alias] = token

    # Escribiendo en el archivo
    out_file = open(token_loc, "w")
    json.dump(tokens, out_file, indent=4)
    out_file.close()

    return alias


def delete_token(token_loc, alias=None):
    """Función para borrar el token.

    Args:
        token_loc (str): Ruta al token
        alias (str, optional): Alias. Por defecto None.
    """
    if alias is None:
        alias = ""

    try:
        os.remove(token_loc)
    except IOError:
        pass


def get_file_token(token_loc):
    """Función para obtener del token.

    Args:
        token_loc (str): Ruta al token.

    Returns:
        dict: Header con el token para las peticiones
        y el alias
    """
    try:
        with open(token_loc, "rb") as f:
            data = f.read()
        token = json.loads(data)
    except IOError:
        return (None, None)

    if len(token) == 0:
        return (None, None)
    return ({'Authorization': 'Bearer ' + list(token.values())[0]},
            list(token.keys())[0])
