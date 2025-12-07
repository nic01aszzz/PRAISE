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
- Crear funcion que termine timeline
"""
from statebuffer import IStateBuffer
from environments import SimulatedEnvironment
import random

class chessPiece:
    #Defino esto para poder usar en la conversión de [x,y] a una posición (a1 por ejemplo)
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8']

    mapeoCoordenadas = {
        col + fila: [i, j] for i, fila in enumerate('12345678') for j, col in enumerate('abcdefgh') 
    }

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

    def legal_moves(self, posInicio, tablero, en_passant_target=None):
        moves = []
        
        posActual = self.mapeoCoordenadas[posInicio]
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
                    destino_diagonal = self.letras[columna] + self.numeros[fila_frente]
                    if self.check_legal([columna, fila_frente], tablero):    
                        if tablero.get(destino_diagonal) is not None:
                            moves.append(destino_diagonal)
                        elif en_passant_target is not None and destino_diagonal == en_passant_target:
                            moves.append(destino_diagonal)
        return moves
    

class Queen(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, posInicio, tablero): 
        moves = []

        posActual = self.mapeoCoordenadas[posInicio]
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

        posActual = self.mapeoCoordenadas[posInicio]
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

        posActual = self.mapeoCoordenadas[posInicio]
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
        
        posActual = self.mapeoCoordenadas[posInicio]
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

        posActual = self.mapeoCoordenadas[posInicio]
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
        return moves


class chessEnv(SimulatedEnvironment):
   
    #Este diccionario es simplemente para ayudar despues con los movimientos, lo pongo como una variable
    #acá porque lo van a usar todos los tableros que se hagan. El punto es: a1: [0,0], a2: [0,1], etc.
    #Nota a futuro: esto devuelve fila,columna
    mapeoCoordenadas = {
        col + fila: [i, j] for i, fila in enumerate('12345678') for j, col in enumerate('abcdefgh') 
    }

    def __new__(cls):
        return super().__new__(cls)
    
    def add(self, agent_id: int) -> None:
        super(chessEnv, self).add(agent_id)
        random_number = random.randint(1,2)
        if random_number == 1:
            self._agents_colors[agent_id] = "white"
        else:
            self._agents_colors[agent_id] = "black"

    def remove(self, agent_id: int) -> None:
        super(chessEnv, self).remove(agent_id)
        self._agents_colors.pop(agent_id, None)
    
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
        self._agents = []
        self._agents_colors = {}
        self._game_info = {
            "move_counter" : 0,
            "fifty_move_clock": 0,
            "en_passant_target" : None,
        }

    #falta parte de enroque
    def FEN_board_loader(self, fen_string):
        fen_parts = fen_string.split()
        fen_rows = fen_parts[0].split("/")

        #en fen es al reves primero
        filas = ["8", "7", "6", "5", "4", "3", "2", "1"]
        columnas = ["a","b","c","d","e","f","g","h"]

        piece_classes = {
            'p': Pawn, 
            'n': Knight, 
            'b': Bishop, 
            'r': Rook, 
            'q': Queen, 
            'k': King
        }

        self._tablero = self.crearTablero()

        for i, row_string in enumerate(fen_rows):
            fila_actual = filas[i]
            col = 0
            
            for char in row_string:
                if char.isdigit():
                    # si es un número, saltamos esa cantidad de columnas vacías
                    col += int(char)
                else:
                    if char.isupper():
                        color = "white"
                    else: 
                        color = "black"
                    clase_pieza = piece_classes[char.lower()]

                    nueva_pieza = clase_pieza(color)
                    
                    coord = columnas[col] + fila_actual
                    self._tablero[coord] = nueva_pieza
                    
                    col += 1

        ep_target = fen_parts[3]
        if ep_target == '-':
            self._game_info["en_passant_target"] = None
        else:
            self._game_info["en_passant_target"] = ep_target

        self._game_info["fifty_move_clock"] = int(fen_parts[4])

        full_move_number = int(fen_parts[5])
        active_color = fen_parts[1]

        base_counter = (full_move_number - 1) * 2
        if active_color == 'b':
            base_counter += 1
        
        self._game_info["move_counter"] = base_counter


    def color_check(self, agent_id): 
        color = self._agents_colors.get(agent_id)
        return color

    #se fija si, dado un tablero, el rey esta en jaque 
    @staticmethod
    def check_check(color_rey, tablero):
        king_pos = None

        for pos, pieza in tablero.items():
            if pieza is not None:
                # Usamos type().__name__ para evitar imports circulares
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
    @staticmethod
    def safe_movement(origen, destino, color, tablero):
        copia_tablero = tablero.copy()

        pieza = copia_tablero[origen]
        copia_tablero[destino] = pieza
        copia_tablero[origen] = None

        if chessEnv.check_check(color, copia_tablero):
            return False 
        else:
            return True 
        
    @staticmethod
    def has_movements(color,tablero, en_passant_target=None):
        for pos_origen, pieza in tablero.items():
            if pieza is not None and pieza.color == color:
                if type(pieza).__name__ == "Pawn":
                    posibles = pieza.legal_moves(pos_origen, tablero, en_passant_target)
                else:
                    posibles = pieza.legal_moves(pos_origen, tablero)
                for pos_destino in posibles:
                    if chessEnv.safe_movement(pos_origen, pos_destino,color, tablero):
                        return True
        return False

    @staticmethod
    def check_mate(color, tablero, en_passant_target=None):
        if not chessEnv.check_check(color, tablero):
            return False
        if not chessEnv.has_movements(color, tablero, en_passant_target):
            return True
        else:
            return False
        
    @staticmethod
    def check_stalemate(color, tablero, en_passant_target=None):
        if chessEnv.check_check(color, tablero):
            return False
        if chessEnv.has_movements(color, tablero, en_passant_target):
            return False
        else:
            return True 

    #es medio el "arbitro" esta funcion
    def get_game_status(self):
        """
        El juego solo tiene 4 estados posibles:
        - En progreso (in_progress)
        - Ganaron blancas (white_won)
        - Ganaron negras (black_won)
        - Rey ahogado (stalemate)
        - Empate por 50 jugadas (draw_by_50_moves)
        """
        
        if self._game_info["fifty_move_clock"] >= 100:
            return "draw_by_50_moves"
        
        if self._game_info["move_counter"] % 2 == 0:
            turn = "white"  
        else:
            turn = "black" 
        
        ep_target = self._game_info["en_passant_target"]

        # Verificamos estados finales
        if chessEnv.check_mate(turn, self._tablero, ep_target):
            if turn == "white":
                return "black_won"
            else:
                return "white_won"            
        elif chessEnv.check_stalemate(turn, self._tablero, ep_target):
            return "stalemate"
        else:
            return "in_progress"
    
    def _handle_move(self, agent_id: int, origen, destino: str) -> None:
        #validamos que hayan entrado dos argumentos
        if not origen or not destino:
            print(f"Error: Invalid Movement {origen}->{destino}")
            return
        
        pieza = self._tablero.get(origen)
        agent_color = self._agents_colors.get(agent_id)
        flag_ep = False

        #validamos que haya una pieza que mover y que sea del mismo color que el agente
        if pieza is None:
            print("Error: there is no piece in that position to move!")
            return
        elif pieza.color != agent_color:
            print("Error: wrong color")
            #ver como devolver esto
            return
        else:
            pass

        #me fijo que sea un movimiento seguro, si lo es, muevo, aumento el contador de movimientos y veo lo del reloj
        if chessEnv.safe_movement(origen, destino, agent_color, self._tablero):
            #hago los preparativos para los checkeos
            pieza_destino = self._tablero[destino]

            #controlo en passant
            if type(pieza).__name__ == "Pawn" and pieza_destino is None:
                coord_origen = self._tableroCoordenadas[origen]
                coord_destino = self._tableroCoordenadas[destino]
                
                if coord_origen[1] != coord_destino[1]:
                    flag_ep = True
                    self._tablero[destino[0] + origen[1]] = None

            self._game_info["move_counter"] += 1
            self._game_info["en_passant_target"] = None
            
            #hago el movimiento
            self.make_mov(origen, destino)

            #controlo el en_passant_target
            if (type(pieza).__name__ == "Pawn"):
                coord_origen = self._tableroCoordenadas[origen]
                coord_destino = self._tableroCoordenadas[destino]
                
                fila_orig = coord_origen[0]
                fila_dest = coord_destino[0]

                if (abs(fila_dest - fila_orig)) == 2:
                    self._game_info["en_passant_target"] = chessPiece.letras[coord_origen[1]] + chessPiece.numeros[(fila_orig + fila_dest) // 2]

            #controlo el fifty_move_clock
            if (type(pieza).__name__ == "Pawn") or (pieza_destino is not None) or (flag_ep):
                self._game_info["fifty_move_clock"] = 0
            else:
                self._game_info["fifty_move_clock"] += 1
            
            status = self.get_game_status()
            if status != "in_progress":
                #ver que hacer
                print(f"Game ended! Final status: {status}!")
        else:
            print(f"Invalid movement: {origen} to {destino}")


    def make_mov(self, origen, destino):
            pieza = self._tablero[origen]
            self._tablero[destino] = pieza
            self._tablero[origen] = None

    def get_property(self, agent_id: int, property_name: str) -> dict:
        if agent_id in self._agents:
            response = {"agent": agent_id}
            #en caso de tener más métodos, ponerlos aca
            property_methods = {
                "tablero": lambda x: self._tablero,                    
                "color": self.color_check,                         
                "game_state": lambda x: self.get_game_status(),        
                "en_passant": lambda x: self._game_info["en_passant_target"],
            }

            property_method = property_methods.get(property_name)

            if property_method:
                response[property_name] = property_method(agent_id) #el (agent_id) es para ejecutar el self._tablero
            else:
                print(f"Invalid property: {property_name}")

            return response
    
    def take_action(self, agent_id: int, action_name: str, params: dict = {}) -> None:
        if agent_id in self._agents:
            action_methods = {
                "move": (self._handle_move, ["origen", "destino"])
            }

            action_method, expected_params = action_methods.get(action_name, (None, None))
            if action_method:
                args = [agent_id] + [params.get(param) for param in expected_params]
                action_method(*args)
                self._update_statebuffers(agent_id)
            else:
                print(f"Invalid action: {action_name}")

    def add_statebuffer(self, agent_id: int, statebuffer: IStateBuffer) -> None:
        super(chessEnv, self).add_statebuffer(agent_id, statebuffer)
        self._update_statebuffers(agent_id)

    def remove_statebuffer(self, agent_id: int,statebuffer: IStateBuffer) -> None:
        super(chessEnv, self).remove_statebuffer(agent_id, statebuffer)

    def _update_statebuffers(self, agent_id: int):
        relevant_statebuffers = [entry["statebuffer"] for entry in self._statebuffers if entry["agent_id"] == agent_id]
        
        if self._game_info["move_counter"] % 2 == 0:
            turn_color = "white"
        else:
            turn_color = "black"

        for statebuffer in relevant_statebuffers:
            datos_juego = {
                "tablero": self._tablero.copy(), 
                "game_info": self._game_info.copy(),
                "status": self.get_game_status(),
                "turn_color": turn_color,
            }
            
            statebuffer.update(datos_juego)