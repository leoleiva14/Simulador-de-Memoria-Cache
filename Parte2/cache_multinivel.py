from math import log2, floor

# Definición de la clase 'cache_multinivel' para simular un sistema de caché multinivel
class cache_multinivel:
    def __init__(self, capacidad_cache, associatividad, tamano_bloque, politica_reemplazo):
        """
        Inicializa una instancia de la clase cache_multinivel con los parámetros dados.

        Parámetros:
        capacidad_cache (int): Capacidad del caché en kilobytes.
        associatividad (int): Número de vías del caché (associativity).
        tamano_bloque (int): Tamaño de cada bloque en bytes.
        politica_reemplazo (str): Política de reemplazo de bloques ("l" para LRU).
        """
        # Inicialización de las estadísticas del caché
        self.total_access = 0
        self.total_misses = 0
        self.total_reads = 0
        self.total_read_misses = 0
        self.total_writes = 0
        self.total_write_misses = 0
        
        # Configuración del caché
        self.cache_capacity = int(capacidad_cache)
        self.cache_assoc = int(associatividad)
        self.block_size = int(tamano_bloque)
        self.repl_policy = politica_reemplazo
        
        # Cálculo del tamaño del desplazamiento en bytes
        self.byte_offset_size = log2(self.block_size)
        
        # Número de conjuntos en el caché
        self.num_sets = int((self.cache_capacity * 1024) / (self.block_size * self.cache_assoc))
        
        # Cálculo del tamaño del índice
        self.index_size = int(log2(self.num_sets))
        
        # Tablas de validez, etiquetas y reemplazo para cada conjunto y vía
        self.valid_table = [[False for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.tag_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.repl_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
    
    def print_info(self):
        """
        Imprime la configuración del caché.
        """
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.cache_capacity) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")
        print("\tPolítica de Reemplazo:\t\t\t" + str(self.repl_policy))
    
    def print_stats(self):
        """
        Imprime las estadísticas de la simulación del caché.
        """
        tasa_misses_total = (100.0 * self.total_misses) / self.total_access
        tasa_misses_total = "{:.3f}".format(tasa_misses_total)
      
        miss_rate = self.total_misses / self.total_access
        miss_rate = "{:.3f}".format(miss_rate)
        hit_rate = 1 - float(miss_rate)
        print(f"\tTotal de misses:\t\t{self.total_misses} ({tasa_misses_total}%)")
        print(f"\tHit rate:\t\t\t{hit_rate:.3f}")
        print(f"\tMiss rate:\t\t\t{miss_rate}")

    def access(self, tipo_acceso, direccion):
        """
        Simula un acceso al caché.

        Parámetros:
        tipo_acceso (str): Tipo de acceso ('r' para lectura, 'w' para escritura).
        direccion (int): Dirección de memoria a acceder.

        Retorna:
        bool: True si el acceso es un miss, False si es un hit.
        """
        byte_offset = int(direccion % (2 ** self.byte_offset_size))
        index = int(floor(direccion / (2 ** self.byte_offset_size)) % (2 ** self.index_size))
        tag = int(floor(direccion / (2 ** (self.byte_offset_size + self.index_size))))
        
        # Buscar la etiqueta en el conjunto
        via = self.find(index, tag)
        miss = False
        
        # Si no se encuentra, traer a caché y contabilizar un miss
        if via == -1:
            self.bring_to_cache(index, tag)
            self.total_misses += 1
            if tipo_acceso == "r":
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
            miss = True
        
        # Contabilizar el acceso
        self.total_access += 1
        if tipo_acceso == "r":
            self.total_reads += 1
        else:
            self.total_writes += 1
        
        return miss
    
    def find(self, index, tag):
        """
        Busca una etiqueta en un conjunto del caché.

        Parámetros:
        index (int): Índice del conjunto.
        tag (int): Etiqueta del bloque.

        Retorna:
        int: Vía donde se encuentra la etiqueta, o -1 si no se encuentra.
        """
        for via in range(self.cache_assoc):
            if self.valid_table[index][via] and (self.tag_table[index][via] == tag):
                return via
        return -1
    
    def bring_to_cache(self, index, tag):
        """
        Trae una nueva etiqueta al caché utilizando la política de reemplazo especificada.

        Parámetros:
        index (int): Índice del conjunto.
        tag (int): Etiqueta del bloque a traer.
        """
        via_libre = -1
        for via in range(self.cache_assoc):
            if not self.valid_table[index][via]:
                self.valid_table[index][via] = True
                self.tag_table[index][via] = tag
                self.repl_table[index][via] = self.cache_assoc - 1
                via_libre = via
                break
        
        if via_libre == -1 and self.repl_policy == "l":  # Política de reemplazo LRU
            via_lru = -1
            lru_value = 999999
            for via in range(self.cache_assoc):
                if self.repl_table[index][via] < lru_value:
                    lru_value = self.repl_table[index][via]
                    via_lru = via
            self.valid_table[index][via_lru] = True
            self.tag_table[index][via_lru] = tag
            self.repl_table[index][via_lru] = self.cache_assoc - 1
            via_libre = via_lru
            for via in range(self.cache_assoc):
                if via != via_libre:
                    self.repl_table[index][via] -= 1

