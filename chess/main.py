import time
from chessworld import chessEnv
from chessagent import ChessAgent
from statebuffer import StateBuffer 
from chessrenderers import ConsoleRenderer 
import random

def main():    
    env = chessEnv()
    
    modo = input("¿Desea comenzar una partida nueva (1) o cargar un tablero desde FEN (2)? ")
    
    if modo == "2":
        fen_str = input("Ingresa la cadena FEN: ").strip()
        try:
            env_fen = chessEnv()
            env_fen.FEN_board_loader(fen_str)
            print("Tablero cargado exitosamente.")
            env = env_fen
        except Exception as e:
            print(f"Error al cargar FEN: {e}")
            print("Se jugará con un tablero nuevo.")

    agente = ChessAgent(env)
    
    human_id = 999
    env.add(human_id)

    eleccion = random.randint(1,2)
    
    if eleccion == '1':
        color_humano = "black"
        color_agente = "white"
    else:
        color_humano = "white"
        color_agente = "black"

    env._agents_colors[human_id] = color_humano
    env._agents_colors[agente.id] = color_agente

    print(f"\nJuego comenzado: Humano ({color_humano}) vs Agente ({color_agente})!")

    human_buffer = StateBuffer(human_id, env)
    renderer = ConsoleRenderer()
    renderer.observe(human_buffer)
    print("Para mover, primero ingrese la casilla de origen y luego la de destino (ejemplo, e2 - enter - e4)")
    print("Para salir, ingrese exit")
    while True:
        state_actual = human_buffer.state

        status = state_actual["status"]
        if status != "in_progress":
            print(f"\nJuego terminado como: {status}!")
            break

        turn_color = state_actual["turn_color"]
        
        print(f"Movimiento #: {env._game_info['move_counter']}")

        if turn_color == color_humano:
            renderer.render()
            print(f"\n>> Tu turno.")
            while True:
                origen = input("Origen: ").strip()
                if origen == "exit": return
                destino = input("Destino: ").strip()
                
                contador_antes = env._game_info["move_counter"]
                env.take_action(human_id, "move", {"origen": origen, "destino": destino})
                if env._game_info["move_counter"] > contador_antes:
                    break 
                else:
                    print("Movimiento inválido, ilegal o inseguro (Jaque). Intenta de nuevo.")
        else:
            print(f"\n>> Turno agente ({color_agente})")
            time.sleep(1)
            agente.behave()

if __name__ == "__main__":
    main()