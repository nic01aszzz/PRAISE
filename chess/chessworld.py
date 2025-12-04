"""
Entorno: 
Totalmente observable: el agente puede ver todo el tablero.
Discreto: hay un número finito de acciones posibles para el agente. 
Estático?: mientras el agente piensa su jugada, el tablero no se mueve.
Estocástico: el movimiento del jugador aporta aleatoridad.


Se tiene un tablero (matriz 8x8) con una posición inicial predeterminada, con las casillas nombradas 
(nomenclatura estándar).
Hay piezas, cada una con su comportamiento específico. 
La idea es que el jugador juega contra el agente. 

TO-DO list:
- FEN
- On peassant
- Agregar contador de turnos para determinadas reglas 
- Crear funcion que termine timeline
"""
from statebuffer import IStateBuffer
from environments import SimulatedEnvironment

class chessPiece:
    #Defino esto para poder usar en la conversión de [x,y] a una posición (a1 por ejemplo)
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self, color):
        self.color = color

    def check_legal(self, posFinal, tablero):
        col = posFinal[0]
        fil = posFinal[1]
        #controlo que no se vaya de los límites del tablero
        if not (0 <= col <= 7 and 0 <= fil <= 7):
            return False
        
        destino = tablero.get(self.letras[col] + self.numeros[fil])
        #si no hay ninguna pieza/hay una pero es enemiga, devuelvo true. De lo contrario devuelvo false
        if destino is None:
            return True
        elif destino.color != self.color:
            return True
        else:
            return False


class Pawn(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, posInicio, tablero):
        moves = []
        
        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]

        #los peones blancos y negros tienen direcciones y filas de inicio distintas
        if self.color == 'white':
            direccion = 1    # hacia indices mayores
            fila_inicio = 1  # fila 2
        else:
            direccion = -1   # hacia indices menores
            fila_inicio = 6  # fila 7

        fila_frente = fila + direccion
        
        #no uso check_legal pq para adelante no puede comer, entonces no tiene sentido q devuelva true
        if 0 <= fila_frente <= 7:
            #movimiento para adelante
            #1 casilla
            if tablero.get(self.letras[col] + self.numeros[fila_frente]) is None:
                moves.append(self.letras[col] + self.numeros[fila_frente])

                #2 casillas
                #esta adentro de este otro if para que no se salten piezas sin querer
                if fila == fila_inicio:
                        nueva_pos = self.letras[col] + self.numeros[fila + (direccion * 2)]
                        if tablero.get(nueva_pos) is None:
                            moves.append(nueva_pos)

            cols_captura = [col - 1, col + 1] # izq y derecha

            for columna in cols_captura:
                #verifico que no me salga de los limites horizontales
                if 0 <= columna <= 7:
                    # ahora si uso check_legal porque es para comer otra pieza
                    if self.check_legal([columna, fila_frente], tablero):    
                        if tablero.get(self.letras[columna] + self.numeros[fila_frente]) is not None:
                            moves.append(self.letras[columna] + self.numeros[fila_frente])
        return moves
    #falta implementar on peassant


class Queen(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self,posInicio, tablero): 
        moves = []

        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]

        direcciones = [
        (1, 0), (-1, 0), (0, 1), (0, -1), #direcciones de la torre
        (1, 1), (1, -1), (-1, 1), (-1, -1) #direcciones del alfil
        ]

        for dir_fila, dir_col in direcciones:
            for i in range(1, 8):
                nueva_fila = fila + (dir_fila * i)
                nueva_col = col + (dir_col * i)
                if self.check_legal([nueva_col, nueva_fila], tablero):
                    moves.append(self.letras[nueva_col] + self.numeros[nueva_fila])
                    if tablero.get(self.letras[nueva_col] + self.numeros[nueva_fila]) is not None:
                        break
                else:
                    break
        return moves


