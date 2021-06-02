# Práctica 1: Servidor Web
## Kevin de la Coba Malam y Rodrigo Juez Hernández
## Pareja 2 (2391)
<img src="htmlfiles/eps.jpg" width="100" style="float: right; margin-right:0px">

### Índice
1. [Introducción](#Introducción)
1. [Desarrollo Técnico](#Desarrollo-Técnico)
   1. [Arquitectura servidor](#Arquitectura-servidor)
   1. [Configuración e Instalación](#Configuración-e-Instalación)
   1. [Diseño Concurrente](#Diseño-Concurrente)
   1. [Librerías .a](#Librerías-.a)
1. [Esquema alto nivel](#Esquema-alto-nivel)
1. [Conclusiones](#Conclusiones)
   1. [Conclusiones técnicas](#Conclusiones-técnicas)
   1. [Conclusiones personales](#Conclusiones-personales)


### Introducción
Todo lo que esta escrito en este archivo también se puede consultar desde la wiki de GitLab.

Hemos desarrollado un servidor web desde cero, programado en C, que responde a peticiones HTTP 1.1.
Este documento tiene el fin de resumir las decisiones técnicas y de diseño implementadas, además de listar todas las peticiones permitidas.


### Desarrollo Técnico
#### Arquitectura servidor
Existen varios tipos de servidores entre los cuales tenemos iterativos y concurrentes. Para la práctica se podría haber implementado un servidor iterativo, ya que al testear el servidor no aplicamos una carga muy grande a este. Por mucho que intentemos enviar peticiones de forma masiva no vamos a ser capaces de replicar el tráfico que un servidor en la red recibe, a pesar de todos los tests que hiciésemos sería difícil ver el rendimiento afectado por estos. Por esta razón el servidor concurrente es una mejor opción. En una situación donde exista bastante tráfico, el servidor concurrente puede atender a varias peticiones al mismo tiempo, esto es una gran ventaja, ya que si nuestro servidor es potente podemos atender a un número mayor de peticiones.

Nuestro servidor es concurrente pero tenemos tenemos un __número fijo__ de "trabajadores", esto limita las capacidades de nuestro servidor ya que puede darse el caso en el que ese número fijo no sea suficiente. Otra opción sería el uso de un número dinámico de "trabajadores", esto permitiría al servidor adaptarse a la situación. El único inconveniente en esta arquitectura es la implementación correcta del servidor.

En un punto de la implementación decidimos contar cuantos "trabajadores" se encontraban trabajando cada vez que se recibia una petición, esto facilitaría una futura implementación de un servidor con un número dinámico. Una forma de hacerlo dinámico podría ser que cada vez que el servidor recibiese una petición este crearía un trabajador, este trabajador podría tener un timeout de forma que cuando el tráfico fuese ligero, el trabajador se quedaría inactivo y por ende moriría.

Aunque el servidor concurrente presenta varias ventajas, a la hora de implementar el servidor decidimos usar un servidor iterativo (estableciendo el número de hilos a 1), de esta forma el servidor pudimos debuguear el código. En la etapa final de la implementación testeamos el servidor con un número de hilos mayor que 1.

En conclusión, para tener un servidor versátil implementamos un servidor concurrente, pero para no complicar demasiado las cosas el servidor tiene un número fijo de trabajadores.

##### Configuración e Instalación
El servidor se deberá configurar mediante el archivo _server.conf_:
```conf
server_root = htmlfiles/
max_clients = 5
listen_port = 8080
server_signature = "Tyrell Corp Server (Nexus 8)"
daemon=false
```
Cambiando las variables podemos configurar el comportamiento del servidor:
* __server_root__: deberá especificar dónde está la raíz del sistema de archivos, se accede con un mapping directo, es decir, si el cliente accede a localhost:8080/prueba.html, el servidor devolverá el archivo que esté en la raíz de server_root y se llame prueba.html, si se quieren hacer subpáginas dentro de la web se hará simplemente con creación de carpetas, por ejemplo todos nuestros scripts están dentro de la carpeta scripts y se accede a ellos: localhost:8080/scripts/test.php.
* __max_clients__: especifica el número de peticiones simultáneas atendidas, esto tendrá relación 1 a 1 con el tamaño del thread pool.
* __listen_port__: el puerto donde escuchará el servidor (en este caso se accedería localhost:8080)
* __server_signature__: este es un campo informativo, en las cabeceras http se debe incluir el nombre del servidor y se usará el nombre especificado aquí.
* __daemon__: si el servidor se ejecuta como daemon no se verá en la terminal y todo el output tanto de información como de error solo se verá reflejado en el syslog.
El parseo de este archivo se implementa mediante la librería __libconfuse.h__ que el sistema operativo del servidor deberá tener instalada.

##### Diseño Concurrente
El tipo de servidor elegido es el 7 __"prethreaded with mutex locking to protect accept"__. Esta decisión fue tomada porque en sistemas UNIX el accept se comporta como un mutex, por lo que varios threads pueden estar en el accept sin que haya condiciones de carrera. Esta implementación nos pareció la mejor entre las disponibles ya que es mucho más sencillo y eficiente la creación de threads, y el _accept_ en el padre nos parecía que gastaría más recursos innecesarios en la comunicación. También nos pareció la mejor manera de preparar todo para que en un futuro se pueda cambiar a una pool dinámica, es decir cuando se estén llegando al número máximo de threads ocupados se creen nuevos hilos. Esto lo hemos conseguido con una variable que es un mutex que comienza en el número de hilos libres, y si entran en el accept hacen down (decrementando el valor) e informan mediante syslog (en el caso de una pool dinámica en vez de informar se haría una comprobación de si se está llegando al número máximo y en ese caso se avisará al padre mediante una simple señal el cual se encargará de crear más hilos y modificar la variable). Cuando terminan hacen up y vuelven a informar de el número de hilos libres.

##### Librerías .a 
Las librerías _.a_ creadas son _server.a_ y _http.a_.
* __server.a__: se encarga de todo lo necesario a bajo nivel, creación de threads (pool_thread.c), sockets (socket.c), logging (log.c) y (servidor.c).
* __http.a__: implementa todo lo necesario para cubrir la especificación HTTP 1.1, esto es el parseo de peticiones (picohttpparser.c), la respuesta a peticiones (http.c) y la ejecución de scripts (cgi.c).




En vez de hacer que cada vez que se procese una petición y cerrar la conexión inmediatamente mediante un _"Connection: close"_ dejamos la conexión abierta y esperamos a que sea el cliente el que nos envíe la petición de cerrar la conexión en cuyo caso ya liberamos el hilo para que espere a otras peticiones. Esta funcionalidad tiene un timeout, ya que algunos navegadores no incluyen en su cabecera la petición de cerrar la conexión.

Los verbos soportados son los básicos _GET, POST y OPTIONS_, además implementamos la funcionalidad __opcional__ de __HEAD__ (es como un _GET_, sin embargo no se envía el contenido, sirve para obtener las cabeceras y status de los archivos sin necesidad de gastar mucho bandwith), estos se pueden ejecutar sobre cualquier recurso disponible, y los códigos de respuesta soportados son:
* __400_ _Bad Request:__ Si el usuario no formula bien la petición se devolverá este código de error.
* __404_ _Not Found:__ Si se intenta acceder a un archivo que no existe.
* __200_ _OK:__ Cualquier petición que tenga contenido y se haya satisfecho.
Y además implementamos otros __opcionales__:
* __413_ _Payload Too Large:__ Si la petición del cliente es demasido larga (aunque ahora es dinámico y realmente nunca se devolverá este error está implementado).
* __415_ _Unspported Media Type:__ Si la petición pide un tipo de archivo que no es soportado por el servidor.
* __405_ _Method Not Allowed:__ Si el method que el cliente ha enviado no es soportado por el servidor.
* __204_ _No Content:__ Cuando devolvemos HEAD y OPTIONS no hay contenido devuelve este código.
* __505_ _HTTP Version not supported:__ Si la versión de HTTP es distinta de 1.1.
* __500_ _Internal Server Error:__ Si ocurre algún error en la ejecución del servidor, ya sea reservando la memoria, o parseando.

Además como funcionalidad __opcional__ extra hemos permitido que, en vez de no enviar contenido con los códigos de error y se muestre una página genérica, el dueño del servidor podrá cambiar el diseño de estas cambiando los archivos errorXXX.html (siendo XXX el código que se desea cambiar el diseño).


Para probar la funcionalidad de scripts CGI, hemos implementado un script muy simple que devuelve el nombre (hola.py), el formato para llamar es el siguiente:
localhost:8080/scripts/hola.py?n1=alberto&n2=kevin&n3=rodrigo

y también una calculadora (calculatora.py), a la cual le pasas argumentos y te devuelve el resultado.
El formato de los argumentos deberá ser el siguiente:
    * __op__: es la operación que se va a ejecutar y puede ser: _sum_, _sub_, _mul_ o _div_
    * __valx__: la x será el orden de la operación y el contenido será el entero que usa, es decir podrá ser val1=0, val2=78, val3=96.

Así un ejemplo de una petición al script podría ser: 
localhost:8080/scripts/calculadora.py?op=sum&val1=1&val2=12&val3=98.

Como funcionalidad extra __opcional__ implementamos un TimeOut con select(), para que si el script se queda bloqueado devuelva un Bad Request. Para comprobar esta funcionalidad se ha creado un script (sleep.py) que se suspende 10 segundos (ya que el TimeOut es de 5 segundos), y así podemos ver que devuelve Bad Request.


### Esquema alto nivel
Los módulos incluidos son los siguientes:
* __socket__: es un wrapper para las funciones de socket, realiza todas las comprobaciones y pasos en la creación, accept y close.
* __servidor__: realiza el parseo de la configuración, inicializa la _struct_ que contiene toda la información del servidor y llama a la creación del pool.
* __pool_thread.h__: se encarga de la creación, ejecución, eliminación y limpieza de los hilos.
* __log.c__: simples funciones para escribir en syslog sin tener que encargarse de abrirlo y cerrarlo.
* __http.c__: se encarga de todo lo relacionado con http, tanto de parsear peticiones, como de gestionar las respuestas.
* __response.c__: genera el contenido de las respuestas http, el módulo http.c llama a este y le indica que tiene que generar y como y este se lo devuelve.
* __picohttpparser.c__: librería externa que facilita el parseo de las peticiones http
* __cgi.c__: se encarga de ejecutar los scripts y devolverle al módulo principal de http el contenido html a partir de los argumentos.

### Conclusiones
##### Conclusiones técnicas
El desarrollo del servidor HTTP nos ha permitido reforzar nuestro conocimiento en 2 aspectos; el manejo de __sockets__ y el __protocolo HTTP__. Para manejar los sockets correctamente tuvimos que seguir el esquema proporcionado en las diapositivas de la práctica. El primer paso sería "crear" el propio socket, para esto simplemente debemos llamar en orden a _socket()_ _bind()_ y _listen()_, así tendremos el socket creado e inicializado pero no estará trabajando, para hacerlo trabajar debemos ejecutar _accept()_. Estos 2 pasos están separados en 2 funciones distintas, para poder crear sockets sin hacer _accept_ inmediatamente.
En cuanto al protocolo HTTP, como ya se ha mencionado anteriormente hacemos uso de este recibiendo e interpretando peticiones (usando _picohttpparser_), y respondiendo al cliente mediante la construcción del mensaje a enviar. La implementación del protocolo en si no es complicada, lo que nos resultó complicado fue el manejo de los descriptores de fichero para enviar respuestas. En nuestra primera implementación de HTTP, respondemos al cliente con una única llamada a _send()_, pensando que esta era nuestra única opción para enviar. Posteriormente nos dimos cuenta de que podíamos usar _send()_ más de una vez. Nuestra implementación envía primero el código, versión y cabeceras, todo en una misma llamada de _send()_, después definimos un tamaño para enviar el objeto en varias iteraciones, básicamente enviamos el objeto en porciones.
Además dejamos preparado el código para que añadir nuevos códigos de respuesta fuese muy sencillo.

El CGI, no resultó complicado debido a que se nos proporcionó un código auxiliar en las diapositivas, simplemente seguimos la estructura proporcionada y lo testeamos. El padre envía por una tubería los argumentos y el hijo redirige dicha tubería a STDIN, después el hijo redirige la tubería a STDOUT, escribimos la ejecución del script en esa tubería y el padre recoge dicha salida.
 
C es un lenguaje en el que hay que poner mucha atención en los detalles, sea tratando punteros, strings, memoria dinámica... Técnicamente esta ha sido nuestra principal dificultad, el manejo correcto de todos estos detalles. En nuestra opinión, la parte más tediosa de la práctica no es el manejo de los sockets o el protocolo HTTP, es el manejo de __C__ y de la gestión de memoria.
 
##### Conclusiones personales
La práctica nos ha reforzado el conocimiento que teníamos en relación con los servidores y sus tipos (iterativos, pool de threads...). También nos ha ayudado a mejorar nuestra agilidad con el lenguaje de programación C, la gestión de la memoria dinámica, la gestón de los socket y la especificación HTTP 1.1 que no solo nos permitirá aprender el funcionamiento de los servidores, si no que también nos permitirá el funcionamiento de internet.
