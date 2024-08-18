from optparse import OptionParser  # Importamos OptionParser para manejar argumentos de línea de comandos
import gzip  # Importamos gzip para leer archivos comprimidos
from politica import *  # Importamos todo desde el módulo policies (asumimos que contiene la lógica de la caché)

# Crear un objeto OptionParser para manejar los argumentos de línea de comandos
parser = OptionParser()

# Definir las opciones de línea de comandos
parser.add_option("-s", dest="tamano_cache")  # tamaño de la caché
parser.add_option("-a", dest="asociatividad")  # asociatividad de la caché
parser.add_option("-b", dest="tamano_bloque_bytes")  # tamaño del bloque en bytes
parser.add_option("-r", dest="politica_reemplazo")  # política de reemplazo de la caché
parser.add_option("-t", dest="TRACE_FILE", default="400.perlbench-41B.trace.txt")  # archivo de rastreo

# Parsear los argumentos de línea de comandos
(options, args) = parser.parse_args()

# Formatear el nombre del archivo de rastreo, agregando el directorio de traces y extensión .gz
options.TRACE_FILE = "./traces/{}.gz".format(options.TRACE_FILE)

# Crear una instancia de la caché utilizando los parámetros proporcionados
# Se asume que el módulo 'policies' tiene una clase o función que acepta estos parámetros
cache = policies(int(options.tamano_cache), int(options.asociatividad), int(options.tamano_bloque_bytes), options.politica_reemplazo)

# Imprimir información de la caché para verificación
cache.print_info()

# Comienza la lectura del archivo de rastreo comprimido
with gzip.open(options.TRACE_FILE, 'rt') as trace_fh:  # 'rt' abre el archivo en modo lectura de texto
    for line in trace_fh:
        # Eliminar cualquier carácter de nueva línea al final de cada línea
        line = line.rstrip()
        
        # Separar la línea en tipo (lectura o escritura) y la dirección del programa (PC)
        tipo, PC = line.split(" ")  # 'tipo' puede ser 'r' (lectura) o 'w' (escritura)
        
        # Convertir la dirección del programa (PC) de hexadecimal a entero
        PC = int(PC, base=16)
        
        # Llamar a la función de reemplazo de la caché con el tipo de operación y la dirección
        cache.replace(tipo, PC)

# Imprimir estadísticas de la caché después de procesar todo el archivo de rastreo
cache.print_stats()
