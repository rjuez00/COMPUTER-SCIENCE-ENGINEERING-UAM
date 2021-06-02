# Práctica 2: Seguridad y criptografía
## Rodrigo Juez Hernández y Kevin de la Coba Malam

## Pareja 2 (2391)

### Índice
1. [Introducción](#Introducción)
1. [Desarrollo Técnico](#Desarrollo-Técnico)
   1. [Esquema híbrido](#Esquema-híbrido)
   1. [Cliente y sus argumentos](#Cliente-y-sus-argumentos)
   1. [Comunicación con la API](#Comunicación-con-la-API)
   1. [Uso de protolos criptográficos](#Uso-de-protolos-criptográficos)
1. [Esquema alto nivel](#Esquema-alto-nivel)
1. [Conclusiones](#Conclusiones)
   1. [Conclusiones técnicas](#Conclusiones-técnicas)
   1. [Conclusiones personales](#Conclusiones-personales)


### Introducción
Todo lo que esta escrito en este archivo también se puede consultar desde la wiki de GitLab.

Hemos desarrollado un cliente el cual mediante la API REST https://vega.ii.uam.es:8080 realiza peticiones para crear y destruir usuarios; subir, descargar y eliminar archivos del servidor; y por último cifrar y descifrar archivos mediante el uso de un esquema híbrido de encriptación el cual usa __AES__, __RSA__ y la función __hash SHA256__.
En este documento desarrollaremos el proceso mediante el cual hemos construido el cliente y como hemos usado los diferentes protocolos de encriptación.
### Desarrollo técnico.
El cliente debe ser capaz de ejecutar comandos con los que ejecutar las acciones especificadas en el enunciado. Hay que tener en cuenta que no todos los comandos ejecutan una acción, hay comandos que son "complementarios" a otros un ejemplo sería:

```txt
securebox --dest_id 34FAB7 --upload doc_secreto.pdf
```
En este comando por ejemplo ```--dest_id``` es complementario a ```--upload```.

NOTA: Se incluye un script vaciar.sh para limpiar todos los archivos del servidor.

Teniendo esto en cuenta el desarrollo del cliente se puede dividir en __4__ partes:
##### Esquema híbrido
El cliente usa un esquema híbrido para cifrar previamente mencionado. Hay 2 pasos funcdamentales, firmar (SHA256) y cifrar (RSA y AES). Para hacer un uso correcto del esquema seguimos los siguientes pasos:
1. Firmar el contenido.
2. Concatenar la firma y el contenido sin cifrar.
3. Mediante una clave aleatoria AES, cifrar el contenido anterior [2].
4. Cifrar la llave AES mediante el protocolo RSA, usando la llave pública del receptor.
5. Concatenar el vector de inicialización AES, la llave AES encriptada y los datos encriptados por AES [3].

Las claves se guardan en archivos .pem. En cuanto al formato a usar en la clave RSA, se nos especifico que debía ser _PEM_, en este punto dudamos con las opciones _DER_ y _OpenSSH_, siendo el primero en formato binario el último al igual que _PEM_ en formato textual.
##### Cliente y sus argumentos.
En primer lugar debemos definir la lógica del cliente, esto lo hicimos en el archivo __src/securebox__ . Como se nos describe en el enunciado el cliente tiene una lista de comandos por los cuales se ejecutan unas acciones. Para recoger estos comandos usamos la librería de python __argparse__. Gracias a esta librería guardamos en un diccionario el comando a ejecutar como "key" (por ejemplo create id) y los argumentos necesarios para este comando como valor (create id: argumentos). 
Gracias a que los datos están en un diccionario, podemos ejecutar todos los que se introduzcan iterando sobre las "keys", o bien si es necesario, acceder a esos comandos complementarios para tener una ejecución correcta.

Después de implementar la lectura de los comandos tuvimos que mapear funciones a cada uno de estos comandos. Esto lo hicimos mediante un segundo diccionario en el que la clave es una string la cual es exactamente igual al nombre del comando (por ejemplo, "create_id": <función>create_id).

Para añadir más seguridad al cliente se ha implementado un menú por el cual el usuario debe introducir una contraseña. Entregamos la práctica con contraseña inicial "admin", puede ser cambiada si ejecutamos el cliente con la opción ```--change_password```, no son necesarios argumentos, se pide primero la contraseña actual y después la nueva. Mientras la contraseña es introducida se ocultan los caracteres en pantalla, después usamos sobre los bytes de la contraseña la función hash SHA256.

Para facilitar el uso del cliente cada vez que el usuario trate de hacer una petición con un token incorrecto, se le muestra en pantalla el link para solicitar un nuevo token. También, se pide un token nuevo si, por ejemplo, ejecutamos el programa por primera vez.
Otra cosa que se ha añadido es que si se manda una petición relacionada con un archivo y esta petición devuelve error, automáticamente se listan los archivos en el servidor. A su vez, si el error es en relación a un usuario, se le muestra el comando a usar para buscar usuarios.


El cliente dispone de un archivo ```config.py``` en el cuál se guarda la __URL__ de la API y los endpoints necesarios para diferentes acciones. Son variables globales que pueden ser accedidas por archivos como ```files.py``` y ```petitions.py```.
##### Comunicación con la API
El primer paso para comunicarnos con la API es el de conseguir un token. Una vez tenemos el token este lo metemos en el archivo __tokens.dat__ y de esta forma podemos comunicarnos con la API usando nuestro token. Todas las comunicaciones se  realizan en los archivos __src/petitions__ y __src/files__, donde estan las funciones de información de la API y gestión de archivos respectivamente.

Para realizar una petición debemos construir un mensaje POST HTTP el cual contenga en las cabeceras el token, y en el objeto de la petición los argumentos necesarios para el comando, en formato JSON. Esto lo hacemos mediante el uso de la librería __requests__.
En esta parte del desarrollo decidimos introducir colores a los mensajes, de esta forma, el texto es más legible.
En cuanto a las respuestas de la API, el control de errores lo hacemos consultando el _"status code"_ de la petición. Dependiendo del comando ejecutado formateamos la respuesta e imprimos el resultado o guardamos en un archivo el contenido recibido.

En el comando "create id" se nos da la posibilidad de establecer un alias, el cual usaremos para referirnos al cliente, y si no se nos proporciona simplemente no le damos mensajes personalizados. A parte en este comando creamos un par de claves RSA para que así podamos recibir o enviar datos.

En cuanto al manejo de los archivos, a la hora de hacer ```--upload```  abrimos el archivo a subir y lo cargamos en memoria leyendo los bytes. Una vez en memoria obtenemos la clave pública RSA del receptor y firmamos y ciframos el archivo, tras esto lo enviamos. En el caso de  ```--download```, el procedimiento es similar, esta vez se cargan en memoria los datos tras enviar la petición, después separamos los distintos componentes (clave AES y contenido del archivo) desciframos los datos y comprobamos la firma del archivo, volvemos a separar el archivo y lo guardamos en un archivo, con el nombre proporcionado en "content-disposition".

##### Uso de protolos criptográficos
La implementación de estos protolos la hicimos en el archivo __src/crypto__. Podemos distinguir 2 procedimientos principales:
* __cifrar__. El primer paso es firmar el contenido del archivo usando la función hash __SHA256__. Una vez firmado usamos la clave pública del receptor y ciframos la firma con esta clave usando la un objeto __PKCS1_v1_5__, que pertenece a la librería _cryptodome__. Estos 2 pasos se encuentran en la función "sign" la cual concatena la firma y el contenido del archivo sin cifrar ni firmar.
Tras usar _sign_, usamos el protocolo AES para cifrar el contenido. El vector de inicialización y la clave las generamos aleatoriamente. Una vez cifrado el contenido usamos un objeto __PKCS1_OAEP__ con la clave pública del receptor para cifrar la clave AES. Estos 2 pasos se encuentran el función "encrypt".
Estos son los pasos y las funciones necesarias para cifrar un fichero. La función "encrypt_sign" realiza la firma y el cifrado del fichero.
* __Descifrar__. Para descifrar seguimos el mismo esquema que al cifrar pero en el orden contrario.
Comenzariamos obteniendo el vector de inicialización, usamos la llave privada con un objeto __PKCS1_OAEP__ para desCifrar los bytes donde se encuentra la clave AES. Con la clave AES desencriptamos los bytes correspondientes al contenido y habríamos obtenido el contenido firmado.
Todo esto se hace en la función "decrypt". Para deshacer la firma usaremos la función "unsign" tras la cual debemos comprobar si no se ha modificado el archivo, es por eso que la función devuelve 2 cosas, la primera los datos y la segunda, si la firma coincide o no.

### Esquema alto nivel
Podemos dividir el código en varios módulos:
* Cliente y su lógica. __src/securebox__.
* Comunicación. __src/config.py__.
   * Comunicación textual e información. __src/petitions__.
   * Comunicación relacionada con archivos __src/files__
* Criptografía. __src/crypto__.
* Tests.  Este módulo esta formado por varios archivos .py. __pruebas/*.py__.
* Archivos con claves y tokens. __appdata/*.pem__, __appdata/token.dat__.

### Conclusiones
##### Conclusiones técnicas
El desarrollo de la práctica ha reforzado nuestro conocimiento de la criptografía, el hecho usar un esquema híbrido implíca que debamos conocer AES y RSA.
Usar python resulta cómodo, la simpleza de la sintaxis facilitó el desarrollo del programa.
##### Conclusiones personales
Comparada con la práctica anterior, esta es mucho más corta. Esto nos ayuda buscar errores en nuestro código y mejorar el programa. Usar python en vez de C también simplifica mucho las cosas, nos ha permitido despreocuparos del manejo correcto de la memoria y nos ha ahorrado tiempo.
La práctica es completa, ya que usamos un protocolo de cifrado simétrico y otro asimétrico, y también usamos funciones hash para comprobar la veracidad de los datos que recibimos. 
En conclusión, hemos aprendido mucho en esta práctica.
