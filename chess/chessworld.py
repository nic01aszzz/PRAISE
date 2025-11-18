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

Futura implementación: que se vea en pantalla y que rote 180° en cada turno.

2. Creating New Environments
To simulate a new world (e.g., a GridWorld or Traffic Simulation), you must implement new classes on the server side:

Environment Class: Inherit from 
SimulatedEnvironment
. This class manages the simulation's core state.
State Buffer Class: You can create a new concrete 
IStateBuffer
 implementation if you need specific treatment of the relevant state dictionary from the Environment for the client's renderer.
Pyro Adapter: Create and register a new Pyro Adapter (e.g., 
GridWorldPyroAdapter
) on the server to expose your new environment and its state buffer factory to clients via Pyro4.
"""
from statebuffer import IStateBuffer
from environments import SimulatedEnvironment

class chessPiece:
    def __init__(self, color):
        self.color = color
        self.simbolo = None 

class Pawn(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Queen(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Rook(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class Knight(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass


class Bishop(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):  #
        pass

class King(chessPiece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self):
        pass
    def checkmate(self):
        if ...:
           return True # gg

class chessEnv(SimulatedEnvironment):
    #Este diccionario es simplemente para ayudar despues con los movimientos, lo pongo como una variable
    #acá porque lo van a usar todos los tableros que se hagan
    mapeoCoordenadas = {
        col + fila: [i, j] for i, fila in enumerate('12345678') for j, col in enumerate('abcdefgh') 
    }

    def __new__(cls):
        return super().__new__(cls)
    
    
    #Este diccionaro es el tablero que va a tener las piezas
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
        
    def crearYRellenarTablero(self):
        tablero = self.crearTablero()
        self.rellenarTablero(tablero)
        return tablero


    def __init__(self):
        super(chessEnv, self).__init__()
        self._tablero = self.crearYRellenarTablero()
        self._tablero = self.crearTablero()
        self._tableroCoordenadas = chessEnv.mapeoCoordenadas
        self.rellenarTablero()





"""
Posibles lógicas de movimiento
1. 
Cada pieza tiene una lista de los posibles movimientos dependiendo de su posición.
Se hace dicho movimiento.

2. 
Cada pieza tiene una lógica de movimiento (esta es la más complicada creo)
Se calculan los posibles movimientos en base a la posición y a la lógica de movimiento que tiene.

3. 
Se le pasa a la pieza su posición de inicio y su posición de fin deseada.
La pieza verifica cosas en base a la posición de fin deseada. 





pieces = [rook, knight, bishop, king, queen, bishop, knight, rook]

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