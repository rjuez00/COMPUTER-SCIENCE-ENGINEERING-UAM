from Datos import Datos
import EstrategiaParticionado
import Clasificador




dataset=Datos('../ConjuntosDatos/german.data')
estrategia=EstrategiaParticionado.ValidacionCruzada(5)
clasificador=Clasificador.ClasificadorNaiveBayes()
errores=clasificador.validacion(estrategia,dataset,clasificador)