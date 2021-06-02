"""Archivo donde se maneja el uso de los diferentes
protocolos critográficos tales como RSA y AES.
También se maneja el uso de la función hash SHA256.

Authors:
    Rodrigo Juez y Kevin de la Coba
"""
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import *
from Cryptodome.Random import get_random_bytes
import random
import getpass
import string

RSA_SIZE = 2048
AES_KEY_LENGTH = 32
AES_KEY_ENCRYPED_LEN = 256
IV_LENGTH = 16  # Longitud del vector de inicialización
SIGN_LENGTH = 256  # SHA256


def generate_RSA_keys(private_key_loc):
    """Función para generar keys usando el protocolo RSA.

    Args:
        private_key_loc (str): Ruta a la clave privada.
        public_key_loc (str): Ruta a la clave pública.

    Returns:
        Clave pública RSA.
    """
    # Generando
    key = RSA.generate(RSA_SIZE)

    # Guardando las keys en formato binario
    f1 = open(private_key_loc, 'wb')
    f1.write(key.export_key('PEM'))
    f1.close()

    # El profe ha dicho que en formato PEM
    return key.publickey().export_key('PEM')


def get_private_RSA_key(private_key_loc):
    """Función para obtener la clave privada RSA
    dada la ruta de esta.

    Args:
        private_key_loc: Ruta hacia la clave
        privada.

    Returns:
        Clave privada importada.
    """
    key = open(private_key_loc, "rb").read()
    return RSA.importKey(key)


def get_receiver_RSA_key(key_receiver):
    """Función para obtener la clave pública RSA del
    receptor.

    Args:
        key_receiver: Clave pública RSA.

    Returns:
        Clave pública del receptor importada.
    """
    return RSA.importKey(key_receiver)


"""
ver Example 2:
https://www.programcreek.com/python/example/105075/Cryptodome.Cipher.AES.new

RSA
https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples

Random bytes:
https://pycryptodome.readthedocs.io/en/latest/src/random/random.html


1.- padding de 16 a datos
2.- crear encryptor AES
3.- encriptar datos
4.- encriptar llave
5.- devolver concatenado
"""


def encrypt(RSA_receiver_key, file_content):
    """Funcíon para encriptar el contenido de un
    fichero.

    Args:
        RSA_receiver_key: Clave pública RSA del receptor.
        file_content: Contenido del fichero a encriptar.

    Returns:
        Vector de inicialización concatenado con la llave AES
        encriptada concatenada con los datos encriptados.
    """
    # Vector de inicialización
    IV = get_random_bytes(IV_LENGTH)

    # Clave de AES
    key = get_random_bytes(AES_KEY_LENGTH)

    # 1.- padding de 16
    file_content = pad(file_content, 16)
    # 2.- crear encryptor AES
    mode = AES.MODE_CBC
    AES_encryptor = AES.new(key, mode, IV=IV)
    # 3.- encriptar datos
    encrypted_data = AES_encryptor.encrypt(file_content)

    # 4.- encriptar llave
    RSA_encryptor = PKCS1_OAEP.new(RSA_receiver_key)
    encrypted_key = RSA_encryptor.encrypt(key)
    if len(encrypted_key) != AES_KEY_ENCRYPED_LEN:
        print("error encriptando, la longitud resultante no es la esperada")
        return None

    # 5.- devolver concatenado
    return IV + encrypted_key + encrypted_data


def sign(RSA_key, file_content):
    """Función para firmar el contenido de un fichero.
    Para firmar el contenido se usa:
    1. La función hash SHA256.
    2. La llave RSA y el protocolo en si.

    Args:
        RSA_key: Llave RSA para cifrar.
        file_content: Contenido a cifrar.

    Returns:
        Firma concatenada con el contenido.
    """
    signer = PKCS1_v1_5.new(RSA_key)

    digest = SHA256.new()
    digest.update(file_content)

    sign = signer.sign(digest)
    return sign + file_content


