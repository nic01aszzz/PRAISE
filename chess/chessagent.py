from abc import ABCMeta, abstractmethod
import uuid
from environments import SimulatedSensor, SimulatedActuator, SimulatedEnvironment
from agents import Agent
from random import randrange

#el unico sensor que necesita el agente es el del tablero
class BoardSensor(SimulatedSensor):
    #creo q ya esta
    def sense(self):
        response = self._env.get_property(self._agent.id, property_name="tablero")
        return response["tablero"]


#la unica accion que va a tener el agente es mover. No va a poder pedir ni aceptar tablas ni rendirse.
class MoverActuator(SimulatedActuator):
    #completar
    def act(self, direction: MoveDirection = MoveDirection.RIGHT):
        request_info = {"direction": ("right" if direction is MoveDirection.RIGHT else "left")}
        self._env.take_action(self._agent.id, "move", request_info)


class ChessAgent(Agent):
    #completar
    def function(self, percept):
        action = {}
        if percept["board_sensor"]:
            action["name"] = "clean"
        return action

    #creo q ya esta
    def __init__(self, env: SimulatedEnvironment):
        super().__init__()
        env.add(self.id)

        mover = MoverActuator(env)
        mover.agent = self
        self.add_actuator("mover", mover)

        board_sensor = BoardSensor(env)
        board_sensor.agent = self
        self.add_sensor("board_sensor", board_sensor)

    #creo q ya esta
    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    #creo q ya esta
    def _act(self, percept):
        action = self.function(percept)
        
        action_actuators = {
            "move": (self._actuators["mover"]),
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)

    #creo q ya esta
    def behave(self):
        percept = self._perceive()
        self._act(percept)

    """
    def function(self, percept):
        action = {}
        if percept["dirt_sensor"]:
            action["name"] = "clean"
        else:
            choice = randrange(2)
            action["name"] = "move"
            action["params"] = {"direction": directions[choice]}
        return action

    def __init__(self, env: SimulatedEnvironment):
        super().__init__()
        env.add(self.id)

        mover = MoverActuator(env)
        mover.agent = self
        self.add_actuator("mover", mover)

        cleaner = CleanerActuator(env)
        cleaner.agent = self
        self.add_actuator("cleaner", cleaner)

        locator = LocationSensor(env)
        locator.agent = self
        self.add_sensor("location_sensor", locator)

        dirt_sensor = DirtSensor(env)
        dirt_sensor.agent = self
        self.add_sensor("dirt_sensor", dirt_sensor)

        # self.setup_function()

    def print_state(self):
        print("Estoy en la posición {} y la celda está {}".format(self._sensors["location_sensor"].sense(),
                                                                  "Sucia" if self._sensors[
                                                                      "dirt_sensor"].sense() else "Limpia"))

    def _perceive(self):
        percept = {}
        for sensor in self._sensors:
            percept[sensor] = self._sensors[sensor].sense()
        return percept

    def _act(self, percept):
        action = self.function(percept)

        action_actuators = {
            "move": (self._actuators["mover"], ["direction"]),
            "clean": (self._actuators["cleaner"], [])
        }

        actuator, expected_params = action_actuators.get(action["name"], (None, None))
        if actuator:
            args = [action["params"].get(param) for param in expected_params]
            actuator.act(*args)



    def behave(self):
        percept = self._perceive()
        self._act(percept)
"""