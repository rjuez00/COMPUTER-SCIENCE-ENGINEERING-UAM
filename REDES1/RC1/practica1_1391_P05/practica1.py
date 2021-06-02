'''
    practica1.py

    Muestra el tiempo de llegada de los primeros n paquetes (se detiene al
    pulsar Ctrl+ C) a la interfaz especificada como argumento y los vuelca a
    traza nueva con 30 minutos de OFFSET en tiempo Unix Epoch. Tambien es
    posible leer una captura .pcap (ver ayuda al ejecutar el programa sin
    argumentos) en cuyo caso no se generara una neva traza

    Autores: Rodrigo Juez
             Angel Casanova
             
    2020 EPS-UAM
'''

from rc1_pcap import *
import sys
import binascii
import signal
import argparse
from argparse import RawTextHelpFormatter
import time
import logging

ETH_FRAME_MAX = 1514
PROMISC = 1
NO_PROMISC = 0
TO_MS = 10
num_paquete = 0
TIME_OFFSET = 30*60
LINKER = "DLT_EN10MB"

def signal_handler(nsignal,frame):
	logging.info('Control C pulsado')
	if handle:
		pcap_breakloop(handle)


def procesa_paquete(us,header,data):
	global num_paquete, pdumper, nbytes
	logging.info('Nuevo paquete de {} bytes capturado en el timestamp UNIX {}.{}'.format(header.len,header.ts.tv_sec,header.ts.tv_sec))
	num_paquete += 1
	string = ''.join('{:02x}'.format(x) for x in data)

	length = 0 # Da formato a la salida en HEX
	if len(string) < nbytes*2:
		length = len(string)
	else:
		length = nbytes*2

	result = ""
	for i in range(0, (length)//2):
		result = result + string[i*2]+string[i*2+1] + " "

	print(result.upper()+ "\n\n") # Imprime el paquete

	header.ts.tv_sec += TIME_OFFSET
	if dumperopen == True:
		pcap_dump(pdumper,header,data) # Guarda el paquete, en el nuevo .pcap

if __name__ == "__main__":
	global pdumper,args,handle, nbytes
	parser = argparse.ArgumentParser(description='Captura tráfico de una interfaz ( o lee de fichero) y muestra la longitud y timestamp de los 50 primeros paquetes',
	formatter_class=RawTextHelpFormatter)
	parser.add_argument('--file', dest='tracefile', default=False,help='Fichero pcap a abrir')
	parser.add_argument('--itf', dest='interface', default=False,help='Interfaz a abrir')
	parser.add_argument('--nbytes', dest='nbytes', type=int, default=14,help='Número de bytes a mostrar por paquete')
	parser.add_argument('--debug', dest='debug', default=False, action='store_true',help='Activar Debug messages')
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s %(levelname)s]\t%(message)s')
	else:
		logging.basicConfig(level = logging.INFO, format = '[%(asctime)s %(levelname)s]\t%(message)s')

	if args.tracefile is False and args.interface is False:
		logging.error('No se ha especificado interfaz ni fichero')
		parser.print_help()
		sys.exit(-1)

	signal.signal(signal.SIGINT, signal_handler)

	errbuf = bytearray()
	handle = None
	pdumper = None
	dumperpointer = None
	dumperopen = False
	nbytes = args.nbytes

	if args.tracefile:
		handle = pcap_open_offline(args.tracefile, errbuf)
	else: # Si capturamos una interfaz
		handle = pcap_open_live(args.interface, ETH_FRAME_MAX, NO_PROMISC, TO_MS, errbuf)
		dumperpointer = pcap_open_dead(DLT_EN10MB, int(ETH_FRAME_MAX))
		pdumper = pcap_dump_open(dumperpointer, "captura." + args.interface + "." + str(time.time()) + ".pcap")
		dumperopen = True


    # Procesa cada paquete de la traza individualmente en "procesa paquete"
	ret = pcap_loop(handle, -1, procesa_paquete, None) #-1 := no limit
	if ret == -1: # Controla los posibles errores generados
		logging.error('Error al capturar un paquete')
	elif ret == -2:
		logging.debug('pcap_breakloop() llamado')
	elif ret == 0:
		logging.debug('No mas paquetes o limite superado')
	logging.info('{} paquetes procesados'.format(num_paquete))

    # Liberamos recursos antes de terminar la ejecucion
	pcap_close(handle)
	if dumperopen == True:
		pcap_close(dumperpointer)
		pcap_dump_close(pdumper)
