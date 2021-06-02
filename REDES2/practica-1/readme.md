#### compilar y ejecutar:
## ¡ALERTA!:
No eliminar la carpeta errors de htmlfiles o siempre devolverá 404 
Al menos en firefox, hasta que no se cierra el navegador no cierra la conexión, entonces cuando se envíe SIGINT no se cerrará el servidor hasta que haya un TIMEOUT o cierres el navegador.

se debe configurar los parametros en server.conf
hay varias opciones para compilar y ejecutar con make:
    make: compila todo y genera un ./main
    make valgrind: compila todo y ejecuta con valgrind
    make kill_server: (ALERTA: si tienes otro programa que se llame ./main no usar) para la ejecución del servidor
    make syslog: printea las últimas lineas del archivo syslog para ver el output del servidor

    si se desea parar la ejecución del servidor basta mandar SIGINT al proceso padre (o pulsar CTRL+C en la terminal)

los archivos deben ir en htmlfiles (o la carpeta que se haya configurado en el server.conf) y esta será la raiz para acceder
por ejemplo si hay un archivo htmlfiles/prueba.html, el archivo se deberá localizar en la raiz de la carpeta htmlfiles