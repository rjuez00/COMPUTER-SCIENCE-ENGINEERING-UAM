# Práctica 3: Multimedia
## Rodrigo Juez Hernández y Kevin de la Coba Malam

## Pareja 2 (2391)

### Índice
1. [Introducción](#Introducción)
1. [Desarrollo Técnico](#Desarrollo-Técnico)
   1. [Comunicación con el servidor de descubrimiento](#Comunicación-con-el-servidor-de-descubrimiento)
   1. [Conexión de control](#Conexión-de-control)
   1. [Llamada](#Llamada)
   1. [Transmisión de imágenes](#Transmisión-de-imágenes)
   1. [Control de flujo](#Control-de-flujo)
   1. [GUI](#GUI) 
1. [Esquema alto nivel](#Esquema-alto-nivel)
1. [Conclusiones](#Conclusiones)
   1. [Conclusiones técnicas](#Conclusiones-técnicas)
   1. [Conclusiones personales](#Conclusiones-personales)


### Introducción
En está última práctica se ha implementado un cliente para hacer videollamadas con otros usuarios. Estos usuarios se encuentran en un servidor en el cual tenemos que registrarnos. Una vez registrados se puede llamar y enviar llamadas con los usuarios del servidor.

Las tareas principales en esta práctica son:
* Mejorar la GUI.
* Establecer una conexión con el servidor de descubrimiento.
* Mantener una transmisión de datos correcta usando una conexión específica para el envío de datos y otra conexión para el control.

### Desarrollo técnico.
##### Comunicación con el servidor de descubrimiento
En el archivo _discoverServer.py_ se codifica la comunicación con el servidor de descubrimiento.
Para esta comunicación se crea una clase en la cual inicialmente los atributos de esta son únicamente la dirección del servidor y el puerto TCP.
Los métodos de esta clase están todos orientados a la comunicación con el servidor, por ejemplo el método _register_, registra un usuario en el servidor... Hay que destacar que en cada llamada que se hace a uno de estos métodos antes se crea un socket TCP que se comunica con el servidor, y que siempre que se recoge la respuesta del server se ejecuta el método quit para finalizar la conexión con el servidor.
Esto es así porque en el cliente las conexiones con el servidor de descubrimiento no son lo más frecuente.
##### Conexión de control
En el archivo _callResponses.py_ se codifican las respuestas o peticiones enviadas entre cliente (CALL_ACCEPTED, CALL_DENIED...). Aquí simplemente hay funciones que crean un mensaje, después un socket y por último envían este mensaje a través del socket al cliente que se ha especificado. Pero, ¿cómo se ha especificado un cliente? En la GUI principal se muestran todos los clientes en el servidor, seleccionando uno de los clientes y pulsando el botón para llamar, se ejecuta esta función con todos los datos del cliente.

La conexión de control no solo se implementa aquí, en el archivo _dial.py_ hay una clase la cual maneja conexiones de control, pero estas conexiones se producen cuando la llamada está en curso o se va a iniciar. En este archivo también se manejan las peticiones que se reciben de otros 

##### Threading
Como se ha mencionado anteriormente el primer paso para iniciar una llamada se ejecuta en _dial.py_. En el caso de que seamos nosotros quien llamamos, se ejecutará el método _send_calling_ el cual envía un mensaje al usuario que queremos llamar, si recibimos la llamada se ejecuta el _handlerCalling_, aquí quien recibe la llamada pregunta al usuario si desea cogerla o no.
Pero, ¿cómo llamamos pero a la vez estamos a la espera de una llamada? En la clase dial cada vez que se quiere enviar una llamada se crea un socket y por este se envía una llamada, en cambio para recibir, hay un único socket, este esta siempre a la espera de un mensaje, este socket se ejecuta en un thread aparte del principal, y se encargará de desplegar todo en caso de que se inicie una llamada o de responder a peticiones.

El sistema general consiste en 3 threads como veremos, el primero que veremos es el de control, que ejecuta todo lo relacionado con el control y la clase dial, este thread se encarga de crear los otros dos threads de los que hablaremos ahora.

Recibamos la llamada o seamos nosotros los que llamemos, __desplegamos la transmisión__. Para desplegar la transmisión hace falta crear una instancia de la clase __transmisión__. En esta clase tenemos 2 sockets, un socket de recepción y un socket para enviar. A parte, en el módulo se configura la resolución de las imágenes y se controla en flujo. Una vez se ha creado el objeto _transmisión_, creamos 2 threads uno para enviar datos y otro para recibir:
* __Thread envío de datos__: Este thread es el encargado de enviar los datos recogidos de la webcam o el archivo. Después se usan los sockets para enviar y recibir las imágenes. Al enviar el mensaje se construye el mensaje, incluyendo _número de frame_, _tiempo UTC al enviar_, _resolución_, los _fps_ y por último los bytes de las imágenes, todo separado por '#'.
* __Thread recepción de datos__: Este thread es el encargado de recibir los datos. Antes de esperar la recepción se ejecuta la función _select_, para tener en cuenta también a la pipe para cerrar. En este thread se maneja el control de flujo. 

Para comunicar los 3 hilos (uno de control y los dos de envio y recepcion de imagenes) se usan pipes, esto es por que python no permite enviar señales a los threads, tuvimos bastantes problemas para colgar ya que era un evento que pasaba en el proceso principal y queriamos enviarselo a los threads por señales, finalmente lo que hicimos es usar la función _select()_, la cual aprendimos a usarla al hacer el opcional de la primera práctica. El select lo combinamos con threading events para pausar y para parar, aquí explico mejor por cada hilo como manejabamos los threading Events y las pipes:

* __Thread control__: Este thread tiene un recv en el que se queda bloqueado esperando a recibir peticiones nuevas, lo que hicimos fue modificarlo para tener un select(), en el que pusimos los dos descriptores de fichero, uno el socket por el que recibe datos, y otro la pipe que le comunica con el proceso principal, cuando salia del bloqueo del select() comprobamos que descriptor ha sido activado y si es la pipe significa que el usuario ha pulsado colgar, asi que procedemos a usar otras dos pipes para avisar a los threads de recepcion y envio que han de colgar.

* __Thread envío datos__: Este thread se encarga de enviar datos, cuando el threading Event pausaLlamada se pone a False, se queda parado en el pausaLlamada por lo tanto no envía más frames hasta que vuelva a ser True.

* __Thread recepción datos__: Este thread es el que más complicación tenía porque se quedaba congelado en el recv y no conseguíamos sacarlo en caso de que se colgase la llamada, por eso se nos ocurrió usar el select con pipes. Cuando vamos a recibir un dato tenemos un select, el cual recibe tanto la pipe como el socket y si se devuelve la pipe sabemos que es colgar, y si se devuelve el socket simplemente mostramos el frame normalmente, el threadingEvent pausaLlamada funciona igual que con el envío de datos, hay un wait en el que se para el bucle hasta que se setea a True.

En el protocolo V0 puedes cambiar la calidad de la llamada usando la caja de opciones visible en la interfaz de llamada.
En el protocolo V1 se sigue permitiendo usar este menú, pero también se cambia la calidad de forma automática.

##### Control de flujo
##### V1
Como parte ___opcional___ hemos decidido implementar un sistema para controlar la calidad (calidad de imagen, compresión de esta, fps y la tolerancia a pérdidas) a la vez que controlamos el flujo. el control de flujo usamos la fórmula dada en las diapositivas de teoría: 

_estimación dinámica del retardo = (1-constante fija) · retardo anterior + constante fija · (tiempo actual - tiempo en que se envió el paquete)_

Para hacer el retardo dinámico lo que hacemos es que dependiendo del valor que calculemos enviamos un mensaje de control. Para controlar la calidad de la imagen recibida  y los fps, se envía el mensaje "CALL META <nivel>", donde _<nivel>_ se refiere a cómo de bien la llamada está funcionando. Si recibimos un __3__ significa que la llamada funciona correctamente, en este caso aumentamos la calidad y los fps (si es posible ya que hemos establecido un máximo). Si recibimos un 2 significa que la llamada no va muy bien, y que si es posible habría que bajar un nivel la calidad de la llamada. Si recibimos un 1 significa que la llamada está funcionando muy mal, por lo que sí es posible bajamos 2 niveles la calidad. 

"CALL_META" son mensajes que se envían entre clientes para controlar la calidad de imágenes que se deben enviar dadas ciertas condiciones en la red. Este mensaje se envía a través de la conexión de control, tratamos de no saturar la red creando nuevas conexiones o envíando estos mensajes de manera muy frecuente.

De esta manera el que recibe informa al que envía si tiene problemas para recibir los paquetes o por el contrario todo va correcto y puede subir la calidad (a través de CALL_META), y el que envía a partir de esto decide cambiar la calidad de transmisión, no forzamos a que el que recibe pidiese una calidad en específico porque si cambiabamos las resoluciones no se generalizaba, entonces aquí simplemente el que recibe envía CALL_METAS 1 y 2 cuando le va mal o regular y 3 cuando va bien, el que envía va escalando y moviendose por las distintas calidades de envío que tenga ese cliente en específico segun reciba 1, 2 o 3.
Este proceso se hace en ambas direcciones.

Estos tipos de mensajes implementan el protocolo __V1__, el protocolo tiene la funcionalidad añadida de controlar la calidad de las imágenes entre los 4 niveles disponibles que ahora expliquemos para que la fluidez de la llamada siempre la prioridad, la calidad no tiene tanta importancia.

¿Cuantos niveles de _calidad_ hay establecidos? Son 4 niveles:
* LOW. 15 FPS y la calidad 160x120.
* MEDIUM. 19 FPS y la calidad 320x240.
* HIGH. 22 FPS y la calidad 640x480.
* HD. 25 FPS y la calidad 960x720.

A parte, se comprueba la versión implementada por la otra parte, si no tiene la V1 no se enviarán dichos mensajes de control.
Pero ¿con qué frequencia se envían estos mensajes? Para no saturar mucho la conexión de control se envían cada 20 imágenes recibidas (aproximadamente cada segundo). Cada 20 imágenes se comprueba el retraso y se envía el mensaje correspondiente al nivel. Los tramos establecidos para decidir el nivel son:
* Mayor que __0.2__ segundos. Como se nos mencionó en las clases de teoría, un retardo de 0.4 segundos o mayor es molesto para el ser humano, hemos decidido anticiparnos a 0.4 y si el retardo es cercano ir disminuyendo la carga para que no llegar a 0.4. Se enviará el nivel 1 (hay que bajar mucho la calidad).
* Entre __0.1__ - __0.2__ segundos. Para anticipar una caída drástica de la calidad en este tramo se pide que el emisor baje su calidad enviando un nivel 2.
* Menor que __0.1__ segundos. En esta situación la transmisión está funcionando muy mal, el emisor tiene que bajar mucho la calidad. Se envía el nivel 1.

En la misma función donde se hace el control de flujo también se tiene en cuenta un delay. Este delay es el delimita la tolerancia a pérdidas de nuestro cliente. Digamos que recibimos un paquete ahora (el segundo actual es el 10), pero este ha sido enviado hace 8 segundos (segundo 2), si el delay es de 2 segundos ejecutaremos el siguiente cálculo:
_(tiempo de envío del paquete + __delay__) - tiempo actual_
_(2 + 2) - 10 = -6_
Al hacer el cálculo obtendremos un resultado negativo. Esto significa que ese paquete no puede ser mostrado.
Mientras el resultado de este cálculo sea mayor que 0.00001 (sea positivo) y sea suficientemente alto para crear un thread (estuvimos testeando cuanto se tardaba en crear un thread) siempre se mostrarán los paquetes recibidos.
Este ___delay___ se modifica también con los niveles, cuanto más alto el nivel (cuanto mejor funciona la llamada), menor el delay permitido, es decir, se reproducen antes los paquetes recibidos, sin embargo si la calidad es baja aumentamos bastante el delay con el que se reproducen, porque si no perdíamos muchos paquetes y se veía muy a tirones.

Para mostrar los paquetes se usa un thread __timer__, este thread se ejecutará en el tiempo calculado (el resultado de la última fórmula usada). Este thread únicamente muestra una imágen sobre el cliente.
###### Testeo del control de flujo
Para testear el control de flujo se usa el script proporcionado para emular una mala conexión. Abrimos dos clientes y llamamos a uno desde el otro, mientras el script está inactivo la llamada tiene la calidad al máximo (dependiendo de la conexión de cada uno), en cuanto empeoramos la conexión, podemos ver que el retardo se hace cada vez más grande, esto provoca que automáticamente el protocolo V1 modifique la calidad enviando mensajes de control.

##### GUI
Para la interfaz gráfica se usa la librería _APPJAR_. La librería está limitada en opciones, no es muy extensa y eso hace que sea simple de usar.

Tenemos varias ventanas que se usan durante la ejecución del cliente:
1. La primera ventana es la venta de ___login___, en esta ventana simplemente pedimos al usuario que introduzca sus datos (nickname, contraseña, puertos TCP y UDP). La ventana tiene 2 botones, uno para cancelar el registro/login y otro para ejecutar dicha acción. Hay que tener en cuenta que las entradas son especiales, no son simples entradas de texto (exceptuando la del nickname). El password oculta la entrada y la entrada de los puertos solo aceptan dígitos.
Los botones son eventos que tienen asociada una función a ejecutar cuando uno se pulsa. En la pantalla de login la función asociada es _login_buttons_, aquí comprobamos que botón se ha pulsado (acabando o continuando con la ejecución).
2. La estructura anterior de los botones se repite en la ___pantalla principal___. La pantalla principal esta compuesta por:
    * Una __lista de los usuarios__ del servidor con la última conexión.
    * Un __buscador__ de usuarios que actualiza la lista anterior.
    * Un __botón para actualizar__ la lista de los usuarios.
    * Un __boton para llamar__ a un usuario  seleccionado en la lista de usuarios.
    * Una __caja de opciones__ para seleccionar si queremos llamar usando la webcam o un archivo.
    * Una __entrada__ para llamar a un usuario en específico. Si la entrada contiene texto, siempre se llamará al usuario especificado en la entrada de texto, independientemente de si hay algún otro seleccionado en la lista. Para escoger un usuario de la lista simplemente habrá que quitar el texto de la entrada.
3. La ___interfaz de llamada___ está compuesta por:
    * Un _botón_ para __pausar__ la llamada.
    * Un _botón_ para __colgar__ la llamada.
    * Una _caja de opciones_ con la __resolución__ a la que enviar los datos.
    * Un _botón_ para aplicar dicha resolución.
    * Un _cuadro_ con la imágen de lo que nosotros enviamos situada en la esquina inferior izquierda.
    * Un _cuadro_ con la imágen que nosotros recibimos, este cuadro abarca casi toda la pantalla.

Antes de llamar si elegimos usar un archivo local en vez de la webcam, se nos abrirá un explorador de archivos para elegir el vídeo que queremos transmitir. Lo mismo sucede si al recibir la llamada especificamos que no queremos usar una webcam.

Otra cosa importante a mencionar es que si se minimiza la ventana de llamada, el número de paquetes enviados y recibidos disminuye. Durante el testeo del cliente hemos sido capaces de detectar este suceso.

Como algo ___adicional___, el usuario entenderá mejor el cliente ya que no necesita establecer los puertos a usar. Estos se establecen automáticamente mediante las variables de entorno _SRC_PORT_ y _CONTROL_PORT_.
El proceso detrás es el siguiente:
1. Se consultan las variables de entorno.
2. En el login, en el apartado "Avanzado" se pueden establecer manualmente los puertos, se consultan estos si no existen las variables de entorno.
3. Si no estan las variables de entorno, y el usuario no es avanzado y no ha seleccionado los puertos que quiere se usan los que vienen en config.py por defecto.

### Esquema alto nivel
Podemos dividir el código en varios módulos:
* Comunicación con el servidor de descubrimiento: __src/discoverServer.py__
* Conexiones de control: __src/dial.py__ y __src/callResponses.py__.
* Transmisión de imágenes: __tsrc/ransmision.py__.
* Configuración de IP y puertos: __src/config.py__.
* Cliente: __practica3_client.py__.
* Imágenes para el cliente: __imgs/__

### Conclusiones
##### Conclusiones técnicas
La práctica nos ha ayudado a entender el funcionamiento de una llamada (o un intercambio de datos en tiempo real). Nos ha enseñado también a valorar el envío de datos entre los participantes de la llamada. Nos ha ayudado también a entender librerías tales como __cv2__ (uso de imágenes) y por último el uso de appjar como GUI.
La parte que ha requerido un esfuerzo mayor en la práctica ha sido el envío y la recepción correctos de datos. Python no resulta un desafío, pero en esta práctica hay que tener en cuenta la ejecución de 2 partes, el emisor y el receptor, y a parte hay que codificar el cliente teniendo cuenta que vamos a ser ambas partes.
En cuanto a appjar, nos ha costado acostumbrarnos a sus funciones y como usarlo, pero una vez entendimos su funcionamiento todo fue mejor.
Respecto al threading en python, opinamos que deja mucho que desear, ya que los threading events no sustituyen a enviar señales como si se puede hacer en c, además no se puede enviar señales a los threads, lo cual fue un quebradero de cabeza para la opción de colgar, que no conseguíamos hacer con un threading Event ya que se quedaba congelado en el recv, nuestra solución al final fue comunicar los threads mediante pipes como ya hemos explicado, pero esta solución no es la más eficiente.
En conclusión, se ha aprendido mucho en la práctica.

##### Conclusiones personales
Lo único que podemos decir es que la la práctica está bien, pero como tenemos más prácticas de otras asignaturas es difícil dedicarle el tiempo que nos gustaría a esta pŕactica. La práctica es extensa, pero nos ha dejado un sabor de boca decente.



