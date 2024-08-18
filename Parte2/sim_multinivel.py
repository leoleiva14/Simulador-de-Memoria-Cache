from optparse import OptionParser
import gzip
import os
from cache_multinivel import *

def calculate_amat(total_access, total_misses, total_l2_misses, total_l2_access, total_l3_misses, total_l3_access, hit_time_l1, hit_time_l2, hit_time_l3, miss_penalty):
    """
    Calcula el AMAT (Average Memory Access Time) para un sistema de caché multinivel.

    Parámetros:
    total_access (int): Número total de accesos al caché L1.
    total_misses (int): Número total de fallos en el caché L1.
    total_l2_misses (int): Número total de fallos en el caché L2.
    total_l2_access (int): Número total de accesos al caché L2.
    total_l3_misses (int): Número total de fallos en el caché L3.
    total_l3_access (int): Número total de accesos al caché L3.
    hit_time_l1 (int): Tiempo de acierto en L1.
    hit_time_l2 (int): Tiempo de acierto en L2.
    hit_time_l3 (int): Tiempo de acierto en L3.
    miss_penalty (int): Penalización por fallo.

    Retorna:
    float: El AMAT calculado.
    """
    miss_rate_l1 = total_misses / total_access
    miss_rate_l2 = total_l2_misses / total_l2_access if total_l2_access > 0 else 0
    miss_rate_l3 = total_l3_misses / total_l3_access if total_l3_access > 0 else 0
    amat = hit_time_l1 + (miss_rate_l1 * (hit_time_l2 + (miss_rate_l2 * (hit_time_l3 + (miss_rate_l3 * miss_penalty)))))
    return amat

# Configuración de los argumentos de línea de comandos
parser = OptionParser()
parser.add_option("--l1_s", dest="l1_s")
parser.add_option("--l1_a", dest="l1_a")
parser.add_option("--l2_s", dest="l2_s")
parser.add_option("--l2_a", dest="l2_a")
parser.add_option("--l3_s", dest="l3_s")
parser.add_option("--l3_a", dest="l3_a")
parser.add_option("-b", dest="block_size", default="64")
parser.add_option("-t", dest="TRACE_DIR")

(options, args) = parser.parse_args()

# Parámetros para cálculo de AMAT
hit_time_l1 = 4
hit_time_l2 = 12
hit_time_l3 = 60
miss_penalty = 500

# Procesamiento de todos los archivos .gz en la carpeta de trazas
trace_dir = options.TRACE_DIR
trace_files = [f for f in os.listdir(trace_dir) if f.endswith(".gz")]

print(f"Archivos de traza encontrados: {len(trace_files)}")

results = []

# Creación del caché L1
l1_cache = cache_multinivel(options.l1_s, options.l1_a, options.block_size, "l")

# Creación del caché L2
l2_cache = cache_multinivel(options.l2_s, options.l2_a, options.block_size, "l")

# Creación del caché L3
l3_cache = cache_multinivel(options.l3_s, options.l3_a, options.block_size, "l")

for trace_file in trace_files:
    print(f"Procesando archivo: {trace_file}")
    
    # Reiniciar estadísticas antes de cada traza
    l1_cache.total_access = 0
    l1_cache.total_misses = 0
    l1_cache.total_reads = 0
    l1_cache.total_read_misses = 0
    l1_cache.total_writes = 0
    l1_cache.total_write_misses = 0

    l2_cache.total_access = 0
    l2_cache.total_misses = 0
    l2_cache.total_reads = 0
    l2_cache.total_read_misses = 0
    l2_cache.total_writes = 0
    l2_cache.total_write_misses = 0

    l3_cache.total_access = 0
    l3_cache.total_misses = 0
    l3_cache.total_reads = 0
    l3_cache.total_read_misses = 0
    l3_cache.total_writes = 0
    l3_cache.total_write_misses = 0

    try:
        with gzip.open(os.path.join(trace_dir, trace_file), 'rt') as trace_fh:
            for line in trace_fh:
                line = line.rstrip()
                access_type, hex_str_address = line.split(" ")
                address = int(hex_str_address, 16)
                is_l1_miss = l1_cache.access(access_type, address)
                if is_l1_miss:
                    is_l2_miss = l2_cache.access(access_type, address)
                    if is_l2_miss:
                        l3_cache.access(access_type, address)
    except Exception as e:
        print(f"Error procesando el archivo {trace_file}: {e}")
        continue
    
    # Calcular el AMAT después de procesar el archivo de traza
    total_access = l1_cache.total_access
    total_misses = l1_cache.total_misses
    total_l2_misses = l2_cache.total_misses
    total_l2_access = l2_cache.total_access
    total_l3_misses = l3_cache.total_misses
    total_l3_access = l3_cache.total_access

    amat = calculate_amat(total_access, total_misses, total_l2_misses, total_l2_access, total_l3_misses, total_l3_access, hit_time_l1, hit_time_l2, hit_time_l3, miss_penalty)
    
    results.append((trace_file, amat))
    print(f"AMAT para {trace_file}: {amat:.3f} ciclos")

    # Imprimir estadísticas del caché L1, L2 y L3 para el archivo de traza procesado
    print("Estadísticas del caché L1:")
    l1_cache.print_stats()
    print("Estadísticas del caché L2:")
    l2_cache.print_stats()
    print("Estadísticas del caché L3:")
    l3_cache.print_stats()

# Imprimir resultados en formato de tabla
print("\nResultados de AMAT para cada archivo de traza:")
print(f"{'Archivo de Traza':<30} {'AMAT (ciclos)'}")
for trace_file, amat in results:
    print(f"{trace_file:<30} {amat:.3f}")

