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
    
    '''
    Genera una posición aleatoria para la comida que no esté en la misma posición que las serpientes o las paredes.
    '''
    
    # Usamos un bucle infinito que solo se romperá con un 'return'
    while True:
        # 1. Generamos una posición
        posicion = (random.randint(0, columnas - 1), random.randint(0, filas - 1)) 
        
        # 2. Asumimos que es válida
        posicion_valida = True
        
        # 3. Comprobamos todas las condiciones de invalidez
        
        # ¿Está en el jugador?
        if posicion in serpiente_jugador:
            posicion_valida = False
        
        # ¿Está en la IA? (Solo lo comprobamos si sigue siendo válida)
        elif posicion in serpiente_ia:
            posicion_valida = False
        
        # ¿Está en alguna pared? (Solo lo comprobamos si sigue siendo válida)
        else:
            for i in paredes:
                if posicion in i:
                    posicion_valida = False
                    break # Si está en una pared, no hace falta mirar las otras
        
        # 4. Si NUNCA se volvió falsa, es una posición buena. La devolvemos.
        if posicion_valida:
            return posicion
            
        # Si no, posicion_valida es False, el 'while True' se repite 
        # y probamos con una nueva posición.

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
    opciones = []
    for d in ("Up", "Down", "Left", "Right"):
        # TODO: Haz una copia de la serpiente rival y muévela en la dirección d
        nueva_rival = serpiente_rival.copy()
        mueve_serpiente(nueva_rival, d, filas, columnas)
        
        if not comprueba_choque(nueva_rival, paredes, serpiente_jugador):    
            # TODO: Calcula la distancia de la cabeza a la comida
            # Usa la distancia Manhattan: valor absoluto de la diferencia en x + valor absoluto de la diferencia de y
            cabeza = nueva_rival[0]
            manhattan = abs(cabeza[0] - posicion_comida[0]) + abs(cabeza[1] - posicion_comida[1])
            # TODO: Añade a la lista opciones una tupla con la distancia y la dirección
            opciones.append((manhattan, d))
    # TODO: Si no hay opciones válidas, devolvemos "Up" por defecto
    if opciones == []:    
        return 'Up'
    # TODO: Devolvemos la dirección que minimiza la distancia a la comida
    menor = opciones[0]
    for tupla in opciones:
        if tupla[0] < menor[0]:
            menor = tupla
    return menor[1]


        