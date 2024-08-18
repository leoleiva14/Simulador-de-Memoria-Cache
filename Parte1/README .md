# Tarea #4: Simulador de Caché 
Luis Aguero Peralta - C10089, Leonardo Leiva Vásquez - C14172, Juan Pablo Morales Vargas - B95322

## Descripción
Este proyecto consiste en un simulador de caché que permite la configuración de parámetros como el tamaño de la caché, la asociatividad, el tamaño del bloque y la política de reemplazo. El simulador procesa archivos de rastreo (`trace files`) para evaluar el rendimiento de la caché según los parámetros especificados.

## Argumentos de Línea de Comandos
El simulador acepta los siguientes argumentos de línea de comandos:

- `-s`: Tamaño de la caché en kilobytes. Debe ser un número entero y una potencia de 2.
- `-a`: Grado de asociatividad de la caché. Debe ser un número entero y una potencia de 2.
- `-b`: Tamaño del bloque en bytes. Debe ser un número entero y una potencia de 2.
- `-r`: Política de reemplazo:
  - `-r l`: Utiliza la política "LRU" (Least Recently Used).
  - `-r r`: Utiliza la política "Aleatoria".
- `-t`: Nombre del archivo de rastreo. Si no se especifica, se utiliza el archivo predeterminado.

## Ejemplos de Uso
A continuación se presentan ejemplos para ejecutar el simulador con diferentes archivos de rastreo y parámetros, según la Sección 2 del documento adjunto.

### Ejemplo 1
Para ejecutar el archivo de rastreo `400.perlbench-41B.trace.txt` con los parámetros especificados en la Sección 2 del documento adjunto:
```sh
python3 cache_test.py -s 128 -a 16 -b 64 -r l -t 400.perlbench-41B.trace.txt
```


### Ejemplo 2
Para correr el trace `401.bzip2-226B.trace.txt` con los argumentos de la sección 2 del documento adjunto:
```sh
 python3 cache_test.py -s 128 -a 16 -b 64 -r l -t 401.bzip2-226B.trace.txt
 ```
Y así con todos los ejemplos.
