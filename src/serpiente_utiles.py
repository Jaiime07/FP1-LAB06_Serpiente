import random

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
    
def comprueba_choque(serpiente: list[tuple[int, int]], paredes: list[list[tuple[int, int]]]) -> bool:
    '''
    Comprueba si la serpiente se ha chocado consigo misma o con las paredes. Tenga en cuenta
    que la serpiente avanza siempre por su cabeza, que está situada en la 
    primera posición de la lista.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de cada segmento de la serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.

    Devuelve:
    True si la serpiente se ha chocado consigo misma o con las paredes, False en caso contrario.
    '''
    if serpiente[0] in serpiente[1:]:
        return True
    for i in paredes:
        if serpiente[0] in i:
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


from collections import namedtuple

def genera_comida_aleatoria(serpiente: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], filas: int, columnas: int) -> tuple[int, int]:
    '''
    Genera una posición aleatoria para la comida que no esté en la misma posición que la serpiente o las paredes.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
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
            if posicion not in serpiente and posicion not in i:
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