class Rook(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    #consigo los movimientos legales para una torre a partir de su posición en el tablero
    def legal_moves(self, posInicio, tablero):  
        moves = []

        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]

        direcciones = [
            (1, 0),  # Arriba (aumenta fila)
            (-1, 0), # Abajo (disminuye fila)
            (0, 1),  # Derecha (aumenta columna)
            (0, -1)  # Izquierda (disminuye columna)
        ]

        for dir_fila, dir_col in direcciones:
            for i in range(1, 8):
                nueva_fila = fila + (dir_fila * i)
                nueva_col = col + (dir_col * i)
                if self.check_legal([nueva_col, nueva_fila], tablero):
                    moves.append(self.letras[nueva_col] + self.numeros[nueva_fila])
                    #como check_legal devuelve true si el espacio está vacio o hay una pieza enemiga,
                    #con esto me fijo si hay una pieza enemiga. En ese caso, detengo el movimiento en esa
                    #dirección
                    if tablero.get(self.letras[nueva_col] + self.numeros[nueva_fila]) is not None:
                        break
                else:
                    break
        return moves


class Knight(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, posInicio, tablero):  
        moves = []

        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]
        #(fila, columna)
        direcciones = [
            #una columna menos, dos filas más
            (2,-1),
            #una columna mas, dos filas mas
            (2, 1),
            #una columna menos, dos filas menos
            (-2, -1),
            #una columna mas, dos filas menos
            (-2, 1),
            #dos columnas menos, una fila mas
            (1, -2),
            #dos columnas menos, una fila menos
            (-1, -2),
            #dos columnas mas, una fila mas
            (1, 2),
            #dos columnas mas, una fila menos
            (-1, 2)
        ]

        for dir_fila, dir_col in direcciones:
                nueva_fila = fila + dir_fila
                nueva_col = col + dir_col
                if self.check_legal([nueva_col, nueva_fila], tablero):
                    moves.append(self.letras[nueva_col] + self.numeros[nueva_fila])
        return moves


class Bishop(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self,posInicio, tablero):  
        moves = []
        
        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]

        direcciones = [
            #diagonal superior derecha
            (1, 1),
            #diagonal superior izquierda 
            (1, -1),
            #diagonal inferior derecha
            (-1, 1), 
            #diagonal inferior izquierda
            (-1, -1)
        ]

        for dir_fila, dir_col in direcciones:
            for i in range(1, 8):
                nueva_fila = fila + (dir_fila * i)
                nueva_col = col + (dir_col * i)
                if self.check_legal([nueva_col, nueva_fila], tablero):
                    moves.append(self.letras[nueva_col] + self.numeros[nueva_fila])
                    if tablero.get(self.letras[nueva_col] + self.numeros[nueva_fila]) is not None:
                        break
                else:
                    break
        return moves


class King(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, posInicio, tablero):  
        moves = []

        posActual = chessEnv.mapeoCoordenadas[posInicio]
        fila = posActual[0]
        col = posActual[1]

        direcciones = [
            (1, 0),  # arriba (aumenta fila)
            (-1, 0), # abajo (disminuye fila)
            (0, 1),  # derecha (aumenta columna)
            (0, -1),  # izquierda (disminuye columna)
            (1, 1), #arriba a la derecha (aumenta fila y columna)
            (-1, 1), #abajo a la derecha (disminuye fila y aumenta columna)
            (1, -1), # arriba a la izquierda (aumenta fila y disminuye columna)
            (-1, -1) #abajo a la izquierda (disminuye fila y columna)
        ]

        for dir_fila, dir_col in direcciones:
                nueva_fila = fila + dir_fila
                nueva_col = col + dir_col 
                if self.check_legal([nueva_col, nueva_fila], tablero):
                    moves.append(self.letras[nueva_col] + self.numeros[nueva_fila])
                    if tablero.get(self.letras[nueva_col] + self.numeros[nueva_fila]) is not None:
                        break
                else:
                    break
        return moves
    
#La posición final está en:
#La misma letra: el número es +-1
#Letras adyacentes: número +-1 o el mismo 
    def checkmate(self):
        if ...:
           return True # gg


