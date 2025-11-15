import random

def comprueba_choque(serpiente: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], otra_serpiente: list[tuple[int, int]]) -> bool:
    '''
    Comprueba si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente. Tenga en cuenta
    que la serpiente avanza siempre por su cabeza, que está situada en la 
    primera posición de la lista.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de cada segmento de la serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    otra_serpiente: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.

    Devuelve:
    True si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente, False en caso contrario.
    '''    
    if serpiente[0] in serpiente[1:] or serpiente[0] in otra_serpiente:
        return True
    for i in paredes:
        if serpiente[0] in i:
            return True
    else: 
        return False

def ha_comido_serpiente(serpiente: list[tuple[int, int]], posicion_comida: tuple[int, int]) -> bool:
    '''
    Comprueba si la cabeza de la serpiente está en la misma posición que la comida.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    posicion_comida: Tupla representando la posición de la comida (columna, fila).

    Devuelve:
    True si la cabeza de la serpiente está en la misma posición que la comida, False en caso contrario.
    '''
    if serpiente[0] == posicion_comida:
        return True
    else:
        return False
    
def crece_serpiente(serpiente: list[tuple[int, int]]) -> None:
    '''
    Hace crecer la serpiente añadiendo duplicando la posición de la cola

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    '''
    serpiente.append(serpiente[-1])
    return serpiente

def genera_comida_aleatoria(serpiente_jugador: list[tuple[int, int]], serpiente_ia: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], filas: int, columnas: int) -> tuple[int, int]:
    '''
    Genera una posición aleatoria para la comida que no esté en la misma posición que las serpientes o las paredes.

    Parámetros:
    serpiente_jugador: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    serpiente_ia: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.

    Devuelve:
    Posición aleatoria para la comida (columna, fila).
    '''
    no_vale = True
    while no_vale:
        posicion = (random.randint(0, columnas - 1), random.randint(0, filas - 1)) 
        for i in paredes:
            if posicion not in serpiente_jugador and posicion not in i and posicion not in serpiente_ia:
                no_vale = False
    return posicion    

def mueve_serpiente(serpiente: list[tuple[int, int]], direccion: str, filas: int, columnas: int) -> None:
    '''
    Mueve la serpiente en el tablero según la dirección dada. El tablero es circular, lo que significa
    que si la serpiente se sale por la derecha, debe aparecer por la izquierda, y viceversa (y lo 
    mismo si se sale por arriba o por abajo).

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    direccion: Dirección en la que se debe mover la serpiente ('Left', 'Right', 'Down', 'Up').
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.
    '''
    if direccion not in ['Left', 'Right', 'Down', 'Up']:
        return 
    else:
        cabeza = serpiente[0]
        x = cabeza[0]
        y = cabeza[1] 
        serpiente.pop()
        if direccion == 'Up':
            tupla_cabeza_izq = (x, (y - 1) % filas )
            serpiente.insert(0, tupla_cabeza_izq)
        elif direccion == 'Down':
            tupla_cabeza_der = (x, (y + 1) % filas)
            serpiente.insert(0, tupla_cabeza_der)
        elif direccion == 'Left':
            tupla_cabeza_ab = ((x - 1) % columnas , y)
            serpiente.insert(0, tupla_cabeza_ab)
        elif direccion == 'Right':
            tupla_cabeza_ar = ((x + 1) % columnas, y)
            serpiente.insert(0, tupla_cabeza_ar)
    return serpiente

def decide_movimiento_ia(serpiente_rival: list[tuple[int, int]], serpiente_jugador: list[tuple[int, int]],
    paredes: list[list[tuple[int, int]]], posicion_comida: tuple[int, int],
    filas: int, columnas: int) -> str:
    '''
    Decide la dirección de movimiento de la serpiente rival, intentando elegir la que más 
    le acerque a la comida sin chocar.

    Parámetros:
    serpiente_rival: lista de posiciones (columna, fila) de la serpiente rival.
    serpiente_jugador: lista de posiciones de la serpiente del jugador.
    paredes: lista de listas de posiciones de las paredes.
    posicion_comida: posición actual de la comida.
    filas, columnas: tamaño del tablero.

    Devuelve:
    Dirección elegida: 'Left', 'Right', 'Up' o 'Down'.    
    '''
    # Construiremos una lista de (distancia_a_la_comida, direccion)
    opciones = []
    for d in ("Up", "Down", "Left", "Right"):
        # TODO: Haz una copia de la serpiente rival y muévela en la dirección d
        nueva_rival = serpiente_rival.copy()
        mueve_serpiente(serpiente_rival, d, filas, columnas)
        
        # TODO: Si la copia no se ha chocado
        if not comprueba_choque(nueva_rival, paredes):    
            # TODO: Calcula la distancia de la cabeza a la comida
            
            # Usa la distancia Manhattan: valor absoluto de la diferencia en x + valor absoluto de la diferencia de y
            pass
            # TODO: Añade a la lista opciones una tuplºa con la distancia y la dirección
        
    # TODO: Si no hay opciones válidas, devolvemos "Up" por defecto
    
    # TODO: Devolvemos la dirección que minimiza la distancia a la comida
    return "Up" 

