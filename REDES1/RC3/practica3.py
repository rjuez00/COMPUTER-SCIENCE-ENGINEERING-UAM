#!/usr/bin/python
'''
    practica3.py
    Programa principal que realiza el análisis de tráfico sobre una traza PCAP.
    Autor: Javier Ramos <javier.ramos@uam.es>
    2020 EPS-UAM
'''


import sys
import argparse
from argparse import RawTextHelpFormatter
import time
import logging
import shlex
import subprocess
import pandas as pd
from io import StringIO
import os
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

'''
    Función: calcularECDF
    Entrada: 
        -datos: lista con los datos sobre los que calcular la ECDF
    Salida: :
        -datos: lista con los valores x (datos de entrada)
        -y: lista con los valores de probabilidad acumulada para cada dato de entrada
    Descripción:  Esta función recibe una lista de datos y calcula la función empírica de distribución 
    acumulada sobre los mismos. Los datos se devuelven listos para ser pintados.
'''
def calcularECDF(datos):
    datos.sort()
    n = len (datos)
    y = [(i-1)/n for i in range(1,n+1)]

    return datos,y



'''
    Función: ejecutarComandoObtenerSalida
    Entrada: 
        -comando: cadena de caracteres con el comando a ejecutar
    Salida: 
        -codigo_retorno: código numérico que indica el retorno del comando ejecutado.
        Si este valor es 0, entonces el comando ha ejecutado correctamente.
        -salida_retorno: cadena de caracteres con el retorno del comando. Este retorno
        es el mismo que obtendríamos por stdout al ejecutar un comando de terminal.

    Descripción: Esta función recibe una cadena con un comando a ejecutar, lo ejecuta y retorna
    tanto el código de resultado de la ejecución como la salida que el comando produzca por stdout
'''
def ejecutarComandoObtenerSalida(comando):
 
    return subprocess.getoutput(comando)


'''
    Función: pintarECDF
    Entrada:
        -datos: lista con los datos que se usarán para calcular y pintar la ECDF
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        -titulo_x: cadena de caracteres con la etiqueta a usar para el eje X de la gráfica
        -titulo_y: cadena de caracteres con la etiqueta a usar para el eje Y de la gráfica
    Salida: 
        -Nada

    Descripción: Esta función pinta una gráfica ECDF para unos datos de entrada y la guarda en una imagen
'''
def pintarECDF(datos,nombre_fichero,titulo,titulo_x,titulo_y):
    
    x, y = calcularECDF(datos)
    x.append(x[-1])
    y.append(1) 
    fig1, ax1 = plt.subplots()
    plt.step(x, y, '-')
    _ = plt.xticks(rotation=45)
    plt.title(titulo)
    fig1.set_size_inches(12, 10)
    plt.tight_layout()
    plt.locator_params(nbins=20)
    ax1.set_xlabel(titulo_x)
    ax1.set_ylabel(titulo_y)
    plt.savefig(nombre_fichero, bbox_inches='tight')


'''
    Función: pintarSerieTemporal
    Entrada:
        -x: lista de tiempos en formato epoch y granularidad segundos
        -y: lista con los valores a graficar
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        -titulo_x: cadena de caracteres con la etiqueta a usar para el eje X de la gráfica
        -titulo_y: cadena de caracteres con la etiqueta a usar para el eje Y de la gráfica
    Salida: 
        -Nada

    Descripción: Esta función pinta una serie temporal dados unos datos x e y de entrada y la guarda en una imagen
'''
def pintarSerieTemporal(x,y,nombre_fichero,titulo,titulo_x,titulo_y):
   
    fig1, ax1 = plt.subplots()
    plt.plot(x, y, '-')
    _ = plt.xticks(rotation=45)
    plt.title(titulo)
    fig1.set_size_inches(12, 10)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_locator(mtick.FixedLocator(x))
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda pos,_: time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(pos))))
    plt.tight_layout()
    plt.locator_params(nbins=20)
    ax1.set_xlabel(titulo_x)
    ax1.set_ylabel(titulo_y)
    plt.savefig(nombre_fichero, bbox_inches='tight')