class chessEnv(SimulatedEnvironment):
   
    #Este diccionario es simplemente para ayudar despues con los movimientos, lo pongo como una variable
    #acá porque lo van a usar todos los tableros que se hagan. El punto es: a1: [0,0], a2: [0,1], etc.
    #Nota a futuro: esto devuelve fila,columna
    mapeoCoordenadas = {
        col + fila: [i, j] for i, fila in enumerate('12345678') for j, col in enumerate('abcdefgh') 
    }

    def __new__(cls):
        return super().__new__(cls)
    
    
    #Este diccionaro es el tablero que va a tener las piezas
    @staticmethod
    def crearTablero():
        columnas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        filas = ['1', '2', '3', '4', '5', '6', '7', '8']
        tablero = {}
        for fila in filas:
            for col in columnas:
                posicion = col + fila
                tablero[posicion] = None 
        return tablero
    

    #Esta función va a poner las piezas (que van a ser clases) en el tablero principal
    @staticmethod
    def rellenarTablero(tablero):
        tablero['a8'] = Rook('black')
        tablero['h8'] = Rook('black')
        tablero['b8'] = Knight('black')
        tablero['g8'] = Knight('black')
        tablero['c8'] = Bishop('black')
        tablero['f8'] = Bishop('black')
        tablero['d8'] = Queen('black')
        tablero['e8'] = King('black')
        tablero['a7'] = Pawn('black')
        tablero['h7'] = Pawn('black')
        tablero['b7'] = Pawn('black')
        tablero['g7'] = Pawn('black')
        tablero['c7'] = Pawn('black')
        tablero['f7'] = Pawn('black')
        tablero['d7'] = Pawn('black')
        tablero['e7'] = Pawn('black')
        
        tablero['a2'] = Pawn('white')
        tablero['h2'] = Pawn('white')
        tablero['b2'] = Pawn('white')
        tablero['g2'] = Pawn('white')
        tablero['c2'] = Pawn('white')
        tablero['f2'] = Pawn('white')
        tablero['d2'] = Pawn('white')
        tablero['e2'] = Pawn('white')
        tablero['a1'] = Rook('white')
        tablero['h1'] = Rook('white')
        tablero['b1'] = Knight('white')
        tablero['g1'] = Knight('white')
        tablero['c1'] = Bishop('white')
        tablero['f1'] = Bishop('white')
        tablero['d1'] = Queen('white')
        tablero['e1'] = King('white')
        return tablero
    
    def crearYRellenarTablero(self):
        tablero = self.crearTablero()
        self.rellenarTablero(tablero)
        return tablero


    def __init__(self):
        super(chessEnv, self).__init__()
        self._tablero = self.crearYRellenarTablero()
        self._tableroCoordenadas = chessEnv.mapeoCoordenadas

    def check_check(self, color_rey, tablero):
        king_pos = None
        for pos, pieza in tablero.items():
            if pieza is not None:
                if type(pieza).__name__ == "King" and pieza.color == color_rey:
                    king_pos = pos
                    break

        if color_rey == "white":
            enemy_color = "black" 
        else:
            enemy_color = "white"

        for pos, pieza in tablero.items():
            if pieza is not None and pieza.color == enemy_color:
                if king_pos in pieza.legal_moves(pos, tablero):
                    return True 
 
        return False

    #esta funcion sirve para ver si un movimiento no va a poner al rey en jaque. Implementa 123 de la timeline
    def safe_movement(self, pos_origen, pos_destino, color):
        copia_tablero = self._tablero.copy()
        pieza = copia_tablero[pos_origen]
        
        copia_tablero[pos_destino] = pieza
        copia_tablero[pos_origen] = None

        if self.check_check(color, copia_tablero):
            return False 
        else:
            return True

    def check_mate(self, color, tablero):
        #si no hay jaque, no hay mate
        if not self.check_check(color, tablero):
            return False

        #buscamos en todas las piezas del mismo color si hay alguna que evite el check, de lo contrario, es checkmate
        for pos_origen, pieza in tablero.items():
            if pieza is not None and pieza.color == color:
                movimientos = pieza.legal_moves(pos_origen, tablero)

                for pos_destino in movimientos:
                    tablero_simulado = tablero.copy()
                    tablero_simulado[pos_destino] = pieza
                    tablero_simulado[pos_origen] = None

                    if not self.check_check(color, tablero_simulado):
                        return False 
        return True