def decrypt(private_key, file_content):
    """Dado el contenido de un fichero ya cifrado,
    lo desciframos extrayendo primero los datos
    interestantes como el vector de inicialización
    la clave AES, y el contenido.

    Args:
        private_key: Clave privada RSA.
        file_content: Contenido cifrado.

    Returns:
        Contenido descifrado.
    """
    # Vector de inicialización
    IV = file_content[:IV_LENGTH]

    key = file_content[IV_LENGTH:(IV_LENGTH + AES_KEY_ENCRYPED_LEN)]
    file_content = file_content[(IV_LENGTH + AES_KEY_ENCRYPED_LEN):]

    # 4.- desencriptar llave
    RSA_encryptor = PKCS1_OAEP.new(private_key)
    key = RSA_encryptor.decrypt(key)

    # 2.- crear encryptor AES
    mode = AES.MODE_CBC
    AES_encryptor = AES.new(key, mode, IV=IV)

    # 3.- desencriptar datos
    file_content = AES_encryptor.decrypt(file_content)

    # 1.- despadding de 16
    file_content = unpad(file_content, 16)

    # 5.- devolver concatenado
    return file_content


"""
RSA_public_key is the key from the sender!


para verificar firmas:
https://www.kite.com/python/docs/Crypto.Signature.PKCS1_v1_5.PKCS115_SigScheme.verify

returns (file_content without sign, true/false, good sign or not)

"""


def unsign(RSA_public_key, file_content):
    """Función para deshacer la firma de un fichero.

    Args:
        RSA_public_key: Clave RSA pública.
        file_content: Contenido en el que deshacer la firma.

    Returns:
        Contenido del fichero y el resultado (bool)
        de la verificación entre el fichero ya firmado y
        una firma efecutada por nosotros.
    """
    sign = file_content[:SIGN_LENGTH]
    file_content = file_content[SIGN_LENGTH:]

    signer = PKCS1_v1_5.new(RSA_public_key)

    # sha256 returns a 256 length key
    digest = SHA256.new()
    digest.update(file_content)

    return file_content, signer.verify(digest, sign)


def encrypt_sign(receiver_key, private_key, data):
    """Función para encriptar datos.

    Args:
        receiver_key: Llave pública RSA del receptor.
        private_key: Llave privada RSA.
        data: Datos a encriptar.

    Returns:
        Datos firmados y encriptados.
    """
    data = sign(private_key, data)
    file_encrypted_bytes = encrypt(receiver_key, data)
    return file_encrypted_bytes


def change_password(PASSWORD_LOC):
    """Función para cambiar la contraseña. Obtiene la
    nueva contraseña y la cifra usando la función hash
    SHA256.

    Args:
        PASSWORD_LOC (str): Ruta a la contraseña.
    """
    new_password_hash_input = bytes(
        getpass.getpass('Introduce la NUEVA contraseña: ',
                        stream=None), encoding='utf8')
    new_password_hash_input = SHA256.new(data=new_password_hash_input).digest()

    out_file = open(PASSWORD_LOC, "wb")
    out_file.write(new_password_hash_input)
    out_file.close()


def check_password(PASSWORD_LOC):
    """Función que obtiene la input del usuario para posteriormente
    evaluarl la contraseña. Dicha contraseña se cifra usando la
    función hash SHA256.

    Args:
        PASSWORD_LOC (str): Ruta al archivo con la password.

    Returns:
        int: -1 Error.
    """
    data = None
    contraseña_anterior = True

    try:
        with open(PASSWORD_LOC, "rb") as f:
            data = f.read()
    except IOError:
        print("No existe contraseña previa, "
              "por favor ejecuta el comando --change_password")
        return -1

    old_password_hash_input = SHA256.new(
        data=bytes(getpass.getpass('Introduce la contraseña: ', stream=None),
                   encoding='utf8')).digest()

    if old_password_hash_input != data:
        print("Contraseña Incorrecta")
        return -1