'''
    Función: pintarTarta
    Entrada:
        -etiquetas: lista con cadenas de caracteres que contienen las etiquetas a usar en el gráfico de tarta
        -valores: lista con los valores a graficar
        -nombre_fichero: cadena de caracteres con el nombre del fichero donde se guardará la imagen
        (por ejemplo figura.png)
        -titulo: cadena de caracteres con el título a pintar en la gráfica
        
    Salida: 
        -Nada

    Descripción: Esta función pinta un gráfico de tarta dadas unas etiquetas y valores de entrada y lo guarda en una imagen
'''
def pintarTarta(etiquetas, valores, nombre_fichero,titulo):
  
    explode = tuple([0.05]*(len(etiquetas)))
 
    fig1, ax1 = plt.subplots()
    plt.pie(valores, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    plt.legend(etiquetas, loc="best")
    plt.title(titulo)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig1 = plt.gcf()
    fig1.gca().add_artist(centre_circle)
    fig1.set_size_inches(12, 10)
    ax1.axis('equal')  
    plt.tight_layout()
    plt.savefig(nombre_fichero, bbox_inches='tight')


'''
    Función: parse_command_two_columns
    Entrada:
        -command: comando que devuelve dos columnas parseables
        
        
    Salida: 
        -array con tuplas de dos elementos

    Descripción: parsea y devuelve array con dos elementos por celda
'''
def command_two_columns_and_tarta(command, file, titulo):
    table = [ (str(i.split(" ")[0]), i.split(" ")[1])  for i in ejecutarComandoObtenerSalida(command).split("\n") ]
    etiquetas = []
    valores = []
    for ip, by in table:
        etiquetas.append(ip)
        valores.append(by)
    pintarTarta(etiquetas,valores,file,titulo)


def serie_temporal_bits(filename, titulo, tituloejex, titulosejey, origen, initialepoch):
    ejecutarComandoObtenerSalida("tshark -r " + args.tracefile + " -Y 'eth."+origen+" eq "+args.mac+"' -w tempfile.pcap -F pcap")
    seconds = []
    bits = []
    for i in ejecutarComandoObtenerSalida("tshark -r tempfile.pcap -qz io,stat,1 | tail -n 131 | head -n 130 | awk '{ print $2 \" \" $6*8 }'").split("\n"):
        fields = i.split(" ")
        seconds.append(int(fields[0])+initialepoch)
        bits.append(int(fields[1]))
    pintarSerieTemporal(seconds, bits, "resultados/"+filename, titulo, tituloejex, titulosejey)
    ejecutarComandoObtenerSalida("rm -rf tempfile.pcap")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Programa principal que realiza el análisis de tráfico sobre una traza PCAP',
    formatter_class=RawTextHelpFormatter)
    parser.add_argument('--trace', dest='tracefile', default=False,help='Fichero de traza a usar',required=True)
    parser.add_argument('--mac', dest='mac', default=False,help='MAC usada para filtrar',required=True)
    parser.add_argument('--ip_flujo_tcp', dest='ip_flujo_tcp', default=False,help='IP para filtrar por el flujo TCP',required=True)
    parser.add_argument('--port_flujo_udp', dest='port_flujo_udp', default=False,help='Puerto para filtrar por el flujo UDP',required=True)
    parser.add_argument('--debug', dest='debug', default=False, action='store_true',help='Activar Debug messages')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s %(levelname)s]\t%(message)s')
    else:
        logging.basicConfig(level = logging.INFO, format = '[%(asctime)s %(levelname)s]\t%(message)s')

    #Creamos un directorio a donde volcaremos los resultado e imágenes
    if not os.path.isdir('resultados'):
        os.mkdir('resultados')
    
    
    #TODO: Añadir código para obtener el porcentaje de tráfico IPv4 y NO-IPv4
    logging.info('Ejecutando tshark para obtener el número de paquetes IP')
    paquetesIP = int(ejecutarComandoObtenerSalida("tshark -r {} -Y 'ip' -T fields -e eth.type | wc -l".format(args.tracefile)))
    total = int(ejecutarComandoObtenerSalida("tshark -r {} -T fields -e eth.type | wc -l".format(args.tracefile)))
    paquetesnoIP = total - paquetesIP

    
    porcentajeIP = paquetesIP/total*100
    porcentajenoIP = 100-porcentajeIP
    print('IP: ', porcentajeIP, 'noIP: ', porcentajenoIP)

    
    #TODO: Añadir código para obtener el porcentaje de tráfico TPC,UDP y OTROS sobre el tráfico IP
    porcentajeUPD = int(ejecutarComandoObtenerSalida("tshark -r {} -Y 'ip  && (ip.proto eq UDP)' -T fields -e eth.type | wc -l".format(args.tracefile)))/paquetesIP * 100
    porcentajeTCP = int(ejecutarComandoObtenerSalida("tshark -r {} -Y 'ip  && (ip.proto eq TCP)' -T fields -e eth.type | wc -l".format(args.tracefile)))/paquetesIP * 100 
    porcentajeOtros = -(porcentajeTCP + porcentajeUPD -100)
    
    print("\nDesglose IP: ")
    print('UDP:', porcentajeUPD, 'TCP:', porcentajeTCP, 'Otros:', porcentajeOtros)

    
    #Obtención de top direcciones IP
    print("Obtención de top direcciones IP")
    #TODO: Añadir código para obtener los datos y generar la gráfica de top IP origen por bytes  
    command = "tshark -r " + args.tracefile + " -T fields -e ip.src -e frame.len -Y 'ip' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command, "resultados/ipsrc_Bytes","Top 5 IPs Origen por Bytes")
    
    #TODO: Añadir código para obtener los datos y generar la gráfica de top IP origen por paquetes 
    command = "tshark -r "+args.tracefile+" -T fields -e ip.src -Y 'ip' | awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command,"resultados/ipscr_Packages","Top 5 IPs Origen por Paquetes")

    #TODO: Añadir código para obtener los datos y generar la gráfica de top IP destino por paquetes
    command = "tshark -r " + args.tracefile + " -T fields -e ip.dst -e frame.len -Y 'ip' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command, "resultados/ipdst_Bytes","Top 5 IPs Destino por Bytes")

    #TODO: Añadir código para obtener los datos y generar la gráfica de top IP destino por bytes
    command = "tshark -r " + args.tracefile + " -T fields -e ip.dst  -Y 'ip' | awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command, "resultados/ipdst_Packages","Top 5 IPs Destino por Paquetes")
     

    #Obtención de top puertos TCP
    print("Obtención de top puertos TCP")
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen TCP por bytes
    command = "tshark -r " + args.tracefile + " -T fields -e tcp.srcport -e frame.len -Y '(ip) && (ip.proto eq TCP)' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command,"resultados/tcpsrc_Bytes","Top 5 TCPs Origen por Bytes")

    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen TCP por paquetes
    command = "tshark -r "+args.tracefile+" -T fields -e tcp.srcport -e frame.len  -Y '(ip) && (ip.proto eq TCP)' | awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command,"resultados/tcpscr_Packages","Top 5 TCPs Origen por Paquetes")
    
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino TCP por bytes
    command = "tshark -r " + args.tracefile + " -T fields -e tcp.dstport -e frame.len -Y '(ip) && (ip.proto eq TCP)' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command,"resultados/tcpdst_Bytes","Top 5 TCPs Destino por Bytes")
 
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino  TCP por paquetes
    command = "tshark -r " + args.tracefile + " -T fields -e tcp.dstport -e frame.len  -Y '(ip) && (ip.proto eq TCP)'| awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command,"resultados/tcpdst_Packages","Top 5 TCPs Destino por Paquetes")
    
    #Obtención de top puertos UDP
    print("Obtención de top puertos UDP")
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen UDP por bytes
    command = "tshark -r " + args.tracefile + " -T fields -e udp.srcport -e frame.len -Y '(ip) && (ip.proto eq UDP)' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command,"resultados/udpsrc_Bytes","Top 5 UDPs Origen por Bytes")

    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto origen UDP por paquetes
    command = "tshark -r " + args.tracefile + " -T fields -e udp.srcport -e frame.len  -Y '(ip) && (ip.proto eq UDP)' | awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command,"resultados/udpscr_Packages","Top 5 UDPs Origen por Paquetes")
  
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino UDP por bytes
    command = "tshark -r " + args.tracefile + " -T fields -e udp.dstport -e frame.len -Y '(ip) && (ip.proto eq UDP)' | awk '{ if($2 != \"\") { colone[$1]+=$2; } } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nrk2 | head -n 5"
    command_two_columns_and_tarta(command,"resultados/udpdst_Bytes","Top 5 UDPs Destino por Bytes")
    
    #TODO: Añadir código para obtener los datos y generar la gráfica de top puerto destino UDP por paquetes
    command = "tshark -r " + args.tracefile + " -T fields -e udp.dstport -e frame.len  -Y '(ip) && (ip.proto eq UDP)' | awk '{ colone[$1]+=1; } END { for (i in colone) { print i \" \" colone[i]; } }' | sort -nk2 -r | head -n5"
    command_two_columns_and_tarta(command,"resultados/udpdst_Packages","Top 5 UDPs Destino por Paquetes")

    
    #Obtención de series temporales de ancho de banda
    print("Obtención de series temporales de ancho de banda")
    initialepoch = float(ejecutarComandoObtenerSalida("tshark -r traza.pcap -T fields -e frame.time_epoch | sort -n -r | tail -n 1"))
    #TODO: Añadir código para obtener los datos y generar la gráfica de la serie temporal de ancho de banda con MAC como origen
    ejecutarComandoObtenerSalida("rm -rf ethdst.pcap ethsrc.pcap")
    serie_temporal_bits("bitspersecsrc.png", "ancho de banda con eth origen", "segundos", "bits", "src", initialepoch)

    #TODO: Añadir código para obtener los datos y generar la gráfica de la serie temporal de ancho de banda con MAC como destino
    serie_temporal_bits("bitspersecdst.png", "ancho de banda con eth destino", "segundos", "bits", "dst", initialepoch)
    
    
    #Obtención de las ECDF de tamaño de los paquetes
    print("Obtención de las ECDF de tamaño de los paquetes")
    #TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tamaños de los paquetes a nivel 2
    pintarECDF( [ int(i) for i in ejecutarComandoObtenerSalida("tshark -Y 'eth.src == "+args.mac+"' -r traza.pcap -T fields -e frame.len").split("\n")],
                "resultados/ECDF_scr",
                "paquetes acumulados origen",
                "Tamaño paquetes (Bytes)",
                "P(X <= tamaño)")
    
    pintarECDF( [ int(i) for i in ejecutarComandoObtenerSalida("tshark -Y 'eth.dst == "+args.mac+"' -r traza.pcap -T fields -e frame.len").split("\n")],
                "resultados/ECDF_dst",
                "paquetes acumulados destino",
                "Tamaño paquetes (Bytes)",
                "P(X <= tamaño)")
    

    #Obtención de las ECDF de tamaño de los tiempos entre llegadas
    print("Obtención de las ECDF de tamaño de los tiempos entre llegadas")
    #TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tiempos entre llegadas para el flujo TCP
    pintarECDF( [ float(i) for i in ejecutarComandoObtenerSalida("tshark -Y '(ip.addr == "+args.ip_flujo_tcp+") && (ip.proto eq TCP)' -r traza.pcap -T fields -e frame.time_delta | awk '{ print $1*100 }'").split("\n")],
            "resultados/ECDF_TCP",
            "paquetes acumulados para flujo TCP con ip "+args.ip_flujo_tcp,
            "Tiempo llegada entre paquetes (ms)",
            "P(X <= tiempo (ms))")

    #TODO: Añadir código para obtener los datos y generar la gráfica de la ECDF de los tiempos entre llegadas para el flujo UDP
    pintarECDF( [ float(i) for i in ejecutarComandoObtenerSalida("tshark -Y '(udp.port == "+args.port_flujo_udp+") && (ip.proto eq UDP)' -r traza.pcap -T fields -e frame.time_delta | awk '{ print $1*100 }'").split("\n")],
            "resultados/ECDF_UDP",
            "paquetes acumulados para puerto UDP "+args.port_flujo_udp,
            "Tiempo llegada entre paquetes (ms)",
            "P(X <= tiempo (ms))")
    
    print("***** Script finalizado con exito *****")
    print("***** Las graficas estan en el directorio ./resultados *****")   