"""
Timeline:
1. Se quiere mover una pieza de A a B
2. Se simula dicho movimiento en una copia o versión temporal del tablero
3. Se controla si el rey propio esta en jaque
4. Si devuelve True (estoy en check), el movimiento es ILEGAL y se lo borra de legal moves
5. Si devuelve False, el movimiento es válido





    def _move_piece_to_square(self, piece, square):
        if square isFree:
            #Mover pieza
        else:
            #Mover pieza y eliminar la otra

    def __init__(self, length: int, random_dirt=False):
        super(VacuumEnvironment, self).__init__()
        self._length = length
        self._agents_locations = {}                     # maps agent id with its location
        self._dirt_locations = set()
        if random_dirt:
            self.random_dirt(length // 2)

    def add(self, agent_id: int) -> None:
        super(VacuumEnvironment, self).add(agent_id)
        self._agents_locations[agent_id] = 0

    def remove(self, agent_id: int) -> None:
        super(VacuumEnvironment, self).remove(agent_id)
        self._agents_locations.pop(agent_id, None)

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(VacuumEnvironment, self).add_statebuffer(agent_id, statebuffer)
        statebuffer.update({"length": self._length, "agent_location": self._location_of(agent_id),
                         "dirt_location": self._dirt_locations})

    def remove_statebuffer(self, agent_id: int,statebuffer: IStateBuffer) -> None:
        super(VacuumEnvironment, self).remove_statebuffer(agent_id, statebuffer)

    def random_dirt(self, number_dirty_locations):
        self._dirt_locations = self._dirt_locations.union(set(random.sample(range(self._length),
                                                                            k=number_dirty_locations)))

    def _is_dirty_in_location(self, x: int) -> bool:
        return x in self._dirt_locations

    def _location_of(self, agent_id: int) -> int:
        return self._agents_locations[agent_id] if agent_id in self._agents_locations else None

    def get_property(self, agent_id: int, property_name: str) -> dict:
        if agent_id in self._agents:
            response = {"agent": agent_id}

            property_methods = {
                "location": self._location_of,
                "dirty": lambda agent_id: self._is_dirty_in_location(self._location_of(agent_id)),
            }

            property_method = property_methods.get(property_name)

            if property_method:
                response[property_name] = property_method(agent_id)
            else:
                print(f"Invalid property: {property_name}")

            return response
        else:
            return {}

    def _handle_move(self, agent_id: int, direction: str) -> None:
        if direction == "left":
            self._move_agent_left(agent_id)
        elif direction == "right":
            self._move_agent_right(agent_id)
        else:
            print(f"Invalid direction: {direction}")

    def _move_agent_left(self, agent_id: int):
        self._agents_locations[agent_id] = max(self._agents_locations[agent_id] - 1, 0)

    def _move_agent_right(self, agent_id: int):
        self._agents_locations[agent_id] = min(self._agents_locations[agent_id] + 1, self._length - 1)

    def _make_clean(self, agent_id: int):
        location = self._location_of(agent_id)
        self._dirt_locations.discard(location)

    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
        if agent_id in self._agents:
            action_methods = {
                "move": (self._handle_move, ["direction"]),
                "clean": (self._make_clean, []),
            }

            action_method, expected_params = action_methods.get(action_name, (None, None))
            if action_method:
                args = [agent_id] + [params.get(param) for param in expected_params]
                action_method(*args)
                self._update_statebuffers(agent_id)
            else:
                print(f"Invalid action: {action_name}")

    def _update_statebuffers(self, agent_id: int):
        relevant_statebuffers = [entry["statebuffer"] for entry in self._statebuffers if entry["agent_id"] == agent_id]
        for statebuffer in relevant_statebuffers:
            statebuffer.update({"length": self._length, "agent_location": self._location_of(agent_id),
                             "dirt_location": self._dirt_locations})
"""