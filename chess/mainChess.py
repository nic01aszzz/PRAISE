from .chessworld import chessEnv, white_color, black_color
from .chessagent import ChessAgent, ChessHuman
from statebuffer import StateBuffer 
from .chessrenderers import ConsoleRenderer, PygameRenderer 
import uuid
import random
import time
import threading
import queue

agent_finished_flag = False
event_render_ready = threading.Event()

def mainConsoleRenderer(env, modo):
    jugadores = []

    if modo == "1":
        # Humano vs Humano
        blanco = ChessHuman(env, None)
        negro = ChessHuman(env, None)
        env._agents_colors[blanco.id] = white_color
        env._agents_colors[negro.id] = black_color
        
        jugadores.extend([blanco, negro])
        print("\nJuego comenzado: Humano (Blanco) vs Humano (Negro)!")

    elif modo == "2":
        # Humano vs IA
        humano = ChessHuman(env, None)
        agente = ChessAgent(env)
        
        eleccion = random.randint(1, 2)
        color_humano = white_color if eleccion == 1 else black_color
        color_agente = black_color if eleccion == 1 else white_color
        
        env._agents_colors[humano.id] = color_humano
        env._agents_colors[agente.id] = color_agente
        
        jugadores.extend([humano, agente])
        print(f"\nJuego comenzado: Humano ({color_humano}) vs Agente ({color_agente})!")

    elif modo == "3":
        # IA vs IA
        agente_blanco = ChessAgent(env)
        agente_negro = ChessAgent(env)
        env._agents_colors[agente_blanco.id] = white_color
        env._agents_colors[agente_negro.id] = black_color
        
        jugadores.extend([agente_blanco, agente_negro])
        print("\nJuego comenzado: IA (Blanco) vs IA (Negro)!")

    # Buffer independiente para renderizar
    arbitro_id = uuid.uuid1().int
    env.add(arbitro_id)
    buffer = StateBuffer(arbitro_id, env)
    
    renderer = ConsoleRenderer()
    renderer.observe(buffer)
    env._update_statebuffers()
    
    print("Para mover, primero ingrese la casilla de origen y luego la de destino (ejemplo, e2 - enter - e4)")
    print("Para salir, ingrese exit")

    while True:
        renderer.render()
        state_actual = buffer.state

        status = state_actual["status"]
        if status != "in_progress":
            print(f"\nJuego terminado como: {status}!")
            break

        print(f"Movimiento #: {env._game_info['move_counter']}")

        for jugador in jugadores:
            if isinstance(jugador, ChessAgent):
                time.sleep(0.5) 
            
            resultado = jugador.behave()
            if resultado is False:
                return

def mainPygameRenderer(env, modo):
    global agent_finished_flag
    agent_finished_flag = False
    
    action_queue = queue.Queue()
    jugadores = {}

    if modo == "1":
        # Humano vs Humano
        blanco = ChessHuman(env, action_queue)
        negro = ChessHuman(env, action_queue)
        env._agents_colors[blanco.id] = white_color
        env._agents_colors[negro.id] = black_color
        
        jugadores[white_color] = blanco
        jugadores[black_color] = negro

    elif modo == "2":
        # Humano vs IA
        humano = ChessHuman(env, action_queue)
        agente = ChessAgent(env)
        
        eleccion = random.randint(1, 2)
        color_humano = white_color if eleccion == 1 else black_color
        color_agente = black_color if eleccion == 1 else white_color
        
        env._agents_colors[humano.id] = color_humano
        env._agents_colors[agente.id] = color_agente
        
        jugadores[color_humano] = humano
        jugadores[color_agente] = agente

    elif modo == "3":
        # IA vs IA
        agente_blanco = ChessAgent(env)
        agente_negro = ChessAgent(env)
        env._agents_colors[agente_blanco.id] = white_color
        env._agents_colors[agente_negro.id] = black_color
        
        jugadores[white_color] = agente_blanco
        jugadores[black_color] = agente_negro

    arbitro_id = uuid.uuid1().int
    env.add(arbitro_id)
    buffer = StateBuffer(arbitro_id, env)
    
    renderer = PygameRenderer(action_queue=action_queue) 
    renderer.observe(statebuffer=buffer) 
    env._update_statebuffers()

    thread_logic = threading.Thread(
        target=game_logic_thread_pygame, 
        args=(env, jugadores)
    )
    thread_logic.start()

    while not agent_finished_flag:
        renderer.render()
        event_render_ready.set()
        time.sleep(0.03)

    thread_logic.join()

def game_logic_thread_pygame(env, jugadores):
    global agent_finished_flag

    lista_jugadores = list(jugadores.values())

    while True:
        status = env.get_game_status()
        if status != "in_progress":
            print(f"\nJuego terminado como: {status}")
            break

        for jugador in lista_jugadores:
            resultado = jugador.behave()
            if resultado is False:
                agent_finished_flag = True
                return

        event_render_ready.wait(timeout=0.03) 
        event_render_ready.clear()
        
    agent_finished_flag = True

def main():    
    env = chessEnv()
    print("1. Humano vs Humano")
    print("2. Humano vs IA")
    print("3. IA vs IA")
    modo = input("Seleccione modo (1/2/3): ").strip()
    
    modo_grafico = input("¿Jugar en consola (1) o con interfaz gráfica (2)? ").strip()

    tipo_tablero = input("¿Desea comenzar una partida nueva (1) o cargar un tablero desde FEN (2)? ").strip()
    if tipo_tablero == "2":
        fen_str = input("Ingresa la cadena FEN: ").strip()
        try:
            env.FEN_board_loader(fen_str)
            print("Tablero FEN cargado exitosamente.")
        except Exception as e:
            print(f"Error al cargar FEN: {e}")
            print("Se jugará con el tablero estándar.")

    if modo_grafico == "1":
        mainConsoleRenderer(env, modo) 
    else:
        mainPygameRenderer(env, modo)
 
if __name__ == "__main__":
    main()