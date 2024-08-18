import random  # Importamos random para usarlo en la política de reemplazo aleatorio

# Definimos la clase policies para gestionar las políticas de la caché
class policies:

    # Constructor de la clase
    def __init__(self, size_cache, asociatividad, size_bloque, politica):
        # Inicializamos los parámetros de la caché
        self.size_cache = size_cache * 1024  # Tamaño de la caché en KB
        self.asociatividad = asociatividad  # Grado de asociatividad de la caché
        self.size_bloque = size_bloque  # Tamaño de cada bloque en bytes
        self.sets = int(self.size_cache / (size_bloque * asociatividad))  # Número de conjuntos en la caché
        self.politica = politica  # Política de reemplazo (LRU o aleatoria)
        
        # Calculamos los bits necesarios para el índice y el offset
        self.index_bits = (self.sets - 1).bit_length()  # Bits para el índice
        self.offset_bits = (size_bloque - 1).bit_length()  # Bits para el offset
        
        # Inicializamos la matriz de recency para la política LRU
        self.recency = []
        for _ in range(self.sets):
            sets = [0] * self.asociatividad  # Cada conjunto tiene 'asociatividad' vías
            self.recency.append(sets)
        
        # Inicializamos la matriz de tags para almacenar las etiquetas de los bloques
        self.tags = []
        for _ in range(self.sets):
            sets = [None] * self.asociatividad  # Cada conjunto tiene 'asociatividad' vías
            self.tags.append(sets)
        
        # Inicializamos contadores para las estadísticas
        self.accesos = 0  # Total de accesos a la caché
        self.misses_read = 0  # Fallos en lectura
        self.accesos_read = 0  # Total de accesos de lectura
        self.misses_write = 0  # Fallos en escritura
        self.accesos_write = 0  # Total de accesos de escritura
    
    # Método para imprimir la información de la caché
    def print_info(self):
        politica_desc = "LRU" if self.politica == 'l' else "Aleatoria"
        print(f"Política: {politica_desc}")
        print(f"\tTamaño de cache : {self.size_cache / 1024} kB")
        print(f"\tAsociatividad : {self.asociatividad}")
        print(f"\tTamaño de bloque : {self.size_bloque} bytes")
    
    # Método para imprimir las estadísticas de la caché
    def print_stats(self):
        total_misses = self.misses_read + self.misses_write
        miss_rate_total = round((total_misses * 100) / self.accesos, 3)
        miss_rate_lectura = round((self.misses_read * 100) / self.accesos_read, 3)
        miss_rate_escritura = round((self.misses_write * 100) / self.accesos_write, 3)
        
        print("Resultados de la simulación")
        print(f"\t# Cantidad total de misses: {total_misses}")
        print(f"\t# Miss rate total: {miss_rate_total}%")
        print(f"\t# Cantidad de misses de lectura: {self.misses_read}")
        print(f"\t# Miss rate en lectura: {miss_rate_lectura}%")
        print(f"\t# Cantidad de misses de escritura: {self.misses_write}")
        print(f"\t# Miss rate en escritura: {miss_rate_escritura}%")
        print(f"Total accesos: {self.accesos}")
    
    # Método para manejar el reemplazo de bloques en la caché
    def replace(self, tipo, PC):
        hit = False
        PC = PC >> self.offset_bits  # Eliminamos los bits de offset
        index = PC % (2 ** self.index_bits)  # Calculamos el índice del conjunto
        tag = PC >> self.index_bits  # Calculamos la etiqueta del bloque
        
        # Actualizamos la recency de todas las vías en el conjunto
        for via in range(self.asociatividad):
            self.recency[index][via] += 1
        
        # Revisamos si el bloque está en la caché
        for etiqueta in self.tags[index]:
            if tag == etiqueta:
                hit = True
                way = self.tags[index].index(etiqueta)  # Encontramos la vía correspondiente al hit
        
        # Si hubo un miss
        if not hit:
            if self.politica == "l":
                lru = -1
                for vejez in self.recency[index]:
                    if vejez > lru:
                        lru = vejez
                        way = self.recency[index].index(vejez)  # Encontramos la vía más antigua
            elif self.politica == 'r':
                way = random.randint(0, self.asociatividad - 1)  # Elegimos una vía aleatoriamente
            
            # Actualizamos la etiqueta del bloque en la caché
            self.tags[index][way] = tag
        
        # Actualizamos la recency de la vía elegida
        self.recency[index][way] = 0
        
        # Actualizamos los contadores de accesos y fallos
        self.accesos += 1
        if tipo == 'w':
            self.accesos_write += 1
            if not hit:
                self.misses_write += 1
        else:
            self.accesos_read += 1
            if not hit:
                self.misses_read += 1

                        
            
   
    