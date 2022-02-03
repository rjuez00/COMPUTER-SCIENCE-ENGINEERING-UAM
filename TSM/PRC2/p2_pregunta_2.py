# Tratamiento de Señales Visuales/Tratamiento de Señales Multimedia I @ EPS-UAM
# Practica 2: Extraccion, descripcion y correspondencia de caracteristicas locales
# Memoria: codigo de la pregunta XX

# AUTOR1: Fernández Freire, Luis
# AUTOR2: Juez Hernández, Rodrigo
# PAREJA/TURNO: 25/1461

from skimage.data import camera
import matplotlib.pyplot as plt
from p2_tarea1 import *
from p2_tarea2 import *
from p2_tarea3 import *
from p2_tests import *

imagen = 0
test_p2_tarea3(imgIdx = imagen, disptime=0,tipoDesc='hist',tipoCorr='minDist')
test_p2_tarea3(imgIdx = imagen, disptime=0,tipoDesc='mag-ori',tipoCorr='minDist')