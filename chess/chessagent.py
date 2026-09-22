from abc import ABCMeta, abstractmethod
import uuid
from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
from agents import Agent
import random
import time
from .chessworld import chessEnv
import queue

#sensor que le brinda al agente el tablero
class BoardSensor(SimulatedSensor):
    #creo q ya esta
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="tablero")
        return response["tablero"]
    
#sensor que le brinda al agente su color
class ColorSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="color")
        return response["color"]
    
#sensor que le brinda al agente información del juego (si termino, en passant, etc)
class GameStateSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="game_state")
        return response["game_state"]

class EnPassantSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="en_passant")
        return response["en_passant"]

class TurnSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="turn_color")
        return response["turn_color"]

class MoveCounterSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="move_counter")
        return response["move_counter"]

#la unica accion que va a tener el agente es mover. No va a poder pedir ni aceptar tablas ni rendirse.
class MoverActuator(SimulatedActuator):
    def act(self, origen, destino, move_counter):
        request_info = {"origen": origen, "destino": destino, "move_counter": move_counter}
        self._env.take_action(self._agent.id, "move", request_info)

class ChessAgent(Agent):
    #la funcion general del agente. en base a la informacion que percibe, toma los posibles movimientos y realiza uno
    #al azar
    def function(self, percept):
        action = {}
        my_color = percept["color_sensor"]
        my_board = percept["board_sensor"] 
        #game_state = percept["game_state_sensor"]
        #ver como implementar lo de arriba
        target_ep = percept["en_passant_sensor"]
        turn_color = percept["turn_sensor"]
        move_counter = percept["move_counter_sensor"]
        valid_moves = [] 

        #cambiar esto despues para cuando se implemente lógica mas compleja
        if my_color != turn_color:
            return action

        for pos_origen, pieza in my_board.items():
            if pieza is not None and pieza.color == my_color:
                if type(pieza).__name__ == "Pawn":
                    possible_moves = pieza.legal_moves(pos_origen, my_board, target_ep)
                else:
                    possible_moves = pieza.legal_moves(pos_origen, my_board)
                
                for pos_destino in possible_moves:
                    if chessEnv.safe_movement(pos_origen, pos_destino, my_color, my_board):
                        valid_moves.append((pos_origen, pos_destino))
                        
        if valid_moves:
            move = random.choice(valid_moves)
            action["name"] = "move"
            action["params"] = {"origen": move[0], "destino": move[1], "move_counter": move_counter}
        return action

    
    def __init__(self, env: SimulatedEnvironment):
        super().__init__()
        env.add(self.id)

        mover = MoverActuator(env)
        mover.agent = self
        self.add_actuator("mover", mover)

        board_sensor = BoardSensor(env)
        board_sensor.agent = self
        self.add_sensor("board_sensor", board_sensor)

        color_sensor = ColorSensor(env)
        color_sensor.agent = self
        self.add_sensor("color_sensor", color_sensor)

        game_state_sensor = GameStateSensor(env)
        game_state_sensor.agent = self
        self.add_sensor("game_state_sensor", game_state_sensor)

        en_passant_sensor = EnPassantSensor(env)
        en_passant_sensor.agent = self
        self.add_sensor("en_passant_sensor", en_passant_sensor)

        turn_sensor = TurnSensor(env)
        turn_sensor.agent = self
        self.add_sensor("turn_sensor", turn_sensor)

        move_counter_sensor = MoveCounterSensor(env)
        move_counter_sensor.agent = self
        self.add_sensor("move_counter_sensor", move_counter_sensor)

    #usa los sensores 
    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    #en base a lo que percibio, llama a function y le manda la informacion al entorno con su actuador
    def _act(self, percept):
        action = self.function(percept)
        
        #innecesario esto, pero no está de mas asegurarse que no esté vacio
        if not action:
            return
        
        action_actuators = {
            "move": (self._actuators["mover"], ["origen", "destino", "move_counter"]),
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)

    #ciclo de percibir y actuar
    def behave(self):
        time.sleep(0.5)
        percept = self._perceive()
        self._act(percept)

class ChessHuman(Agent):
    def __init__(self, env: SimulatedEnvironment, action_queue=None):
        super().__init__()
        self._env = env
        self.action_queue = action_queue

        env.add(self.id)

        mover = MoverActuator(env)
        mover.agent = self
        self.add_actuator("mover", mover)

        color_sensor = ColorSensor(env)
        color_sensor.agent = self
        self.add_sensor("color_sensor", color_sensor)

        turn_sensor = TurnSensor(env)
        turn_sensor.agent = self
        self.add_sensor("turn_sensor", turn_sensor)

        move_counter_sensor = MoveCounterSensor(env)
        move_counter_sensor.agent = self
        self.add_sensor("move_counter_sensor", move_counter_sensor)

    def _perceive(self):
        percept = {}
        for name, sensor in self._sensors.items():
            percept[name] = sensor.sense()
        return percept

    def function(self, percept):
        action = {}
        my_color = percept["color_sensor"]
        turn_color = percept["turn_sensor"]
        move_counter = percept["move_counter_sensor"]

        if my_color != turn_color:
            return action

        if self.action_queue: #UI
            try:
                origen, destino = self.action_queue.get_nowait() #devuelve false si esta vacia
            except queue.Empty:
                return action
        else: #consola
            origen = input("Origen: ").strip()
            if origen == "exit":
                action["name"] = "exit"
                return action
            destino = input("Destino: ").strip()

        action["name"] = "move"
        action["params"] = {
            "origen": origen,
            "destino": destino,
            "move_counter": move_counter
        }
        return action

    def _act(self, action):
        if not action:
            return True

        if action.get("name") == "exit":
            return False

        action_actuators = {
            "move": (self._actuators["mover"], ["origen", "destino", "move_counter"])
        }

        actuator, expected_params = action_actuators.get(action.get("name"), (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)
        return True

    def behave(self):
        percept = self._perceive()
        action = self.function(percept)
        return self._act(action)