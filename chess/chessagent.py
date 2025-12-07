from abc import ABCMeta, abstractmethod
import uuid
from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
from agents import Agent
import random
from chessworld import chessEnv


class BoardSensor(SimulatedSensor):
    #creo q ya esta
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="tablero")
        return response["tablero"]
    

class ColorSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="color")
        return response["color"]
    
class GameStateSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="game_state")
        return response["game_state"]

class EnPassantSensor(SimulatedSensor):
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="en_passant")
        return response["en_passant"]

#la unica accion que va a tener el agente es mover. No va a poder pedir ni aceptar tablas ni rendirse.
class MoverActuator(SimulatedActuator):
    def act(self, origen, destino):
        request_info = {"origen": origen, "destino": destino}
        self._env.take_action(self._agent.id, "move", request_info)


class ChessAgent(Agent):
    def function(self, percept):
        action = {}
        my_color = percept["color_sensor"]
        my_board = percept["board_sensor"] 
        #game_state = percept["game_state_sensor"]
        #ver como implementar lo de arriba
        target_ep = percept["en_passant_sensor"]
        valid_moves = [] 

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
            action["params"] = {"origen": move[0], "destino": move[1]}
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

    #creo q ya esta
    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)
        
        action_actuators = {
            "move": (self._actuators["mover"], ["origen", "destino"]),
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)

    #creo q ya esta
    def behave(self):
        percept = self._perceive()
        self._act(percept)

