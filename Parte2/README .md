# Tarea #4: Simulador de Caché 
Luis Aguero Peralta - C10089, Leonardo Leiva Vásquez - C14172, Juan Pablo Morales Vargas - B95322

# Simulación de Caché Multinivel

Este proyecto simula un sistema de caché multinivel. Permite analizar el rendimiento de configuraciones de caché de un solo nivel, dos niveles y tres niveles, calculando el Average Memory Access Time (AMAT) para diferentes trazas de memoria.

## Requisitos

- Python 3.x
- Biblioteca `gzip`
- Archivo `cache_multinivel.py` con la clase `cache_multinivel`

## Uso

### Configuración del Caché de Un Solo Nivel

Para ejecutar la simulación con un caché de un solo nivel (L1), sigue estos pasos:

1. **Configura los parámetros**:
   - `--l1_s`: Capacidad del caché L1 en kB.
   - `--l1_a`: Asociatividad del caché L1.
   - `-b`: Tamaño del bloque en bytes.
   - `-t`: Directorio que contiene las trazas de memoria comprimidas en formato `.gz`.

2. **Ejecuta el script**:

```bash
python3 sim_multinivel.py --l1_s 32 --l1_a 8 -b 64 -t traces

```

### Configuración del Caché de Dos Niveles

Para ejecutar la simulación con cachés de dos niveles (L1 y L2), sigue estos pasos:

1. **Configura los parámetros**:
   - `--l1_s`: Capacidad del caché L1 en kB.
   - `--l1_a`: Asociatividad del caché L1.
   - `--l2_s`: Capacidad del caché L2 en kB.
   - `--l2_a`: Asociatividad del caché L2.
   - `-b`: Tamaño del bloque en bytes.
   - `-t`: Directorio que contiene las trazas de memoria comprimidas en formato `.gz`.

2. **Ejecuta el script**:

Para ejecutar el script para diferentes configuraciones de L2, puedes hacerlo de la siguiente manera:

```bash
# Capacidad de L2: 64kB, Asociatividad de L2: 8-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 64 --l2_a 8 -b 64 -t traces

# Capacidad de L2: 64kB, Asociatividad de L2: 16-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 64 --l2_a 16 -b 64 -t traces

# Capacidad de L2: 128kB, Asociatividad de L2: 8-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 128 --l2_a 8 -b 64 -t traces

# Capacidad de L2: 128kB, Asociatividad de L2: 16-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 128 --l2_a 16 -b 64 -t traces
```
 
### Configuración del Caché de Tres Niveles

Para ejecutar la simulación con cachés de dos niveles (L1, L2 y L3), sigue estos pasos:

1. **Configura los parámetros**:
   - `--l1_s`: Capacidad del caché L1 en kB.
   - `--l1_a`: Asociatividad del caché L1.
   - `--l2_s`: Capacidad del caché L2 en kB.
   - `--l2_a`: Asociatividad del caché L2.
   - `-b`: Tamaño del bloque en bytes.
   - `-t`: Directorio que contiene las trazas de memoria comprimidas en formato `.gz`.

2. **Ejecuta el script**:

### Ejemplos de Ejecución

Para ejecutar el script para diferentes configuraciones de L3, puedes hacerlo de la siguiente manera:

```bash
# Capacidad de L3: 512kB, Asociatividad de L3: 16-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 256 --l2_a 8 --l3_s 512 --l3_a 16 -b 64 -t traces

# Capacidad de L3: 512kB, Asociatividad de L3: 32-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 256 --l2_a 8 --l3_s 512 --l3_a 32 -b 64 -t traces

# Capacidad de L3: 1024kB, Asociatividad de L3: 16-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 256 --l2_a 8 --l3_s 1024 --l3_a 16 -b 64 -t traces

# Capacidad de L3: 1024kB, Asociatividad de L3: 32-way
python3 sim_multinivel.py --l1_s 32 --l1_a 8 --l2_s 256 --l2_a 8 --l3_s 1024 --l3_a 32 -b 64 -t traces
```





