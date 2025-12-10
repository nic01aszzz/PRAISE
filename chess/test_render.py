from chessrenderers import ConsoleRenderer
from chessworld import Pawn, King, Rook 


class MockBuffer:
    def get_state(self):
        tablero_falso = {}
        
        tablero_falso["e1"] = King("white")
        tablero_falso["e8"] = King("black")
        
        tablero_falso["d2"] = Pawn("white")
        tablero_falso["e4"] = Pawn("white") 
        tablero_falso["d7"] = Pawn("black")
        
        tablero_falso["a1"] = Rook("white")

        return {
            "tablero": tablero_falso,
            "status": "in_progress",
            "turn_color": "white",
            "game_info": {}, 
            "en_passant": None
        }

def main():
    renderer = ConsoleRenderer()
    fake_buffer = MockBuffer()
    renderer.observe(fake_buffer)
    
    renderer.render()

if __name__ == "__main__":
    main()