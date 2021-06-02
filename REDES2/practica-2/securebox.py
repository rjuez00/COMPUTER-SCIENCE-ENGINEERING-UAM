import sys
sys.path.insert(0, './src')

import argparse
from files import *
from petitions import *
import tokens
from crypto import check_password


# Parseando argumentos
parser = argparse.ArgumentParser(description='Servicio SecureBox')
parser.add_argument('--create_id', dest='create_id', default=False,
                    help='Crear nueva identidad, se necesita nombre, email '
                    + 'y opcionalmente alias', nargs='+')
parser.add_argument('--search_id', dest='search_id', default=False,
                    help='Busca un usuario cuyo nombre o correo electrónico '
                    + 'contenga cadena en el repositorio de identidades de '
                    + 'SecureBox y devuelve su ID')
parser.add_argument('--delete_id', dest='delete_id',  default=False,
                    help='Borra la identidad con ID id registrada '
                    + 'en el sistema. Obviamente, sólo se pueden '
                    + 'borrar aquellas identidades creadas '
                    + 'por el usuario que realiza la llamada.')
parser.add_argument('--upload', dest='upload', default=False,
                    help='Envia un fichero a otro usuario, cuyo ID es '
                    + 'especificado con la opción --dest_id. Pordefecto, '
                    + 'el archivo se subirá a SecureBox firmado y cifrado '
                    + 'con las claves adecuadas para que pueda ser '
                    + 'recuperado y verificado por el destinatario')
parser.add_argument('--source_id', dest='source_id', default=False,
                    help='ID del emisor del fichero.')
parser.add_argument('--dest_id', dest='dest_id',  default=False,
                    help='ID del receptor del fichero.')
parser.add_argument('--list_files', dest='list_files', action='store_true',
                    default=False,
                    help='Lista todos los ficheros pertenecientes al usuario')
parser.add_argument('--download', dest='download',  default=False,
                    help='Recupera un fichero con ID id_fichero del sistema. '
                    + 'Tras ser descargado, debe serverificada la firma y, '
                    + 'después, descifrado el contenido.')
parser.add_argument('--delete_file', dest='delete_file',  default=False,
                    help='Borra un fichero del sistema.')
parser.add_argument('--encrypt', dest='encrypt', default=False,
                    help='Cifra un fichero, de forma que puede ser descifrado '
                    + 'por otro usuario, cuyo ID esespecificado '
                    + 'con la opción --dest_id.')
parser.add_argument('--sign', dest='sign', default=False,
                    help='Firma un fichero.')
parser.add_argument('--enc_sign', dest='enc_sign', default=False,
                    help='Cifra y firma un fichero, combinando '
                    + 'funcionalmente las dos opciones anteriores.')
parser.add_argument('--change_password', dest='change_password', default=False,
                    action='store_true',
                    help='Cambia la contraseña del cliente de SecureBox')


args = vars(parser.parse_args())

token, alias = get_token()

if token is None and (not args['create_id'] and not args['change_password']):
    print(f"Hola, parece que no tienes un token, dirigete a {bcolors.OKBLUE}"
          f"https://vega.ii.uam.es:8080/tokens/{bcolors.ENDC} "
          f"para solicitar un nuevo token y ejecuta el comando --create_id")
    exit()

if alias != "" or alias is not None:
    print(f"Bienvenido a {bcolors.BOLD}{bcolors.OKBLUE}SecureBox " +
           f"{alias}{bcolors.ENDC}{bcolors.ENDC}")


if check_password(PASSWORD_LOC) == -1 and not args['change_password']:
    exit()

# Mapa con las funciones de cada argumento
functions = {'create_id': create_id, 'search_id': search_id,
             'delete_id': delete_id, 'upload': upload,
             'enc_sign': enc_sign, 'sign': sign,
             'encrypt': encrypt, 'delete_file': delete_file,
             'download': download, 'list_files': list_files,
             'change_password': change_password}

for key, value in args.items():
    if value is False:
        continue

    func = functions.get(key)
    if func is not None:
        func(token, value, args)
