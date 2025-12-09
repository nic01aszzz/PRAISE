from chessworld import chessEnv
from chessagent import ChessAgent
import time

def imprimir_tablero_consola(env):
    """
    Imprime el tablero ASCII. 
    Mayúsculas = Blancas (Tu)
    Minúsculas = Negras (Bot)
    """
    tablero = env._tablero
    print("\n   a b c d e f g h")
    print("  -----------------")
    
    filas = ['8', '7', '6', '5', '4', '3', '2', '1']
    columnas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    simbolos = {
        "Pawn": "P", "Rook": "R", "Knight": "N",
        "Bishop": "B", "Queen": "Q", "King": "K"
    }

    for fila in filas:
        linea = f"{fila} |"
        for col in columnas:
            pieza = tablero.get(col + fila)
            if pieza is None:
                linea += ". "
            else:
                tipo = type(pieza).__name__
                letra = simbolos.get(tipo, "?")
                if pieza.color == "black":
                    letra = letra.lower()
                linea += f"{letra} "
        print(linea + f"| {fila}")
    print("  -----------------")
    print("   a b c d e f g h\n")


def main():
    env = chessEnv()

    bot = ChessAgent(env)
    
    human_id = 999
    env.add(human_id)


    env._agents_colors[human_id] = "white"
    env._agents_colors[bot.id] = "black"

    print("Comienza: Jugador (Blancas/Mayúsculas) vs Agente (Negras/Minúsculas)")
    imprimir_tablero_consola(env)

    while True:
        estado = env.get_game_status()
        if estado != "in_progress":
            print(f"Fin del juego: {estado}!")
            break

        turn_color = "white" if env._game_info["move_counter"] % 2 == 0 else "black"
        
        if turn_color == "white":
            print(f"Tu Turno (Blancas). Ingresa primero la casilla de inicio del movimiento y luego la del fin)")
            
            while True:
                origen = input("Origen (ej: e2): ").strip()
                if origen == "exit": return
                
                destino = input("Destino (ej: e4): ").strip()
                
                contador_previo = env._game_info["move_counter"]
                
                env.take_action(human_id, "move", {"origen": origen, "destino": destino})
                
                if env._game_info["move_counter"] > contador_previo:
                    imprimir_tablero_consola(env)
                    break
                else:
                    print("Movimiento inválido o inseguro. Intenta de nuevo.")

        else:

            print("Turno del agente (Negras)")
            time.sleep(1) 
            bot.behave()
            imprimir_tablero_consola(env)

if __name__ == "__main__":
    main()