def crear_tablero_ajedrez():
    # Definimos las columnas (archivos) y filas (rangos)
    columnas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    filas = ['1', '2', '3', '4', '5', '6', '7', '8']
    
    tablero = {}
    
    # Generamos las claves combinando letras y números
    for fila in filas:
        for col in columnas:
            posicion = col + fila
            tablero[posicion] = None # Inicialmente vacía
            
    return tablero

# Crear el tablero
mi_tablero = crear_tablero_ajedrez()

# Ejemplo: Imprimir algunas posiciones para verificar
print(f"Total de casillas: {len(mi_tablero)}")
print(f"Valor en 'a1': {mi_tablero['a1']}")
print(f"Claves generadas (primeras 10): {list(mi_tablero.keys())[:10]}")